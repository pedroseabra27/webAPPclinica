from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc

def layout_exames():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Visualização de Exames", className="my-4"))
        ]),
        html.Hr(),
        
        # Linha superior com controles principais
        dbc.Row([
            # Coluna esquerda com controle do exame
            dbc.Col([
                html.H4("Controle do Exame", className="mb-3"),
                dbc.ButtonGroup([
                    dbc.Button("Iniciar Exame", id="btn-iniciar-exame-web", color="success", className="me-2"),
                    dbc.Button("Terminar Exame", id="btn-terminar-exame-web", color="danger", disabled=True),
                    dbc.Button("Reiniciar Exame", id="btn-reiniciar-exame-web", color="warning", disabled=True),
                ], className="mb-3"),
                
                # Status do exame e recebimento de dados
                dbc.Row([
                    dbc.Col([
                        html.Div(id="status-exame-div", children="Exame parado.", className="mb-2 fw-bold"),
                    ], width=8),
                    dbc.Col([
                        # Indicador LED para mostrar se está recebendo dados
                        html.Div([
                            html.Span("Recebendo dados: ", className="me-2"),
                            html.Span(id="led-recebendo-dados", className="led-indicator led-off", 
                                     style={"display": "inline-block", "width": "15px", "height": "15px", 
                                           "border-radius": "50%", "background-color": "gray"})
                        ], className="d-flex align-items-center")
                    ], width=4)
                ], className="mb-3"),
            ], md=6),
            
            # Coluna direita com informações do paciente
            dbc.Col([
                html.H4("Paciente Selecionado", className="mb-3"),
                html.Div(id="info-paciente-exame", children=[
                    html.P("Nenhum paciente selecionado.", className="text-muted")
                ]),
                dbc.Button("Selecionar Paciente", id="btn-selecionar-paciente", color="primary", className="mt-2")
            ], md=6)
        ]),
        
        # Gráfico principal de polissonografia
        dbc.Row([
            dbc.Col([
                html.H4("Visualização dos Dados", className="mt-4 mb-3"),
                
                # Controles do Visualizador
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            # Controles de visualização
                            dbc.Col([
                                html.Div([
                                    html.Span("Modo: ", className="me-2"),
                                    dbc.ButtonGroup([
                                        dbc.Button("Online", id="btn-modo-online", color="primary", outline=True, size="sm"),
                                        dbc.Button("Offline", id="btn-modo-offline", color="secondary", outline=True, size="sm"),
                                    ], className="mb-2")
                                ]),
                            ], width=4),
                            
                            # Controles de janela e grid
                            dbc.Col([
                                html.Div([
                                    html.Span("Tamanho da janela: ", className="me-2"),
                                    dbc.Select(
                                        id="select-tamanho-janela",
                                        options=[
                                            {"label": "5s", "value": "5"},
                                            {"label": "15s", "value": "15"},
                                            {"label": "30s", "value": "30"},
                                            {"label": "1min", "value": "60"},
                                            {"label": "2min", "value": "120"},
                                        ],
                                        value="30",
                                        size="sm",
                                        style={"width": "80px"}
                                    ),
                                    dbc.Button("Grid", id="btn-toggle-grid", color="secondary", outline=True, size="sm", className="ms-2")
                                ], className="d-flex align-items-center"),
                            ], width=5),
                            
                            # Controles de canais
                            dbc.Col([
                                dbc.Button("Alterar Canais", id="btn-alterar-canais", color="info", outline=True, size="sm"),
                                dbc.Button("Capturar Tela", id="btn-capturar-tela", color="success", outline=True, size="sm", className="ms-2")
                            ], width=3, className="d-flex justify-content-end")
                        ]),
                        
                        # Segunda linha de controles - teclas de atalho F2-F8
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Span("Configurações rápidas: ", className="me-2"),
                                    dbc.ButtonGroup([
                                        dbc.Button("F2", id="btn-f2", color="secondary", outline=True, size="sm"),
                                        dbc.Button("F3", id="btn-f3", color="secondary", outline=True, size="sm"),
                                        dbc.Button("F4", id="btn-f4", color="secondary", outline=True, size="sm"),
                                        dbc.Button("F5", id="btn-f5", color="secondary", outline=True, size="sm"),
                                        dbc.Button("F6", id="btn-f6", color="secondary", outline=True, size="sm"),
                                        dbc.Button("F7", id="btn-f7", color="secondary", outline=True, size="sm"),
                                        dbc.Button("F8", id="btn-f8", color="secondary", outline=True, size="sm"),
                                    ])
                                ], className="mt-2")
                            ], width=12)
                        ])
                    ])
                ], className="mb-3"),
                
                # Gráfico principal
                dcc.Graph(id="grafico-polissonografia", style={'height': '45vh'}),
                
                # Controles de navegação
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.ButtonGroup([
                                    dbc.Button("⏮ Home", id="btn-home", color="primary", outline=True, size="sm"),
                                    dbc.Button("◀ Left", id="btn-left", color="primary", outline=True, size="sm"),
                                    dbc.Button("Right ▶", id="btn-right", color="primary", outline=True, size="sm"),
                                    dbc.Button("End ⏭", id="btn-end", color="primary", outline=True, size="sm"),
                                ]),
                            ], width=6),
                            dbc.Col([
                                # Controles de zoom/página
                                dbc.ButtonGroup([
                                    dbc.Button("Page Up", id="btn-page-up", color="secondary", outline=True, size="sm"),
                                    dbc.Button("Page Down", id="btn-page-down", color="secondary", outline=True, size="sm"),
                                ])
                            ], width=6, className="d-flex justify-content-end")
                        ]), 
                        dbc.Row([
                            dbc.Col([
                                # Barra de navegação / timeline
                                html.Div([
                                    dbc.Progress(id="timeline-progress", value=0, className="mt-3", style={"height": "15px"}),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Página"),
                                        dbc.Input(id="input-pagina-atual", value="1", type="number", min=1, style={"width": "80px"}),
                                        dbc.InputGroupText("de"),
                                        dbc.InputGroupText(id="total-paginas", children="1")
                                    ], size="sm", className="mt-2", style={"width": "250px"})
                                ])
                            ], width=12)
                        ])
                    ])
                ], className="mb-3")
            ], width=12),
        ]),
        
        # Linha inferior com vídeo e posição
        dbc.Row([
            dbc.Col([
                html.H5("Câmera", className="mb-2"),
                html.Div(
                    id="video-container", 
                    className="border rounded", 
                    style={"height": "15vh", "background-color": "#222", "display": "flex", "align-items": "center", "justify-content": "center"}
                ),
                html.Div(id="status-camera", className="text-center mt-1 small text-muted", children="Câmera não conectada")
            ], md=6),
            dbc.Col([
                html.H5("Posição no Leito", className="mb-2"),
                html.Div(
                    id="posicao-leito-container", 
                    className="border rounded", 
                    style={"height": "15vh", "background-color": "#f8f9fa", "display": "flex", "align-items": "center", "justify-content": "center"}
                )
            ], md=6)
        ]),
        
        # Seção de Comentários
        dbc.Row([
            dbc.Col([
                html.H5("Comentários", className="mt-4 mb-2"),
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="comentarios-lista", children=[
                            html.P("Nenhum comentário adicionado.", className="text-muted")
                        ], style={"max-height": "150px", "overflow-y": "auto"}),
                        dbc.Button("Adicionar Comentário", id="btn-adicionar-comentario", color="primary", size="sm", className="mt-2")
                    ])
                ])
            ], width=12)
        ]),
        
        # Seção de Análise de Estágios (visível apenas na janela de 15s)
        dbc.Row([
            dbc.Col([
                html.H5("Estágios do Sono", className="mt-4 mb-2"),
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            dbc.ButtonGroup([
                                dbc.Button("A", id="btn-estagio-acordado", color="primary", outline=True, size="sm", className="me-1", title="Acordado"),
                                dbc.Button("R", id="btn-estagio-rem", color="primary", outline=True, size="sm", className="me-1", title="REM"),
                                dbc.Button("1", id="btn-estagio-nrem1", color="primary", outline=True, size="sm", className="me-1", title="Não REM 1"),
                                dbc.Button("2", id="btn-estagio-nrem2", color="primary", outline=True, size="sm", className="me-1", title="Não REM 2"),
                                dbc.Button("3", id="btn-estagio-nrem3", color="primary", outline=True, size="sm", className="me-1", title="Não REM 3"),
                                dbc.Button("4", id="btn-estagio-nrem4", color="primary", outline=True, size="sm", className="me-1", title="Não REM 4"),
                                dbc.Button("M", id="btn-estagio-movimento", color="primary", outline=True, size="sm", className="me-1", title="Movimento"),
                                dbc.Button("D", id="btn-estagio-desconectado", color="primary", outline=True, size="sm", className="me-1", title="Desconectado"),
                                dbc.Button("E", id="btn-estagio-auto", color="primary", outline=True, size="sm", className="me-1", title="Calcular Estágio Automático"),
                                dbc.Button("L", id="btn-estagio-buscar", color="primary", outline=True, size="sm", className="me-1", title="Buscar Estágio"),
                            ]),
                            html.Div([
                                html.Span("Estágio Atual: ", className="me-2"),
                                html.Span(id="estagio-atual", children="Não definido", className="fw-bold")
                            ], className="mt-2")
                        ]),
                        html.Div(id="analise-estagio-visibilidade")
                    ])
                ])
            ], width=12)
        ]),
        
        # Elementos ocultos e intervalos para atualização
        dcc.Interval(
            id='intervalo-atualizacao-grafico',
            interval=200,
            n_intervals=0,
            disabled=True
        ),
        dcc.Interval(
            id='intervalo-led-piscando',
            interval=500,
            n_intervals=0,
            disabled=True
        ),
        
        # Store para armazenar estado do exame
        dcc.Store(id='store-exame-estado', data={'modo': 'offline', 'grid': False, 'pagina_atual': 1, 'total_paginas': 1}),
        
        # Modal para selecionar paciente
        dbc.Modal(
            [
                dbc.ModalHeader("Selecione um paciente"),
                dbc.ModalBody(id="modal-pacientes-lista"),
                dbc.ModalFooter(
                    dbc.Button("Fechar", id="btn-fechar-modal-paciente", className="ms-auto")
                ),
            ],
            id="modal-selecionar-paciente",
            size="lg",
        ),
        
        # Modal para alterar canais
        dbc.Modal(
            [
                dbc.ModalHeader("Configurar Canais"),
                dbc.ModalBody([
                    html.P("Selecione os canais para exibição e sua ordem:"),
                    dbc.ListGroup(id="lista-canais-configuracao", style={"max-height": "50vh", "overflow-y": "auto"})
                ]),
                dbc.ModalFooter([
                    dbc.Button("Aplicar", id="btn-aplicar-canais", color="success"),
                    dbc.Button("Cancelar", id="btn-cancelar-canais", className="ms-2")
                ]),
            ],
            id="modal-alterar-canais",
            size="lg",
        ),
        
        # Modal para adicionar comentário
        dbc.Modal(
            [
                dbc.ModalHeader("Adicionar Comentário"),
                dbc.ModalBody([
                    dbc.Input(id="input-comentario", placeholder="Digite seu comentário...", type="text", className="mb-3"),
                    html.P("Ou selecione um comentário pré-definido:"),
                    dbc.ListGroup(id="lista-comentarios-predefinidos")
                ]),
                dbc.ModalFooter([
                    dbc.Button("Adicionar", id="btn-confirmar-comentario", color="success"),
                    dbc.Button("Cancelar", id="btn-cancelar-comentario", className="ms-2")
                ]),
            ],
            id="modal-adicionar-comentario",
            size="lg",
        )
    ], fluid=True, className="content-custom")
