from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
from app import app
from app.models.data_store import pacientes_cadastrados_web

@app.callback(
    Output("lista-pacientes-div-pacientes", "children"),
    Output("div-feedback-cadastro-pacientes", "children"),
    Output("input-nome-completo", "value"),
    Output("input-cpf", "value"),
    Output("input-idade", "value"),
    Output("input-endereco", "value"),
    Output("input-telefone", "value"),
    Output("input-queixa", "value"),
    Input("btn-cadastrar-paciente", "n_clicks"),
    State("input-nome-completo", "value"),
    State("input-cpf", "value"),
    State("input-idade", "value"),
    State("input-endereco", "value"),
    State("input-telefone", "value"),
    State("input-queixa", "value"),
    prevent_initial_call=True
)
def callback_gerenciar_pacientes(
    n_clicks_botao, nome, cpf, idade_str, endereco, telefone, queixa
):
    mensagem_feedback = []
    ret_nome, ret_cpf, ret_idade_str, ret_endereco, ret_telefone, ret_queixa = nome, cpf, idade_str, endereco, telefone, queixa
    if n_clicks_botao:
        campos_obrigatorios_ok = nome and cpf and idade_str and endereco
        if campos_obrigatorios_ok:
            try:
                idade = int(idade_str)
                if idade < 0: raise ValueError("Idade negativa")
            except (ValueError, TypeError):
                mensagem_feedback = dbc.Alert("Erro: Idade inválida.", color="warning", dismissable=True, duration=5000)
                if not pacientes_cadastrados_web: elementos_lista = [html.P("Nenhum paciente cadastrado.")]
                else: elementos_lista = [dbc.ListGroup([dbc.ListGroupItem(f"{p['nome']} (CPF: {p['cpf']})") for p in pacientes_cadastrados_web])]
                return elementos_lista, mensagem_feedback, ret_nome, ret_cpf, ret_idade_str, ret_endereco, ret_telefone, ret_queixa
            if any(p['cpf'] == cpf for p in pacientes_cadastrados_web):
                mensagem_feedback = dbc.Alert(f"Erro: CPF '{cpf}' já cadastrado!", color="danger", dismissable=True, duration=5000)
            else:
                novo_paciente = {"nome": nome, "cpf": cpf, "idade": idade, "endereco": endereco, "telefone": telefone or "Não informado", "queixa": queixa or "Não informada"}
                pacientes_cadastrados_web.append(novo_paciente)
                mensagem_feedback = dbc.Alert(f"Paciente '{nome}' (CPF: {cpf}) cadastrado!", color="success", dismissable=True, duration=4000)
                ret_nome, ret_cpf, ret_idade_str, ret_endereco, ret_telefone, ret_queixa = "", "", None, "", "", ""
        else:
            mensagem_feedback = dbc.Alert("Erro: Nome, CPF, Idade e Endereço são obrigatórios!", color="warning", dismissable=True, duration=5000)
    if not pacientes_cadastrados_web: elementos_lista = [html.P("Nenhum paciente cadastrado.")]
    else: elementos_lista = [dbc.ListGroup([dbc.ListGroupItem(f"{p['nome']} (CPF: {p['cpf']})") for p in pacientes_cadastrados_web])]
    return elementos_lista, mensagem_feedback, ret_nome, ret_cpf, ret_idade_str, ret_endereco, ret_telefone, ret_queixa
