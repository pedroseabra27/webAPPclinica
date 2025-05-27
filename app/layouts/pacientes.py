from dash import html, dcc # Adicionar dcc para o Store
import dash_bootstrap_components as dbc
# Importe as funções e o modelo necessários
from app.callbacks.pacientes_callbacks import get_all_pacientes_from_db # Reutilizar a função

def layout_pacientes():
    pacientes_do_banco = get_all_pacientes_from_db()
    elementos_lista_inicial = []
    if not pacientes_do_banco:
        elementos_lista_inicial = [html.P("Nenhum paciente cadastrado no banco de dados.")]
    else:
        for p in pacientes_do_banco:
            item = dbc.ListGroupItem(
                [
                    html.Div(f"{p.nome_completo} (CPF: {p.cpf})", style={"flexGrow": 1}),
                    dbc.Button("Excluir", id={"type": "btn-excluir-paciente", "index": p.id}, color="danger", size="sm", className="ms-2")
                ], 
                className="d-flex justify-content-between align-items-center"
            )
            elementos_lista_inicial.append(item)
        elementos_lista_inicial = [dbc.ListGroup(elementos_lista_inicial)]


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
                    # Modificação no campo CPF
                    dbc.Col(dbc.Input(id="input-cpf", placeholder="", type="text", maxLength=11, className="mb-2"), width=6),
                    dbc.Col(dbc.Input(id="input-idade", placeholder="Ex: 35", type="number", min=0, step=1, className="mb-2"), width=6)
                ]),
                
                # Subdivisão do Endereço
                dbc.Label("Endereço:"),
                dbc.Row([
                    dbc.Col(dbc.Input(id="input-rua", placeholder="Rua/Avenida", type="text", className="mb-2"), md=7),
                    dbc.Col(dbc.Input(id="input-numero-casa", placeholder="Nº", type="text", className="mb-2"), md=2),
                    dbc.Col(dbc.Input(id="input-complemento", placeholder="Compl.", type="text", className="mb-2"), md=3)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Input(id="input-bairro", placeholder="Bairro", type="text", className="mb-2"), md=6),
                    dbc.Col(dbc.Input(id="input-cidade", placeholder="Cidade", type="text", className="mb-2"), md=4),
                    dbc.Col(dbc.Input(id="input-estado", placeholder="UF", type="text", maxLength=2, className="mb-2"), md=2)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Input(id="input-cep", placeholder="CEP (somente números)", type="text", maxLength=8, className="mb-2"), md=6)
                ]),

                dbc.Row([
                    dbc.Col(dbc.Label("Telefone (opcional):"), width=12),
                    dbc.Col(dbc.Input(id="input-telefone", placeholder="", type="text", className="mb-2"), width=12)
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
                html.Div(id="lista-pacientes-div-pacientes", children=elementos_lista_inicial) 
            ], md=6)
        ]),
        # Modal de confirmação de exclusão
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclusão")),
            dbc.ModalBody(id="modal-excluir-paciente-body"),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancelar-excluir-paciente", color="secondary"),
                dbc.Button("Confirmar Exclusão", id="btn-confirmar-excluir-paciente", color="danger")
            ])
        ], id="modal-confirmar-excluir-paciente", is_open=False),
        dcc.Store(id="store-paciente-para-excluir-id") # Para guardar o ID do paciente a ser excluído
    ], fluid=True, className="content-custom")
