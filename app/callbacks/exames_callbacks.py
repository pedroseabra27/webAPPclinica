import dash
from dash import Input, Output, State, html, callback_context, ALL, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from app import app
from app.models.data_store import dados_plot_exame, ptr_exame, pacientes_cadastrados_web, NUM_CANAIS_EXAME, PONTOS_GRAFICO_EXAME
import logging # Adicionar logging

logger = logging.getLogger(__name__) # Configurar logger para este módulo

# Estado global simulado para o exame
ESTADO_EXAME = {
    'em_andamento': False,
    'paciente_selecionado': None,
    'modo': 'offline',
    'pagina_atual': 1,
    'total_paginas': 100,  # Simulado
    'tamanho_janela': '30',
    'mostrar_grid': False,
    'canais_visiveis': ['EEG1', 'EEG2', 'EOG', 'EMG', 'ECG', 'Flow', 'Chest', 'ABD'],
    'canal_selecionado': 'EEG1',
    'ganho_canais': {'EEG1': 1.0, 'EEG2': 1.0, 'EOG': 1.0, 'EMG': 1.0, 
                    'ECG': 1.0, 'Flow': 1.0, 'Chest': 1.0, 'ABD': 1.0},
    'filtro_canais': {'EEG1': False, 'EEG2': False, 'EOG': False, 'EMG': False, 
                     'ECG': False, 'Flow': False, 'Chest': False, 'ABD': False},
    'comentarios': [],
    'estagios': [None] * 100,  # Simulados para 100 páginas
    'camera_conectada': False
}

# Lista de canais disponíveis (pode ser expandida conforme necessário)
CANAIS_DISPONIVEIS = [
    {'id': 'EEG1', 'nome': 'EEG C3-A2'},
    {'id': 'EEG2', 'nome': 'EEG C4-A1'},
    {'id': 'EOG', 'nome': 'EOG E1-A2'},
    {'id': 'EMG', 'nome': 'EMG Queixo'},
    {'id': 'ECG', 'nome': 'ECG'},
    {'id': 'Flow', 'nome': 'Fluxo Aéreo'},
    {'id': 'Chest', 'nome': 'Esforço Torácico'},
    {'id': 'ABD', 'nome': 'Esforço Abdominal'}
]

# Configurações rápidas para F2-F8
CONFIGURACOES_RAPIDAS = {
    'F2': ['EEG1', 'EEG2', 'EOG', 'EMG'],
    'F3': ['EEG1', 'EEG2', 'EOG', 'EMG', 'ECG'],
    'F4': ['Flow', 'Chest', 'ABD'],
    'F5': ['EEG1', 'EEG2', 'Flow', 'ECG'],
    'F6': ['EEG1', 'EEG2', 'EOG', 'EMG', 'ECG', 'Flow', 'Chest'],
    'F7': ['EEG1', 'EEG2', 'EOG', 'EMG', 'ECG', 'Flow', 'Chest', 'ABD'],  # Todos
    'F8': []  # Nenhum
}

# Comentários predefinidos
COMENTARIOS_PREDEFINIDOS = [
    "Apneia obstrutiva",
    "Apneia central",
    "Hipopneia",
    "Dessaturação",
    "Despertar breve",
    "Movimento de pernas",
    "Arritmia cardíaca",
    "Ronco"
]

# Callback para controle do exame (iniciar/terminar/reiniciar)
@app.callback(
    Output("intervalo-atualizacao-grafico", "disabled"),
    Output("intervalo-led-piscando", "disabled"),
    Output("btn-iniciar-exame-web", "disabled"),
    Output("btn-terminar-exame-web", "disabled"),
    Output("btn-reiniciar-exame-web", "disabled"),
    Output("status-exame-div", "children"),
    Input("btn-iniciar-exame-web", "n_clicks"),
    Input("btn-terminar-exame-web", "n_clicks"),
    Input("btn-reiniciar-exame-web", "n_clicks"),
    prevent_initial_call=True
)
def controlar_exame_web(n_iniciar, n_terminar, n_reiniciar):
    ctx = dash.callback_context
    if not ctx.triggered: 
        return True, True, False, True, True, "Exame parado."
    
    botao_clicado = ctx.triggered[0]['prop_id'].split('.')[0]
    global ptr_exame, dados_plot_exame, ESTADO_EXAME
    
    if botao_clicado == "btn-iniciar-exame-web":
        ptr_exame = 0
        for i in range(len(dados_plot_exame)): 
            dados_plot_exame[i] = np.zeros(500)
        ESTADO_EXAME['em_andamento'] = True
        return False, False, True, False, False, "Exame iniciado (simulado)..."
    
    elif botao_clicado == "btn-terminar-exame-web":
        ESTADO_EXAME['em_andamento'] = False
        return True, True, False, True, False, "Exame terminado."
    
    elif botao_clicado == "btn-reiniciar-exame-web":
        ptr_exame = 0
        for i in range(len(dados_plot_exame)): 
            dados_plot_exame[i] = np.zeros(500)
        ESTADO_EXAME['em_andamento'] = True
        return False, False, True, False, False, "Exame reiniciado (simulado)..."
    
    return True, True, False, True, True, "Exame parado."

# Callback para atualizar o LED piscando
@app.callback(
    Output("led-recebendo-dados", "style"),
    Input("intervalo-led-piscando", "n_intervals")
)
def atualizar_led_piscando(n_intervals):
    if n_intervals is None or ESTADO_EXAME['em_andamento'] == False:
        return {"display": "inline-block", "width": "15px", "height": "15px", 
                "border-radius": "50%", "background-color": "gray"}
    
    # LED pisca alternadamente
    if n_intervals % 2 == 0:
        return {"display": "inline-block", "width": "15px", "height": "15px", 
                "border-radius": "50%", "background-color": "green"}
    else:
        return {"display": "inline-block", "width": "15px", "height": "15px", 
                "border-radius": "50%", "background-color": "#90EE90"}

# Callback para atualizar o gráfico de exame
@app.callback(
    Output("grafico-polissonografia", "figure"),
    Input("intervalo-atualizacao-grafico", "n_intervals"),
    Input("select-tamanho-janela", "value"),
    Input("btn-toggle-grid", "n_clicks"),
    State("store-exame-estado", "data")
)
def atualizar_grafico_exame_web(n_intervals, tamanho_janela, n_grid, estado):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Atualizar estado com base nos inputs
    ESTADO_EXAME['tamanho_janela'] = tamanho_janela
    
    # Toggle grid quando o botão é clicado
    if triggered_id == "btn-toggle-grid":
        ESTADO_EXAME['mostrar_grid'] = not ESTADO_EXAME['mostrar_grid']
    
    # Gerar figura
    global ptr_exame, dados_plot_exame
    fig = go.Figure()
    
    # Definir cores para cada canal
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    # Criar o gráfico baseado nos canais visíveis
    y_offset = 0
    for i, canal_id in enumerate(ESTADO_EXAME['canais_visiveis']):
        if canal_id not in [c['id'] for c in CANAIS_DISPONIVEIS]:
            continue
        
        canal_idx = next((i for i, c in enumerate(CANAIS_DISPONIVEIS) if c['id'] == canal_id), i % len(dados_plot_exame))
        
        # Aplicar ganho ao canal
        ganho = ESTADO_EXAME['ganho_canais'].get(canal_id, 1.0)
        
        # Simular dados para o canal
        if ESTADO_EXAME['em_andamento'] and ESTADO_EXAME['modo'] == 'online':
            # No modo online, atualizamos os dados em tempo real
            amplitude = 20 + (canal_idx % 3) * 5
            frequencia_base = ptr_exame * 0.02
            frequencia_canal = (canal_idx * 0.5 + 1)
            dado_bruto = np.sin(frequencia_base * frequencia_canal * np.pi) * amplitude + np.random.normal(0, 1.5)
            dados_plot_exame[canal_idx % len(dados_plot_exame)][:-1] = dados_plot_exame[canal_idx % len(dados_plot_exame)][1:]
            dados_plot_exame[canal_idx % len(dados_plot_exame)][-1] = dado_bruto
        
        # Calcular offset visual para separar os canais visualmente
        offset_visual = y_offset
        y_offset += 50
        
        # Aplicar filtro se ativado
        dados_canal = dados_plot_exame[canal_idx % len(dados_plot_exame)].copy()
        if ESTADO_EXAME['filtro_canais'].get(canal_id, False):
            # Simular filtro - aqui estamos apenas suavizando o sinal
            from scipy.signal import savgol_filter
            dados_canal = savgol_filter(dados_canal, 15, 3)
        
        # Aplicar ganho
        dados_canal = dados_canal * ganho
        
        # Adicionar o traço ao gráfico
        nome_canal = next((c['nome'] for c in CANAIS_DISPONIVEIS if c['id'] == canal_id), canal_id)
        fig.add_trace(go.Scatter(
            y=dados_canal + offset_visual, 
            mode='lines', 
            name=nome_canal, 
            line=dict(color=cores[i % len(cores)]),
            hovertemplate=f"{nome_canal}: %{{y:.2f}} μV<extra></extra>"
        ))
    
    # Atualizar contador para simulação
    if ESTADO_EXAME['em_andamento'] and ESTADO_EXAME['modo'] == 'online':
        ptr_exame += 1
    
    # Configurar layout do gráfico
    fig.update_layout(
        title=f"Polissonografia - {'Online' if ESTADO_EXAME['modo'] == 'online' else 'Offline'} - "
              f"Janela: {ESTADO_EXAME['tamanho_janela']}s",
        xaxis_title="Tempo (s)",
        yaxis_title="Amplitude (μV)",
        showlegend=True,
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    # Adicionar grid se ativado
    if ESTADO_EXAME['mostrar_grid']:
        fig.update_layout(
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.2)')
        )
    else:
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
    
    # Definir intervalo visível no eixo X com base no tamanho da janela
    tamanho = int(ESTADO_EXAME['tamanho_janela'])
    fig.update_xaxes(range=[0, tamanho])
    
    return fig

# Callbacks para navegação por página
@app.callback(
    Output("store-exame-estado", "data"),
    Output("timeline-progress", "value"),
    Output("input-pagina-atual", "value"),
    Output("total-paginas", "children"),
    [
        Input("btn-home", "n_clicks"),
        Input("btn-left", "n_clicks"),
        Input("btn-right", "n_clicks"),
        Input("btn-end", "n_clicks"),
        Input("input-pagina-atual", "value"),
        Input("btn-page-up", "n_clicks"),
        Input("btn-page-down", "n_clicks"),
    ],
    [State("store-exame-estado", "data")]
)
def navegar_paginas(n_home, n_left, n_right, n_end, pagina_input, n_page_up, n_page_down, estado):
    ctx = dash.callback_context
    if not ctx.triggered:
        return estado, 0, 1, "100"  # Valores padrão
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    pagina_atual = int(estado.get('pagina_atual', 1))
    total_paginas = int(estado.get('total_paginas', 100))
    
    if botao_id == "btn-home":
        pagina_atual = 1
    elif botao_id == "btn-left":
        pagina_atual = max(1, pagina_atual - 1)
    elif botao_id == "btn-right":
        pagina_atual = min(total_paginas, pagina_atual + 1)
    elif botao_id == "btn-end":
        pagina_atual = total_paginas
    elif botao_id == "input-pagina-atual":
        try:
            pagina_atual = max(1, min(total_paginas, int(pagina_input)))
        except:
            pass
    elif botao_id == "btn-page-up":
        # Diminuir a escala (mostrar mais tempo)
        tamanho_atual = int(estado.get('tamanho_janela', 30))
        if tamanho_atual < 120:  # Máximo 2 minutos
            novo_tamanho = min(120, tamanho_atual * 2)
            estado['tamanho_janela'] = str(novo_tamanho)
    elif botao_id == "btn-page-down":
        # Aumentar a escala (mostrar menos tempo)
        tamanho_atual = int(estado.get('tamanho_janela', 30))
        if tamanho_atual > 5:  # Mínimo 5 segundos
            novo_tamanho = max(5, tamanho_atual // 2)
            estado['tamanho_janela'] = str(novo_tamanho)
    
    # Atualizar estado
    estado['pagina_atual'] = pagina_atual
    
    # Calcular porcentagem para a barra de progresso
    progress = (pagina_atual - 1) / (total_paginas - 1) * 100 if total_paginas > 1 else 0
    
    return estado, progress, pagina_atual, str(total_paginas)

# Callback para mostrar modal de seleção de paciente
@app.callback(
    Output("modal-selecionar-paciente", "is_open"),
    Output("modal-pacientes-lista", "children"),
    Input("btn-selecionar-paciente", "n_clicks"),
    Input("btn-fechar-modal-paciente", "n_clicks"),
    State("modal-selecionar-paciente", "is_open")
)
def toggle_modal_paciente(n_abrir, n_fechar, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, []
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if botao_id == "btn-selecionar-paciente":
        # Preparar lista de pacientes
        if not pacientes_cadastrados_web:
            lista_pacientes = [html.P("Nenhum paciente cadastrado.", className="text-muted")]
        else:
            lista_pacientes = [
                dbc.ListGroup([
                    dbc.ListGroupItem(
                        f"{p['nome']} (CPF: {p['cpf']})",
                        id=f"paciente-item-{i}",
                        action=True,
                        n_clicks=0
                    ) for i, p in enumerate(pacientes_cadastrados_web)
                ])
            ]
        return not is_open, lista_pacientes
    
    elif botao_id == "btn-fechar-modal-paciente":
        return not is_open, []
    
    return is_open, []

# Callback para atualizar informações do paciente selecionado
@app.callback(
    Output("info-paciente-exame", "children"),
    Output("modal-selecionar-paciente", "is_open", allow_duplicate=True),
    Input({"type": "paciente-item", "index": ALL}, "n_clicks"),
    State("modal-selecionar-paciente", "is_open"),
    prevent_initial_call=True
)
def selecionar_paciente(n_clicks_list, is_open):
    ctx = dash.callback_context
    if not ctx.triggered or not any(n > 0 for n in n_clicks_list):
        return [html.P("Nenhum paciente selecionado.", className="text-muted")], is_open
    
    # Encontrar qual paciente foi clicado
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger_id.startswith('paciente-item-'):
        try:
            idx = int(trigger_id.split('-')[-1])
            if idx < len(pacientes_cadastrados_web):
                paciente = pacientes_cadastrados_web[idx]
                ESTADO_EXAME['paciente_selecionado'] = paciente
                
                # Criar card com informações do paciente
                info_paciente = [
                    dbc.Card(
                        dbc.CardBody([
                            html.H5(paciente['nome'], className="card-title"),
                            html.P(f"CPF: {paciente['cpf']}"),
                            html.P(f"Idade: {paciente['idade']} anos"),
                            html.P(f"Endereço: {paciente['endereco']}"),
                            html.P(f"Telefone: {paciente['telefone']}")
                        ])
                    )
                ]
                return info_paciente, False  # Fecha o modal
        except (ValueError, IndexError):
            pass
    
    return [html.P("Nenhum paciente selecionado.", className="text-muted")], is_open

# Callback para mostrar modal de configuração de canais
@app.callback(
    Output("modal-alterar-canais", "is_open"),
    Output("lista-canais-configuracao", "children"),
    Input("btn-alterar-canais", "n_clicks"),
    Input("btn-aplicar-canais", "n_clicks"),
    Input("btn-cancelar-canais", "n_clicks"),
    State("modal-alterar-canais", "is_open")
)
def toggle_modal_canais(n_abrir, n_aplicar, n_cancelar, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, []
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if botao_id == "btn-alterar-canais":
        # Preparar lista de canais para configuração
        items = []
        for canal in CANAIS_DISPONIVEIS:
            checked = canal['id'] in ESTADO_EXAME['canais_visiveis']
            items.append(
                dbc.ListGroupItem([
                    dbc.Checkbox(id=f"check-canal-{canal['id']}", checked=checked, className="me-2"),
                    html.Span(f"{canal['nome']} ({canal['id']})")
                ], className="d-flex align-items-center")
            )
        return not is_open, items
    
    elif botao_id in ["btn-aplicar-canais", "btn-cancelar-canais"]:
        # Atualizar canais visíveis se foi aplicado
        # (Precisaríamos de um callback separado para capturar os valores dos checkboxes)
        return False, []
    
    return is_open, []

# Callback para configurações rápidas (F2-F8)
@app.callback(
    Output("store-exame-estado", "data", allow_duplicate=True),
    [
        Input("btn-f2", "n_clicks"),
        Input("btn-f3", "n_clicks"),
        Input("btn-f4", "n_clicks"),
        Input("btn-f5", "n_clicks"),
        Input("btn-f6", "n_clicks"),
        Input("btn-f7", "n_clicks"),
        Input("btn-f8", "n_clicks"),
    ],
    State("store-exame-estado", "data"),
    prevent_initial_call=True
)
def aplicar_configuracao_rapida(n_f2, n_f3, n_f4, n_f5, n_f6, n_f7, n_f8, estado):
    ctx = dash.callback_context
    if not ctx.triggered:
        return estado
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if botao_id == "btn-f2":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F2']
    elif botao_id == "btn-f3":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F3']
    elif botao_id == "btn-f4":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F4']
    elif botao_id == "btn-f5":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F5']
    elif botao_id == "btn-f6":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F6']
    elif botao_id == "btn-f7":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F7']
    elif botao_id == "btn-f8":
        ESTADO_EXAME['canais_visiveis'] = CONFIGURACOES_RAPIDAS['F8']
    
    # Atualizar o estado
    estado['canais_visiveis'] = ESTADO_EXAME['canais_visiveis']
    return estado

# Callback para alternar entre modos online e offline
@app.callback(
    Output("btn-modo-online", "outline"),
    Output("btn-modo-offline", "outline"),
    Output("store-exame-estado", "data", allow_duplicate=True),
    [
        Input("btn-modo-online", "n_clicks"),
        Input("btn-modo-offline", "n_clicks"),
    ],
    State("store-exame-estado", "data"),
    prevent_initial_call=True
)
def alternar_modo(n_online, n_offline, estado):
    ctx = dash.callback_context
    if not ctx.triggered:
        return True, False, estado
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if botao_id == "btn-modo-online":
        ESTADO_EXAME['modo'] = 'online'
        estado['modo'] = 'online'
        return False, True, estado
    elif botao_id == "btn-modo-offline":
        ESTADO_EXAME['modo'] = 'offline'
        estado['modo'] = 'offline'
        return True, False, estado
    
    return True, False, estado

# Callback para mostrar modal de adicionar comentário
@app.callback(
    Output("modal-adicionar-comentario", "is_open"),
    Output("lista-comentarios-predefinidos", "children"),
    Input("btn-adicionar-comentario", "n_clicks"),
    Input("btn-confirmar-comentario", "n_clicks"),
    Input("btn-cancelar-comentario", "n_clicks"),
    State("modal-adicionar-comentario", "is_open"),
    State("input-comentario", "value")
)
def toggle_modal_comentario(n_abrir, n_confirmar, n_cancelar, is_open, comentario_texto):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, []
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if botao_id == "btn-adicionar-comentario":
        # Mostrar comentários predefinidos
        items = []
        for comentario in COMENTARIOS_PREDEFINIDOS:
            items.append(
                dbc.ListGroupItem(comentario, action=True, id=f"comentario-pred-{COMENTARIOS_PREDEFINIDOS.index(comentario)}")
            )
        return not is_open, items
    
    elif botao_id == "btn-confirmar-comentario":
        # Adicionar o comentário
        if comentario_texto:
            timestamp = datetime.now().strftime("%H:%M:%S")
            pagina = ESTADO_EXAME['pagina_atual']
            novo_comentario = {
                'texto': comentario_texto,
                'timestamp': timestamp,
                'pagina': pagina
            }
            ESTADO_EXAME['comentarios'].append(novo_comentario)
        return False, []
    
    elif botao_id == "btn-cancelar-comentario":
        return False, []
    
    return is_open, []

# Callback para atualizar a lista de comentários
@app.callback(
    Output("comentarios-lista", "children"),
    Input("btn-confirmar-comentario", "n_clicks"),
    Input("store-exame-estado", "data")  # Atualiza quando muda a página
)
def atualizar_lista_comentarios(n_clicks, estado):
    if not ESTADO_EXAME['comentarios']:
        return [html.P("Nenhum comentário adicionado.", className="text-muted")]
    
    # Mostrar todos os comentários
    comentarios_html = []
    for i, com in enumerate(ESTADO_EXAME['comentarios']):
        comentarios_html.append(
            html.Div([
                html.Span(f"[{com['timestamp']} - Pág {com['pagina']}] ", className="text-muted small me-1"),
                html.Span(com['texto'])
            ], className="mb-1")
        )
    
    return comentarios_html

# Callbacks para os estágios do sono
@app.callback(
    Output("estagio-atual", "children"),
    [
        Input("btn-estagio-acordado", "n_clicks"),
        Input("btn-estagio-rem", "n_clicks"),
        Input("btn-estagio-nrem1", "n_clicks"),
        Input("btn-estagio-nrem2", "n_clicks"),
        Input("btn-estagio-nrem3", "n_clicks"),
        Input("btn-estagio-nrem4", "n_clicks"),
        Input("btn-estagio-movimento", "n_clicks"),
        Input("btn-estagio-desconectado", "n_clicks"),
        Input("btn-estagio-auto", "n_clicks"),
    ],
    State("store-exame-estado", "data")
)
def atualizar_estagio_sono(n_a, n_r, n_1, n_2, n_3, n_4, n_m, n_d, n_auto, estado):
    ctx = dash.callback_context
    if not ctx.triggered:
        # Mostrar o estágio atual da página atual, se existir
        pagina = estado.get('pagina_atual', 1)
        if 0 < pagina <= len(ESTADO_EXAME['estagios']):
            estagio = ESTADO_EXAME['estagios'][pagina-1]
            if estagio:
                return estagio
        return "Não definido"
    
    botao_id = ctx.triggered[0]['prop_id'].split('.')[0]
    pagina = estado.get('pagina_atual', 1)
    
    # Verificar se está na janela de 15s
    tamanho_janela = estado.get('tamanho_janela', '30')
    if tamanho_janela != '15':
        return "Estágios só podem ser definidos na janela de 15s"
    
    # Definir o estágio conforme o botão clicado
    if botao_id == "btn-estagio-acordado":
        estagio = "Acordado (A)"
    elif botao_id == "btn-estagio-rem":
        estagio = "REM (R)"
    elif botao_id == "btn-estagio-nrem1":
        estagio = "Não REM 1 (1)"
    elif botao_id == "btn-estagio-nrem2":
        estagio = "Não REM 2 (2)"
    elif botao_id == "btn-estagio-nrem3":
        estagio = "Não REM 3 (3)"
    elif botao_id == "btn-estagio-nrem4":
        estagio = "Não REM 4 (4)"
    elif botao_id == "btn-estagio-movimento":
        estagio = "Movimento (M)"
    elif botao_id == "btn-estagio-desconectado":
        estagio = "Desconectado (D)"
    elif botao_id == "btn-estagio-auto":
        # Simular cálculo automático
        import random
        opcoes = ["Acordado (A)", "REM (R)", "Não REM 1 (1)", "Não REM 2 (2)", 
                 "Não REM 3 (3)", "Não REM 4 (4)"]
        estagio = random.choice(opcoes)
    
    # Salvar o estágio para a página atual
    if 0 < pagina <= len(ESTADO_EXAME['estagios']):
        ESTADO_EXAME['estagios'][pagina-1] = estagio
    
    return estagio

# Callback para controlar a visibilidade da seção de análise de estágios
@app.callback(
    Output("analise-estagio-visibilidade", "style"),
    Input("select-tamanho-janela", "value")
)
def controlar_visibilidade_estágios(tamanho_janela):
    # A análise de estágios só deve estar visível na janela de 15s
    if tamanho_janela == "15":
        return {"display": "block"}
    else:
        return {"display": "none"}

from dash import Input, Output, State, no_update, callback_context # Modificado aqui
import plotly.graph_objs as go
import numpy as np
from app import app
from app.models.data_store import dados_plot_exame, ptr_exame, NUM_CANAIS_EXAME, PONTOS_GRAFICO_EXAME

# Simulação de dados para 32 canais
def simular_novos_dados_exame():
    global ptr_exame
    novos_dados_batch = []
    for i in range(NUM_CANAIS_EXAME):
        # Gerar dados diferentes para cada canal para melhor visualização
        # Ex: senoides com frequências/amplitudes diferentes ou ruído com offsets
        frequencia_base = (i + 1) * 0.5 
        amplitude_base = 5 + i 
        ruido = np.random.randn() * (2 + i*0.2) # Ruído diferente por canal
        novo_ponto = np.sin(ptr_exame * 0.02 * frequencia_base) * amplitude_base + ruido
        novos_dados_batch.append(novo_ponto)
    
    ptr_exame += 1
    return novos_dados_batch

@app.callback(
    Output('interval-component-exames', 'disabled'),
    Output('store-estado-exame', 'data'),
    Output('btn-iniciar-exame', 'disabled'),
    Output('btn-pausar-exame', 'disabled'),
    Input('btn-iniciar-exame', 'n_clicks'),
    Input('btn-pausar-exame', 'n_clicks'),
    State('store-estado-exame', 'data'),
    prevent_initial_call=True
)
def controlar_estado_exame(n_iniciar, n_pausar, estado_atual):
    # Adicionar logs para depuração
    logger.info(f"Callback 'controlar_estado_exame' acionado.")
    logger.info(f"n_iniciar: {n_iniciar}, n_pausar: {n_pausar}, estado_atual: {estado_atual}")

    ctx = callback_context # Usar dash.callback_context
    if not ctx.triggered:
        logger.warning("Nenhum input acionou o callback 'controlar_estado_exame'. Retornando no_update para tudo.")
        return no_update, no_update, no_update, no_update

    triggered_id = ctx.triggered_id
    logger.info(f"ID do componente que acionou: {triggered_id}")

    if triggered_id == 'btn-iniciar-exame':
        logger.info("Botão 'Iniciar' clicado. Configurando para rodar.")
        # Intervalo habilitado (disabled=False), rodando=True, Botão Iniciar desabilitado, Botão Pausar habilitado
        return False, {'rodando': True}, True, False
    elif triggered_id == 'btn-pausar-exame':
        logger.info("Botão 'Pausar' clicado. Configurando para pausar.")
        # Intervalo desabilitado (disabled=True), rodando=False, Botão Iniciar habilitado, Botão Pausar desabilitado
        return True, {'rodando': False}, False, True
    
    logger.warning(f"ID do gatilho '{triggered_id}' não esperado no callback 'controlar_estado_exame'. Retornando no_update.")
    return no_update, no_update, no_update, no_update


@app.callback(
    Output('live-graph-exames', 'figure'),
    Input('interval-component-exames', 'n_intervals'),
    State('store-estado-exame', 'data') 
)
def update_graph_live_exames(n, estado_exame):
    if not estado_exame['rodando'] and n > 0 : # Se não estiver rodando E não for o primeiro carregamento
        return no_update # Não atualiza o gráfico se estiver pausado

    novos_dados = simular_novos_dados_exame()

    traces = []
    for i in range(NUM_CANAIS_EXAME):
        dados_plot_exame[i][:-1] = dados_plot_exame[i][1:]
        dados_plot_exame[i][-1] = novos_dados[i]
        
        offset_vertical = i * 20 

        trace = go.Scatter(
            y=dados_plot_exame[i] + offset_vertical,
            name=f'Canal {i+1}',
            mode='lines',
        )
        traces.append(trace)

    layout = go.Layout(
        xaxis=dict(title='Tempo (amostras)', showticklabels=False, zeroline=False, showgrid=False), 
        yaxis=dict(title='Amplitude + Offset', showticklabels=False, zeroline=False, showgrid=False), 
        showlegend=False, 
        margin=dict(l=20, r=20, t=30, b=20), 
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)', 
    )

    return {'data': traces, 'layout': layout}
