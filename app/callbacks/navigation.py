from dash import Input, Output
from app import app
from app.layouts.home import layout_home
from app.layouts.pacientes import layout_pacientes
from app.layouts.exames import layout_exames
from app.layouts.error_page import layout_404
from app.layouts.suites_layout import layout_suites  # Corrija para suites_layout

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/pacientes":
        return layout_pacientes()
    elif pathname == "/exames":
        return layout_exames()
    elif pathname == "/suites":
        return layout_suites()
    elif pathname == "/":
        return layout_home()
    return layout_404(pathname)
