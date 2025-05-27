from dash import html
import dash_bootstrap_components as dbc

def layout_404(pathname):
    return dbc.Container([
        html.H1("404: Página não encontrada", className="text-danger"),
        html.Hr(),
        html.P(f"O caminho '{pathname}' não foi reconhecido.")
    ], className="content-custom text-center py-5")
