from dash import html
import dash_bootstrap_components as dbc
# Importe as funções e o modelo necessários
from app.callbacks.pacientes_callbacks import get_all_pacientes_from_db # Reutilizar a função

def layout_pacientes():
    pacientes_do_banco = get_all_pacientes_from_db()
    if not pacientes_do_banco:
        elementos_lista_inicial = [html.P("Nenhum paciente cadastrado no banco de dados.")]
    else:
        elementos_lista_inicial = [dbc.ListGroup([dbc.ListGroupItem(f"{p.nome_completo} (CPF: {p.cpf})") for p in pacientes_do_banco])]

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Gerenciamento de Pacientes", className="my-4"))
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.H4("Cadastrar Novo Paciente"),
                dbc.Row([
                    dbc.Col(dbc.Label("Nome Completo:"), width=12),
                    dbc.Col(dbc.Input(id="input-nome-completo", placeholder="Digite o nome completo", type="text", className="mb-2"), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("CPF (somente números):"), width=6),
                    dbc.Col(dbc.Label("Idade:"), width=6)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Input(id="input-cpf", placeholder="Ex: 12345678900", type="text", className="mb-2"), width=6),
                    dbc.Col(dbc.Input(id="input-idade", placeholder="Ex: 35", type="number", min=0, step=1, className="mb-2"), width=6)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Endereço Completo:"), width=12),
                    dbc.Col(dbc.Input(id="input-endereco", placeholder="Ex: Rua Exemplo, 123, Bairro, Cidade - UF", type="text", className="mb-2"), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Telefone (opcional):"), width=12),
                    dbc.Col(dbc.Input(id="input-telefone", placeholder="Ex: (31) 99999-8888", type="text", className="mb-2"), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Queixa Principal (opcional):"), width=12),
                    dbc.Col(dbc.Textarea(id="input-queixa", placeholder="Descreva a queixa principal do paciente...", className="mb-2", style={'height': '100px'}), width=12)
                ]),
                dbc.Button("Cadastrar Paciente", id="btn-cadastrar-paciente", color="primary", className="w-100 mb-3 mt-2"),
                html.Div(id="div-feedback-cadastro-pacientes", children=[]),
            ], md=6, className="mb-4 mb-md-0"),

            dbc.Col([
                html.H4("Pacientes Cadastrados:", className="mt-md-0"),
                # A lista de pacientes agora é preenchida inicialmente aqui
                html.Div(id="lista-pacientes-div-pacientes", children=elementos_lista_inicial) 
            ], md=6)
        ])
    ], fluid=True, className="content-custom")
