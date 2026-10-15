"""
Motor de Agregação SRE e FinOps (FastAPI Router).
Transforma os eventos brutos de IA em indicadores de saúde (Golden Signals, SLI/SLO p95)
e telemetria financeira de custos (FinOps por modelo e rota).
"""

from __future__ import annotations

import math
from typing import Any
from fastapi import APIRouter
from src.app.observabilidade import (
    SLO_LIMITE_P95_MS,
    SLO_LIMITE_TAXA_ERRO,
    estado_processo,
    listar_chamadas,
    listar_execucoes,
)

router = APIRouter(tags=["observabilidade"])


def _percentil_95(valores: list[int]) -> int:
    """Calcula o p95 (Nearest-Rank) para mensurar a cauda longa de latência."""
    if not valores:
        return 0
    ordenados = sorted(valores)
    indice = math.ceil(0.95 * len(ordenados)) - 1
    return ordenados[min(max(indice, 0), len(ordenados) - 1)]


def _media(valores: list[float | int]) -> float:
    return (sum(valores) / len(valores)) if valores else 0.0


def _agrupar(itens: list[dict[str, Any]], chave: str) -> dict[str, list[dict[str, Any]]]:
    grupos: dict[str, list[dict[str, Any]]] = {}
    for item in itens:
        val = str(item.get(chave) or "desconhecido")
        grupos.setdefault(val, []).append(item)
    return grupos


@router.get("/monitor")
def obter_painel_observabilidade() -> dict[str, Any]:
    """Retorna os dados agregados de SRE e FinOps para visualização e monitoramento."""
    execucoes = listar_execucoes()
    chamadas = listar_chamadas()
    proc = estado_processo()

    latencias = [e["latencia_ms"] for e in execucoes]
    erros = sum(1 for e in execucoes if e["status"] == "erro")
    bloqueios = sum(1 for e in execucoes if e["status"] == "bloqueado")
    taxa_erro = (erros / len(execucoes)) if execucoes else 0.0
    p95 = _percentil_95(latencias)

    tokens_in = sum(c["tokens_entrada"] for c in chamadas)
    tokens_out = sum(c["tokens_saida"] for c in chamadas)
    custo_total = sum(c["custo_usd"] for c in chamadas)

    # Agrupamento por Modelo
    por_modelo_bruto = _agrupar(chamadas, "modelo")
    mais_usado = "—"
    if por_modelo_bruto:
        mais_usado = max(
            por_modelo_bruto,
            key=lambda nome: (
                len(por_modelo_bruto[nome]),
                sum(i["tokens_entrada"] + i["tokens_saida"] for i in por_modelo_bruto[nome]),
            ),
        )

    por_modelo = [
        {
            "modelo": mod,
            "chamadas": len(itens),
            "tokens_entrada": sum(i["tokens_entrada"] for i in itens),
            "tokens_saida": sum(i["tokens_saida"] for i in itens),
            "custo_usd": round(sum(i["custo_usd"] for i in itens), 6),
            "latencia_media_ms": round(_media([i["latencia_ms"] for i in itens])),
            "fallbacks": sum(1 for i in itens if i.get("fallback")),
        }
        for mod, itens in por_modelo_bruto.items()
    ]
    por_modelo.sort(key=lambda x: x["custo_usd"], reverse=True)

    # Agrupamento por Rota / Especialista
    por_rota_bruto = _agrupar(execucoes, "rota")
    por_rota = [
        {
            "rota": r,
            "turnos": len(itens),
            "erros": sum(1 for i in itens if i["status"] == "erro"),
            "bloqueios": sum(1 for i in itens if i["status"] == "bloqueado"),
            "latencia_media_ms": round(_media([i["latencia_ms"] for i in itens])),
            "custo_usd": round(sum(i["custo_usd"] for i in itens), 6),
        }
        for r, itens in por_rota_bruto.items()
    ]
    por_rota.sort(key=lambda x: x["turnos"], reverse=True)

    # Série Temporal de Custo Acumulado
    acumulado = 0.0
    serie_custo = []
    for ex in execucoes:
        acumulado += ex["custo_usd"]
        serie_custo.append({"hora": ex["hora"], "custo_acumulado_usd": round(acumulado, 6)})

    return {
        "slo": {
            "latencia_p95_limite_ms": SLO_LIMITE_P95_MS,
            "taxa_erro_limite": SLO_LIMITE_TAXA_ERRO,
        },
        "resumo": {
            "turnos": len(execucoes),
            "em_andamento": proc["em_andamento"],
            "no_ar_segundos": proc["no_ar_segundos"],
            "taxa_erro": round(taxa_erro, 4),
            "bloqueios": bloqueios,
            "latencia_media_ms": round(_media(latencias)),
            "latencia_p95_ms": p95,
            "slo_ok": (p95 <= SLO_LIMITE_P95_MS) and (taxa_erro <= SLO_LIMITE_TAXA_ERRO),
            "tokens_entrada": tokens_in,
            "tokens_saida": tokens_out,
            "tokens_total": tokens_in + tokens_out,
            "custo_usd": round(custo_total, 6),
            "modelo_mais_usado": mais_usado,
            "fallbacks": sum(1 for c in chamadas if c.get("fallback")),
        },
        "serie_latencia": [{"hora": e["hora"], "latencia_ms": e["latencia_ms"]} for e in execucoes],
        "serie_custo": serie_custo,
        "por_modelo": por_modelo,
        "por_rota": por_rota,
        "turnos": [
            {
                **e,
                "session_id": e["contexto_id"],
                "custo_usd": round(e["custo_usd"], 6),
            }
            for e in execucoes
        ],
    }
