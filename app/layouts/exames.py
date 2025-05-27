from dash import html, dcc
import dash_bootstrap_components as dbc
from app.models.data_store import NUM_CANAIS_EXAME # Importar o número de canais

def layout_exames():
    # Gerar lista de nomes dos canais
    nomes_canais_itens = []
    for i in range(1, NUM_CANAIS_EXAME + 1):
        nomes_canais_itens.append(
            dbc.ListGroupItem(f"Canal {i}", className="py-1") # py-1 para diminuir altura
        )

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Visualização de Exames em Tempo Real (Simulado)", className="my-4"))
        ]),
        html.Hr(),
        # Botões de controle
        dbc.Row([
            dbc.Col([
                dbc.Button("Iniciar", id="btn-iniciar-exame", color="success", className="me-2"),
                dbc.Button("Pausar", id="btn-pausar-exame", color="warning"),
            ], width="auto", className="mb-3")
        ]),
        dbc.Row([
            # Coluna para a lista de nomes dos canais
            dbc.Col([
                html.H5("Canais", className="mb-2"),
                dbc.ListGroup(
                    nomes_canais_itens,
                    # Aplicar estilo para scroll se a lista for muito longa e altura fixa
                    style={"maxHeight": "80vh", "overflowY": "auto", "fontSize": "0.8rem"} 
                )
            ], md=2, className="pe-0"), # pe-0 para remover padding à direita

            # Coluna para o gráfico
            dbc.Col([
                dcc.Graph(
                    id='live-graph-exames',
                    animate=False, # Animação pode ser pesada com muitos canais
                    config={'displayModeBar': True, 'scrollZoom': True},
                    # Definir uma altura grande para o gráfico
                    style={'height': '80vh'} # Ajustar altura se necessário com os botões
                ),
                dcc.Interval(
                    id='interval-component-exames',
                    interval=200,  # em milissegundos (ajuste conforme necessário)
                    n_intervals=0,
                    disabled=True # Começa desabilitado
                )
            ], md=10, className="ps-2") # ps-2 para adicionar um pequeno padding à esquerda
        ], 
        # Remover gutters (espaçamento entre colunas) para juntar mais
        className="g-0" 
        ),
        dcc.Store(id='store-estado-exame', data={'rodando': False}) # Estado inicial: não rodando
    ], fluid=True, className="content-custom")
