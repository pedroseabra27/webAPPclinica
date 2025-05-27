from dash import html
import dash_bootstrap_components as dbc
from app import app

# Estilo da Sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem", # Largura da sidebar
    "padding": "2rem 1rem",
}

# Componente da Sidebar
sidebar = html.Div(
    [
        # Adiciona o logo aqui. Certifique-se que 'logo.png' está na pasta 'assets'
        html.Img(src=app.get_asset_url('logo.png'), className="sidebar-logo"),
        html.H2("PoliSoft Web", className="sidebar-title"), # Usando classe CSS
        html.Hr(),
        html.P(
            "Navegue pelas funcionalidades:", className="sidebar-lead-text" # Usando classe CSS
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Cadastro de Pacientes", href="/pacientes", active="exact"),
                dbc.NavLink("Visualizar Exames", href="/exames", active="exact"),
                dbc.NavLink("Gerenciamento de Suítes", href="/suites", active="exact"),  # Adicionado aqui
            ],
            vertical=True,
            pills=True,
            className="flex-grow-1" # Para garantir que os links ocupem o espaço
        ),
        html.Hr(className="mt-auto"), # Linha no final
        html.P("© 2024 Sua Clínica do Sono", className="text-center text-muted small") # Rodapé da sidebar
    ],
    style=SIDEBAR_STYLE,
    className="sidebar-custom d-flex flex-column", # Adiciona a classe CSS e classes flexbox para alinhar rodapé
)
