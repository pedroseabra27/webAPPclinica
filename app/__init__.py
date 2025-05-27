import dash
import dash_bootstrap_components as dbc

# Inicialização da aplicação Dash
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.LUX], 
                suppress_callback_exceptions=True,
                assets_folder='../assets')  # Aponta para a pasta assets no diretório raiz
