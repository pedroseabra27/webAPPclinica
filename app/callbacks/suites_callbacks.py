from dash import Input, Output, State, html, callback_context, ALL, no_update, dash
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from app import app
from app.models.data_store import pacientes_cadastrados_web, marcacoes_suites, TOTAL_SUITES

# Callback para atualizar a visualização das suítes e resumo
@app.callback(
    Output("grid-suites", "children"),
    Output("suites-disponiveis", "children"),
    Output("suites-ocupadas", "children"),
    Output("data-selecionada", "children"),
    Output("lista-pacientes-agendados", "children"),
    Input("date-picker-suites", "date"),
    Input("btn-confirmar-marcar-suite", "n_clicks"), # Para re-renderizar após marcar
    Input("btn-confirmar-remover-marcacao", "n_clicks") # Para re-renderizar após remover
)
def renderizar_pagina_suites(data_selecionada_str, n_confirm_marcar, n_confirm_remover):
    if data_selecionada_str is None:
        return no_update, no_update, no_update, no_update, no_update

    data_obj = datetime.strptime(data_selecionada_str, "%Y-%m-%d")
    data_formatada_usuario = data_obj.strftime("%d/%m/%Y")

    if data_selecionada_str not in marcacoes_suites:
        marcacoes_suites[data_selecionada_str] = {}

    marcacoes_do_dia = marcacoes_suites[data_selecionada_str]
    
    cards_suites = []
    suites_ocupadas_count = 0

    for suite_id in range(1, TOTAL_SUITES + 1):
        ocupada = suite_id in marcacoes_do_dia
        card_body_content = []
        header_class = "bg-success text-white" # Disponível por padrão

        if ocupada:
            suites_ocupadas_count += 1
            header_class = "bg-danger text-white" # Ocupada
            info_marcacao = marcacoes_do_dia[suite_id]
            paciente_id = info_marcacao['paciente_id']
            paciente_nome = "Desconhecido"
            if 0 <= paciente_id < len(pacientes_cadastrados_web):
                paciente_nome = pacientes_cadastrados_web[paciente_id]['nome']
            
            card_body_content = [
                html.H5(paciente_nome, className="card-title"),
                html.P(f"Horário: {info_marcacao['hora_inicio']} - {info_marcacao['hora_fim']}"),
                dbc.Button("Remover Marcação", id={"type": "btn-remover-suite", "index": suite_id}, color="warning", size="sm")
            ]
        else:
            card_body_content = [
                html.H5("Disponível", className="card-title"),
                dbc.Button("Marcar Exame", id={"type": "btn-marcar-suite", "index": suite_id}, color="primary", size="sm")
            ]
        
        card = dbc.Col(
            dbc.Card([
                dbc.CardHeader(f"Suíte {suite_id}", className=header_class),
                dbc.CardBody(card_body_content)
            ]), 
            width=12, md=6, lg=4, className="mb-3" # Ajuste de colunas para responsividade
        )
        cards_suites.append(card)
    
    grid_layout = dbc.Row(cards_suites)
    suites_disponiveis_count = TOTAL_SUITES - suites_ocupadas_count

    # Atualizar lista de pacientes agendados
    lista_pacientes_agendados_html = []
    if marcacoes_do_dia:
        for suite_id, info in marcacoes_do_dia.items():
            paciente_id = info['paciente_id']
            paciente_nome = "Desconhecido"
            if 0 <= paciente_id < len(pacientes_cadastrados_web):
                paciente_nome = pacientes_cadastrados_web[paciente_id]['nome']
            lista_pacientes_agendados_html.append(
                dbc.ListGroupItem(f"Suíte {suite_id}: {paciente_nome} ({info['hora_inicio']} - {info['hora_fim']})")
            )
    else:
        lista_pacientes_agendados_html = [html.P("Nenhum paciente agendado para esta data.", className="text-muted")]

    return grid_layout, str(suites_disponiveis_count), str(suites_ocupadas_count), data_formatada_usuario, lista_pacientes_agendados_html

# Callback para navegar entre datas
@app.callback(
    Output("date-picker-suites", "date"),
    Input("btn-data-anterior", "n_clicks"),
    Input("btn-data-proxima", "n_clicks"),
    State("date-picker-suites", "date"),
    prevent_initial_call=True
)
def navegar_datas(n_anterior, n_proxima, data_atual_str):
    if data_atual_str is None:
        return no_update
    
    ctx = callback_context
    if not ctx.triggered_id:
        return no_update

    data_atual_obj = datetime.strptime(data_atual_str, "%Y-%m-%d")
    
    if ctx.triggered_id == "btn-data-anterior":
        nova_data_obj = data_atual_obj - timedelta(days=1)
    elif ctx.triggered_id == "btn-data-proxima":
        nova_data_obj = data_atual_obj + timedelta(days=1)
    else:
        return no_update
        
    return nova_data_obj.strftime("%Y-%m-%d")

# Callback para abrir o modal de marcar suíte e preencher dados
@app.callback(
    Output("modal-marcar-suite", "is_open"),
    Output("modal-marcar-suite-titulo", "children"),
    Output("dropdown-paciente-suite", "options"),
    Output("store-suite-selecionada-id", "data"),
    Output("store-data-selecionada-para-modal", "data"), # Para passar a data correta
    Output("dropdown-paciente-suite", "value"), # Limpar seleção anterior
    Input({"type": "btn-marcar-suite", "index": ALL}, "n_clicks"),
    State("date-picker-suites", "date"),
    prevent_initial_call=True
)
def abrir_modal_marcar_suite(n_clicks_marcar, data_selecionada_str):
    ctx = callback_context
    if not ctx.triggered_id or not any(n_clicks_marcar): # Verifica se algum botão foi clicado
        return False, no_update, no_update, no_update, no_update, None

    triggered_prop_id = ctx.triggered_id
    suite_id_clicada = triggered_prop_id["index"]
    
    opcoes_pacientes = [{"label": p['nome'], "value": idx} for idx, p in enumerate(pacientes_cadastrados_web)]
    
    titulo_modal = f"Marcar Suíte {suite_id_clicada} para {datetime.strptime(data_selecionada_str, '%Y-%m-%d').strftime('%d/%m/%Y')}"

    return True, titulo_modal, opcoes_pacientes, suite_id_clicada, data_selecionada_str, None


# Callback para fechar o modal de marcar suíte (botão Cancelar)
@app.callback(
    Output("modal-marcar-suite", "is_open", allow_duplicate=True),
    Input("btn-cancelar-marcar-suite", "n_clicks"),
    prevent_initial_call=True
)
def fechar_modal_marcar_suite_cancelar(n_clicks):
    if n_clicks:
        return False
    return no_update

# Callback para confirmar a marcação de suíte
@app.callback(
    Output("modal-marcar-suite", "is_open", allow_duplicate=True),
    # Outputs adicionais para feedback podem ser adicionados aqui
    Input("btn-confirmar-marcar-suite", "n_clicks"),
    State("store-suite-selecionada-id", "data"),
    State("store-data-selecionada-para-modal", "data"), # Usar a data armazenada
    State("dropdown-paciente-suite", "value"),
    State("input-hora-inicio", "value"),
    State("input-hora-fim", "value"),
    prevent_initial_call=True
)
def confirmar_marcacao_suite_action(n_clicks, suite_id, data_selecionada_str, paciente_id, hora_inicio, hora_fim):
    if not n_clicks or paciente_id is None or suite_id is None or data_selecionada_str is None:
        # Adicionar um alerta aqui seria bom se os campos não forem preenchidos
        return no_update 

    if data_selecionada_str not in marcacoes_suites:
        marcacoes_suites[data_selecionada_str] = {}
    
    # Verificar se a suíte já está ocupada (embora o botão "Marcar Exame" não devesse aparecer)
    if suite_id in marcacoes_suites[data_selecionada_str]:
        # Lógica de erro/aviso
        return True # Mantém o modal aberto para o usuário ver o erro (precisaria de um componente de alerta no modal)

    marcacoes_suites[data_selecionada_str][suite_id] = {
        'paciente_id': paciente_id,
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'status': 'agendado'
    }
    return False # Fecha o modal


# Callback para abrir o modal de remover marcação
@app.callback(
    Output("modal-confirmar-remover-marcacao", "is_open"),
    Output("store-suite-selecionada-id", "data", allow_duplicate=True), # Para saber qual remover
    Output("store-data-selecionada-para-modal", "data", allow_duplicate=True),
    Input({"type": "btn-remover-suite", "index": ALL}, "n_clicks"),
    State("date-picker-suites", "date"),
    prevent_initial_call=True
)
def abrir_modal_remover_marcacao(n_clicks_remover, data_selecionada_str):
    ctx = callback_context
    if not ctx.triggered_id or not any(n_clicks_remover):
        return False, no_update, no_update

    triggered_prop_id = ctx.triggered_id
    suite_id_clicada = triggered_prop_id["index"]
    return True, suite_id_clicada, data_selecionada_str

# Callback para fechar o modal de remover marcação (botão Cancelar)
@app.callback(
    Output("modal-confirmar-remover-marcacao", "is_open", allow_duplicate=True),
    Input("btn-cancelar-remover-marcacao", "n_clicks"),
    prevent_initial_call=True
)
def fechar_modal_remover_cancelar(n_clicks):
    if n_clicks:
        return False
    return no_update

# Callback para confirmar a remoção da marcação
@app.callback(
    Output("modal-confirmar-remover-marcacao", "is_open", allow_duplicate=True),
    # Outputs adicionais para feedback podem ser adicionados aqui
    Input("btn-confirmar-remover-marcacao", "n_clicks"),
    State("store-suite-selecionada-id", "data"),
    State("store-data-selecionada-para-modal", "data"),
    prevent_initial_call=True
)
def confirmar_remocao_marcacao_action(n_clicks, suite_id, data_selecionada_str):
    if not n_clicks or suite_id is None or data_selecionada_str is None:
        return no_update

    if data_selecionada_str in marcacoes_suites and suite_id in marcacoes_suites[data_selecionada_str]:
        del marcacoes_suites[data_selecionada_str][suite_id]
    
    return False # Fecha o modal
