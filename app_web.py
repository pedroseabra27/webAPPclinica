# app_web.py - Ponto de entrada principal da aplicação
from dash import html, dcc
from app import app
from app.components.sidebar import sidebar
from app.utils.constants import CONTENT_STYLE

# Importar todos os callbacks para registrá-los
from app.callbacks import navigation, pacientes_callbacks, exames_callbacks

# Layout Principal da Aplicação
content_wrapper = html.Div(id="page-content")  # Wrapper para o conteúdo principal

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    sidebar,
    # Aplicando a classe CSS ao wrapper do conteúdo
    html.Div(content_wrapper, style=CONTENT_STYLE, className="content-custom-wrapper")
])

# --- Roda o Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
