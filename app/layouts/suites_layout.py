from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

def layout_suites():
    hoje_str = datetime.now().strftime("%Y-%m-%d")
    
    return dbc.Container([
        html.H2("Gerenciamento de Suítes", className="mb-4"),
        
        dbc.Row([
            # Coluna da Esquerda: Seleção de Data e Resumo
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Selecione a Data", className="card-title"),
                        dbc.Row([
                            dbc.Col(dbc.Button("◀", id="btn-data-anterior", color="primary", outline=True, size="sm"), width="auto", className="pe-1"),
                            dbc.Col(dcc.DatePickerSingle(
                                id='date-picker-suites',
                                date=hoje_str,
                                display_format='DD/MM/YYYY',
                                style={'width': '100%'}
                            ), className="px-0"),
                            dbc.Col(dbc.Button("▶", id="btn-data-proxima", color="primary", outline=True, size="sm"), width="auto", className="ps-1"),
                        ], align="center", justify="center"),
                    ])
                ], className="mb-3"),
                
                dbc.Card([
                    dbc.CardHeader("Resumo das Suítes"),
                    dbc.CardBody([
                        html.Div([dbc.Badge("Disponíveis:", color="success", className="me-1"), html.Span(id="suites-disponiveis")]),
                        html.Div([dbc.Badge("Ocupadas:", color="danger", className="me-1"), html.Span(id="suites-ocupadas")]),
                        html.Div([dbc.Badge("Data:", color="info", className="me-1"), html.Span(id="data-selecionada")]),
                    ])
                ])
            ], md=4),
            
            # Coluna da Direita: Pacientes Agendados
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Pacientes Agendados no Dia"),
                    dbc.CardBody(html.Div(id="lista-pacientes-agendados", style={"maxHeight": "300px", "overflowY": "auto"}))
                ])
            ], md=8),
        ], className="mb-4"),
        
        # Grade de Suítes
        html.H4("Status das Suítes", className="mt-4 mb-3"),
        html.Div(id="grid-suites"), # Será preenchido pelo callback
        
        # Modal para Marcar Suíte
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="modal-marcar-suite-titulo")),
            dbc.ModalBody([
                dbc.Label("Paciente:"),
                dcc.Dropdown(id="dropdown-paciente-suite", placeholder="Selecione um paciente", className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Hora de Início:"),
                        dbc.Input(id="input-hora-inicio", type="time", value="19:00")
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Hora de Fim:"),
                        dbc.Input(id="input-hora-fim", type="time", value="07:00")
                    ], width=6),
                ], className="mb-3"),
                html.Div(id="modal-data-selecionada-hidden", style={"display": "none"}), # Para passar a data
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancelar-marcar-suite", color="secondary"),
                dbc.Button("Confirmar Marcação", id="btn-confirmar-marcar-suite", color="primary")
            ])
        ], id="modal-marcar-suite", is_open=False),
        
        # Modal para Confirmar Remoção
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirmar Remoção")),
            dbc.ModalBody("Tem certeza que deseja remover esta marcação?"),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancelar-remover-marcacao", color="secondary"),
                dbc.Button("Confirmar Remoção", id="btn-confirmar-remover-marcacao", color="danger")
            ])
        ], id="modal-confirmar-remover-marcacao", is_open=False),
        
        dcc.Store(id="store-suite-selecionada-id"), # Armazena o ID da suíte clicada
        dcc.Store(id="store-data-selecionada-para-modal") # Armazena a data para o modal

    ], fluid=True, className="content-custom")
