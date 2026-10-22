"""
Motor de Agregação SRE e FinOps (FastAPI Router).
Transforma os eventos brutos de IA em indicadores de saúde (Golden Signals, SLI/SLO p95)
e telemetria financeira de custos (FinOps por modelo e rota).
Suporta tanto visualização gráfica web (HTML Dashboard) quanto API estruturada (JSON).
"""

from __future__ import annotations

import math
from typing import Any
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
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


def calcular_dados_monitor() -> dict[str, Any]:
    """Calcula as métricas agregadas de SRE e FinOps."""
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


def renderizar_dashboard_html() -> str:
    """Renderiza a página visual completa do painel de SRE & FinOps em HTML responsivo."""
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel SRE & FinOps | Cinttia AI</title>
    <style>
        :root {
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-hover: #334155;
            --border: #334155;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #38bdf8;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --card-radius: 12px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            padding: 1.5rem;
            line-height: 1.5;
        }
        .container { max-width: 1300px; margin: 0 auto; }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .title-group h1 { font-size: 1.75rem; font-weight: 700; color: var(--primary); }
        .title-group p { font-size: 0.9rem; color: var(--text-muted); }
        .controls { display: flex; gap: 0.75rem; align-items: center; }
        button, a.btn {
            background: var(--surface);
            color: var(--text);
            border: 1px solid var(--border);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.85rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            transition: all 0.2s;
        }
        button:hover, a.btn:hover { background: var(--surface-hover); border-color: var(--primary); }
        
        .slo-banner {
            padding: 1rem 1.25rem;
            border-radius: var(--card-radius);
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
        }
        .slo-ok { background: rgba(34, 197, 94, 0.15); border: 1px solid var(--success); color: #4ade80; }
        .slo-bad { background: rgba(239, 68, 68, 0.15); border: 1px solid var(--danger); color: #f87171; }
        
        .grid-kpis {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--card-radius);
            padding: 1.2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .card .label { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .card .value { font-size: 1.8rem; font-weight: 700; margin-top: 0.25rem; }
        .card .subtext { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem; }
        
        .tables-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 0.75rem;
        }
        th, td {
            padding: 0.6rem 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th { color: var(--text-muted); font-weight: 600; background: rgba(0,0,0,0.1); }
        tr:hover td { background: rgba(255,255,255,0.02); }
        
        .badge {
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }
        .badge-ok { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
        .badge-bloqueado { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-erro { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        
        .chart-box {
            display: flex;
            align-items: flex-end;
            gap: 4px;
            height: 120px;
            padding-top: 1rem;
            border-bottom: 1px solid var(--border);
            margin-top: 0.5rem;
        }
        .bar {
            flex: 1;
            background: var(--primary);
            border-radius: 3px 3px 0 0;
            min-height: 2px;
            position: relative;
            transition: height 0.3s ease;
        }
        .bar:hover { background: #7dd3fc; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="title-group">
                <h1>Painel de Observabilidade SRE & FinOps</h1>
                <p>Monitoramento contínuo em tempo real de modelos, latência, custos e governança</p>
            </div>
            <div class="controls">
                <a href="/" class="btn">💬 Ir para o Chat</a>
                <a href="/monitor/data" target="_blank" class="btn">🔌 JSON API</a>
                <button onclick="atualizarDados()">🔄 Atualizar</button>
                <label style="font-size: 0.85rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.3rem;">
                    <input type="checkbox" id="autoRefresh" checked> Auto-refresh (3s)
                </label>
            </div>
        </header>

        <div id="sloBanner" class="slo-banner slo-ok">
            <div>
                <span id="sloTitulo">🟢 SLO EM CONFORMIDADE</span>
                <span id="sloDesc" style="margin-left: 1rem; font-weight: normal; font-size: 0.85rem;">Latência p95 &le; 8.000ms | Taxa de Erro &le; 5.0%</span>
            </div>
            <span id="processUptime" style="font-size: 0.85rem; font-weight: normal;">Uptime: 0s</span>
        </div>

        <div class="grid-kpis">
            <div class="card">
                <div class="label">Latência p95</div>
                <div class="value" id="kpiP95">0 ms</div>
                <div class="subtext" id="kpiMedia">Média: 0 ms</div>
            </div>
            <div class="card">
                <div class="label">Taxa de Erro (SLO)</div>
                <div class="value" id="kpiTaxaErro">0.0%</div>
                <div class="subtext" id="kpiErros">0 erros de sistema</div>
            </div>
            <div class="card">
                <div class="label">Bloqueios de Guardrail</div>
                <div class="value" id="kpiBloqueios" style="color: var(--warning);">0</div>
                <div class="subtext">Segurança operando (Não é erro)</div>
            </div>
            <div class="card">
                <div class="label">Custo Total (USD)</div>
                <div class="value" id="kpiCusto" style="color: var(--primary);">$0.000000</div>
                <div class="subtext" id="kpiTokens">0 tokens processados</div>
            </div>
            <div class="card">
                <div class="label">Turnos / Em Andamento</div>
                <div class="value" id="kpiTurnos">0</div>
                <div class="subtext" id="kpiEmAndamento">0 concorrência ativa</div>
            </div>
            <div class="card">
                <div class="label">Modelo Mais Usado</div>
                <div class="value" id="kpiModelo" style="font-size: 1.2rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">—</div>
                <div class="subtext" id="kpiFallbacks">0 fallbacks ativados</div>
            </div>
        </div>

        <div class="tables-grid">
            <div class="card">
                <h3>💰 FinOps por Modelo</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Modelo</th>
                            <th>Chamadas</th>
                            <th>Tokens In/Out</th>
                            <th>Custo (USD)</th>
                            <th>Latência</th>
                        </tr>
                    </thead>
                    <tbody id="tbModelos">
                        <tr><td colspan="5" style="text-align:center; color: var(--text-muted);">Nenhuma chamada registrada</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="card">
                <h3>🧭 SRE por Rota de Especialista</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Rota</th>
                            <th>Turnos</th>
                            <th>Bloqueios</th>
                            <th>Erros</th>
                            <th>Latência Média</th>
                            <th>Custo (USD)</th>
                        </tr>
                    </thead>
                    <tbody id="tbRotas">
                        <tr><td colspan="6" style="text-align:center; color: var(--text-muted);">Nenhuma rota executada</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="card" style="margin-bottom: 1.5rem;">
            <h3>📈 Histórico de Latência Recente (ms)</h3>
            <div id="chartLatencia" class="chart-box"></div>
        </div>

        <div class="card">
            <h3>📑 Histórico Granular de Execuções Recentes</h3>
            <table>
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Session ID</th>
                        <th>Rota</th>
                        <th>Status</th>
                        <th>Latência</th>
                        <th>Tokens</th>
                        <th>Custo (USD)</th>
                    </tr>
                </thead>
                <tbody id="tbTurnos">
                    <tr><td colspan="7" style="text-align:center; color: var(--text-muted);">Nenhuma execução recente</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        let atualizacaoEmAndamento = false;

        async function atualizarDados() {
            if (atualizacaoEmAndamento) return;
            atualizacaoEmAndamento = true;
            const controlador = new AbortController();
            const timeout = setTimeout(() => controlador.abort(), 10000);
            try {
                const res = await fetch('/monitor/data', {
                    cache: 'no-store',
                    signal: controlador.signal,
                    headers: { 'Cache-Control': 'no-cache' }
                });
                if (!res.ok) return;
                const d = await res.json();
                
                // SLO Banner
                const banner = document.getElementById('sloBanner');
                const sloOk = d.resumo.slo_ok;
                banner.className = 'slo-banner ' + (sloOk ? 'slo-ok' : 'slo-bad');
                document.getElementById('sloTitulo').innerText = sloOk ? '🟢 SLO EM CONFORMIDADE' : '🔴 ALERTA DE VIOLAÇÃO DE SLO';
                document.getElementById('processUptime').innerText = 'Uptime: ' + d.resumo.no_ar_segundos + 's';
                
                // KPIs
                document.getElementById('kpiP95').innerText = d.resumo.latencia_p95_ms + ' ms';
                document.getElementById('kpiMedia').innerText = 'Média: ' + d.resumo.latencia_media_ms + ' ms';
                document.getElementById('kpiTaxaErro').innerText = (d.resumo.taxa_erro * 100).toFixed(1) + '%';
                document.getElementById('kpiBloqueios').innerText = d.resumo.bloqueios;
                document.getElementById('kpiCusto').innerText = '$' + d.resumo.custo_usd.toFixed(6);
                document.getElementById('kpiTokens').innerText = d.resumo.tokens_total.toLocaleString() + ' tokens (' + d.resumo.tokens_entrada.toLocaleString() + ' in / ' + d.resumo.tokens_saida.toLocaleString() + ' out)';
                document.getElementById('kpiTurnos').innerText = d.resumo.turnos;
                document.getElementById('kpiEmAndamento').innerText = d.resumo.em_andamento + ' em andamento agora';
                document.getElementById('kpiModelo').innerText = d.resumo.modelo_mais_usado;
                document.getElementById('kpiFallbacks').innerText = d.resumo.fallbacks + ' fallbacks ativados';
                
                // Tabela de Modelos
                const tbMod = document.getElementById('tbModelos');
                if (d.por_modelo && d.por_modelo.length > 0) {
                    tbMod.innerHTML = d.por_modelo.map(m => `
                        <tr>
                            <td><strong>${m.modelo}</strong> ${m.fallbacks > 0 ? '<span class="badge badge-bloqueado">Fallback</span>' : ''}</td>
                            <td>${m.chamadas}</td>
                            <td>${m.tokens_entrada.toLocaleString()} / ${m.tokens_saida.toLocaleString()}</td>
                            <td style="color: var(--primary); font-weight:600;">$${m.custo_usd.toFixed(6)}</td>
                            <td>${m.latencia_media_ms} ms</td>
                        </tr>
                    `).join('');
                } else {
                    tbMod.innerHTML = '<tr><td colspan="5" style="text-align:center; color: var(--text-muted);">Nenhuma chamada registrada</td></tr>';
                }

                // Tabela de Rotas
                const tbRot = document.getElementById('tbRotas');
                if (d.por_rota && d.por_rota.length > 0) {
                    tbRot.innerHTML = d.por_rota.map(r => `
                        <tr>
                            <td><strong>${r.rota}</strong></td>
                            <td>${r.turnos}</td>
                            <td><span style="color: var(--warning);">${r.bloqueios || 0}</span></td>
                            <td><span style="color: ${r.erros > 0 ? 'var(--danger)' : 'var(--text-muted)'};">${r.erros}</span></td>
                            <td>${r.latencia_media_ms} ms</td>
                            <td style="color: var(--primary);">$${r.custo_usd.toFixed(6)}</td>
                        </tr>
                    `).join('');
                } else {
                    tbRot.innerHTML = '<tr><td colspan="6" style="text-align:center; color: var(--text-muted);">Nenhuma rota executada</td></tr>';
                }

                // Gráfico de Barras de Latência
                const chartBox = document.getElementById('chartLatencia');
                if (d.serie_latencia && d.serie_latencia.length > 0) {
                    const maxLat = Math.max(...d.serie_latencia.map(s => s.latencia_ms), 100);
                    chartBox.innerHTML = d.serie_latencia.slice(-30).map(s => {
                        const h = Math.max(4, Math.round((s.latencia_ms / maxLat) * 110));
                        return `<div class="bar" style="height:${h}px;" title="${s.hora}: ${s.latencia_ms}ms"></div>`;
                    }).join('');
                } else {
                    chartBox.innerHTML = '<div style="color: var(--text-muted); font-size: 0.85rem; align-self: center; width: 100%; text-align: center;">Aguardando execuções...</div>';
                }

                // Tabela de Turnos Granulares
                const tbTur = document.getElementById('tbTurnos');
                if (d.turnos && d.turnos.length > 0) {
                    tbTur.innerHTML = d.turnos.slice().reverse().map(t => {
                        let badgeClass = 'badge-ok';
                        if (t.status === 'bloqueado') badgeClass = 'badge-bloqueado';
                        else if (t.status === 'erro') badgeClass = 'badge-erro';
                        return `
                            <tr>
                                <td>${t.hora}</td>
                                <td style="font-family: monospace; font-size: 0.8rem; color: var(--text-muted);">${(t.session_id || '—').substring(0, 18)}</td>
                                <td><strong>${t.rota}</strong></td>
                                <td><span class="badge ${badgeClass}">${t.status.toUpperCase()}</span></td>
                                <td>${t.latencia_ms} ms</td>
                                <td>${(t.tokens_total || 0).toLocaleString()}</td>
                                <td style="color: var(--primary);">$${t.custo_usd.toFixed(6)}</td>
                            </tr>
                        `;
                    }).join('');
                } else {
                    tbTur.innerHTML = '<tr><td colspan="7" style="text-align:center; color: var(--text-muted);">Nenhuma execução recente</td></tr>';
                }

            } catch (err) {
                if (err.name !== 'AbortError') console.error("Erro ao atualizar monitor:", err);
            } finally {
                clearTimeout(timeout);
                atualizacaoEmAndamento = false;
            }
        }

        atualizarDados();
        setInterval(() => {
            if (document.getElementById('autoRefresh').checked) {
                atualizarDados();
            }
        }, 1000);
    </script>
</body>
</html>
"""


@router.get("/monitor/data")
def obter_dados_monitor() -> dict[str, Any]:
    """Retorna os dados puros em JSON para a interface e integrações externas."""
    return calcular_dados_monitor()


@router.get("/monitor")
def obter_painel_observabilidade(request: Request) -> Any:
    """
    Endpoint principal de observabilidade.
    - Se acessado por um navegador (Accept: text/html), entrega a UI gráfica do Dashboard.
    - Se chamado por APIs / fetch / format=json, entrega o payload JSON consolidado.
    """
    accept = request.headers.get("accept", "")
    quer_json = request.query_params.get("format") == "json" or request.query_params.get("raw") == "1"

    if "text/html" in accept and not quer_json:
        return HTMLResponse(content=renderizar_dashboard_html(), status_code=200)

    return calcular_dados_monitor()
