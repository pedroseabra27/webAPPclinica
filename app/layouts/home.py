from dash import html
import dash_bootstrap_components as dbc

def layout_home():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Bem-vindo ao Software da Clinica do Sono!", className="text-center my-4")),
        ]),
        dbc.Row([
            dbc.Col(html.P("Este é o sistema de gerenciamento de exames de polissonografia.", className="lead text-center")),
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Funcionalidades Principais", className="card-title"),
                        html.P("Utilize a barra lateral para navegar entre as seções:"),
                        html.Ul([
                            html.Li("Cadastro e gerenciamento de pacientes."),
                            html.Li("Agendamento e visualização de exames."),
                            html.Li("Análise de dados de polissonografia (em desenvolvimento).")
                        ])
                    ]),
                    className="mt-4"
                )
            )
        ])
    ], fluid=True, className="content-custom")
