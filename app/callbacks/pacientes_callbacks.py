from dash import Input, Output, State, html, callback_context, ALL, no_update
import dash_bootstrap_components as dbc
from sqlalchemy.exc import IntegrityError
from app import app
from app.models.paciente_model import Paciente
from app.database import SessionLocal
import logging

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_pacientes_from_db():
    db = SessionLocal()
    try:
        logger.info("Buscando todos os pacientes do banco de dados.")
        pacientes = db.query(Paciente).all()
        logger.info(f"Encontrados {len(pacientes)} pacientes.")
        return pacientes
    finally:
        db.close()

def create_paciente_in_db(nome, cpf, idade, endereco_completo, telefone, queixa): # Parâmetro 'endereco' mudou para 'endereco_completo'
    db = SessionLocal()
    try:
        logger.info(f"Tentando criar paciente: {nome}, CPF: {cpf}")
        novo_paciente = Paciente(
            nome_completo=nome,
            cpf=cpf,
            idade=idade,
            endereco=endereco_completo, # Usar a string de endereço completa
            telefone=telefone or "Não informado",
            queixa_principal=queixa or "Não informada"
        )
        db.add(novo_paciente)
        db.commit()
        db.refresh(novo_paciente)
        logger.info(f"Paciente ID {novo_paciente.id} criado com sucesso.")
        return novo_paciente, True # Retorna o paciente e True para sucesso
    except IntegrityError as e: 
        db.rollback()
        logger.error(f"Erro de integridade ao criar paciente (CPF duplicado?): {cpf}. Erro: {e}")
        return None, False # Retorna None e False para CPF duplicado
    except Exception as e:
        db.rollback()
        logger.error(f"Erro inesperado ao criar paciente: {nome}, CPF: {cpf}. Erro: {e}")
        return None, None # Retorna None e None para outros erros
    finally:
        db.close()

def delete_paciente_from_db(paciente_id: int):
    db = SessionLocal()
    try:
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if paciente:
            logger.info(f"Tentando excluir paciente ID: {paciente_id}, Nome: {paciente.nome_completo}")
            db.delete(paciente)
            db.commit()
            logger.info(f"Paciente ID: {paciente_id} excluído com sucesso.")
            return True, f"Paciente '{paciente.nome_completo}' excluído com sucesso."
        else:
            logger.warning(f"Tentativa de excluir paciente ID: {paciente_id} não encontrado.")
            return False, "Paciente não encontrado para exclusão."
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao excluir paciente ID: {paciente_id}. Erro: {e}")
        return False, f"Erro ao excluir paciente: {e}"
    finally:
        db.close()

@app.callback(
    Output("lista-pacientes-div-pacientes", "children"),
    Output("div-feedback-cadastro-pacientes", "children"),
    Output("input-nome-completo", "value"),
    Output("input-cpf", "value"),
    Output("input-idade", "value"),
    # Outputs para limpar os novos campos de endereço
    Output("input-rua", "value"),
    Output("input-numero-casa", "value"),
    Output("input-complemento", "value"),
    Output("input-bairro", "value"),
    Output("input-cidade", "value"),
    Output("input-estado", "value"),
    Output("input-cep", "value"),
    Output("input-telefone", "value"),
    Output("input-queixa", "value"),
    Input("btn-cadastrar-paciente", "n_clicks"),
    Input("btn-confirmar-excluir-paciente", "n_clicks"),
    State("input-nome-completo", "value"),
    State("input-cpf", "value"),
    State("input-idade", "value"),
    # States para os novos campos de endereço
    State("input-rua", "value"),
    State("input-numero-casa", "value"),
    State("input-complemento", "value"),
    State("input-bairro", "value"),
    State("input-cidade", "value"),
    State("input-estado", "value"),
    State("input-cep", "value"),
    State("input-telefone", "value"),
    State("input-queixa", "value"),
    prevent_initial_call=True
)
def callback_gerenciar_pacientes(
    n_clicks_cadastrar, n_clicks_confirmar_excluir,
    nome, cpf, idade_str, 
    rua, numero_casa, complemento, bairro, cidade, estado, cep, # Novos parâmetros de endereço
    telefone, queixa
):
    mensagem_feedback = []
    # Manter valores nos campos em caso de erro
    ret_nome, ret_cpf, ret_idade_str = nome, cpf, idade_str
    ret_rua, ret_numero_casa, ret_complemento = rua, numero_casa, complemento
    ret_bairro, ret_cidade, ret_estado, ret_cep = bairro, cidade, estado, cep
    ret_telefone, ret_queixa = telefone, queixa
    
    ctx = callback_context
    triggered_id = ctx.triggered_id if ctx.triggered_id else "No trigger"

    if triggered_id == "btn-cadastrar-paciente":
        logger.info(f"Botão 'Cadastrar Paciente' clicado. Nome: {nome}, CPF: {cpf}")
        
        # Construir a string de endereço completo
        # Apenas adiciona partes que foram preenchidas
        partes_endereco = []
        if rua: partes_endereco.append(rua)
        if numero_casa: partes_endereco.append(f"Nº {numero_casa}")
        if complemento: partes_endereco.append(f"Compl: {complemento}")
        if bairro: partes_endereco.append(f"Bairro: {bairro}")
        if cidade: partes_endereco.append(cidade)
        if estado: partes_endereco.append(f"- {estado.upper()}")
        if cep: partes_endereco.append(f"CEP: {cep}")
        endereco_completo = ", ".join(filter(None, partes_endereco))

        # Validação de campos obrigatórios (nome, cpf, idade e pelo menos a rua do endereço)
        campos_obrigatorios_ok = nome and cpf and idade_str and rua 

        if campos_obrigatorios_ok:
            try:
                idade = int(idade_str)
                if idade < 0: raise ValueError("Idade negativa")
            except (ValueError, TypeError):
                logger.warning(f"Idade inválida fornecida: {idade_str}")
                mensagem_feedback = dbc.Alert("Erro: Idade inválida.", color="warning", dismissable=True, duration=5000)
            else:
                # Passar endereco_completo para a função de criação
                resultado_criacao, sucesso_ou_cpf_duplicado = create_paciente_in_db(nome, cpf, idade, endereco_completo, telefone, queixa)
                if resultado_criacao and sucesso_ou_cpf_duplicado is True: 
                    logger.info(f"Paciente '{nome}' cadastrado com sucesso no DB.")
                    mensagem_feedback = dbc.Alert(f"Paciente '{nome}' (CPF: {cpf}) cadastrado com sucesso!", color="success", dismissable=True, duration=4000)
                    # Limpar todos os campos
                    ret_nome, ret_cpf, ret_idade_str = "", "", None
                    ret_rua, ret_numero_casa, ret_complemento = "", "", ""
                    ret_bairro, ret_cidade, ret_estado, ret_cep = "", "", "", ""
                    ret_telefone, ret_queixa = "", ""
                elif sucesso_ou_cpf_duplicado is False: 
                    logger.warning(f"Falha ao criar paciente '{nome}' no DB. CPF duplicado.")
                    mensagem_feedback = dbc.Alert(f"Erro: CPF '{cpf}' já cadastrado!", color="danger", dismissable=True, duration=5000)
                else: 
                    logger.error(f"Falha ao criar paciente '{nome}' no DB devido a um erro inesperado.")
                    mensagem_feedback = dbc.Alert(f"Erro inesperado ao cadastrar paciente '{nome}'.", color="danger", dismissable=True, duration=5000)
        else:
            logger.warning("Campos obrigatórios não preenchidos (Nome, CPF, Idade, Rua).")
            mensagem_feedback = dbc.Alert("Erro: Nome, CPF, Idade e Rua são obrigatórios!", color="warning", dismissable=True, duration=5000)
    
    # A lógica de feedback para exclusão será tratada pelo callback do modal de exclusão,
    # mas a lista de pacientes precisa ser atualizada aqui se o botão de confirmar exclusão foi o gatilho.
    # Se a exclusão foi confirmada, o feedback já foi dado pelo callback do modal.
    # Apenas atualizamos a lista.

    pacientes_do_banco = get_all_pacientes_from_db()
    elementos_lista = []
    if not pacientes_do_banco:
        elementos_lista = [html.P("Nenhum paciente cadastrado no banco de dados.")]
    else:
        for p in pacientes_do_banco:
            item = dbc.ListGroupItem(
                [
                    html.Div(f"{p.nome_completo} (CPF: {p.cpf})", style={"flexGrow": 1}),
                    dbc.Button("Excluir", id={"type": "btn-excluir-paciente", "index": p.id}, color="danger", size="sm", className="ms-2")
                ],
                className="d-flex justify-content-between align-items-center"
            )
            elementos_lista.append(item)
        elementos_lista = [dbc.ListGroup(elementos_lista)]
    
    # Se o cadastro foi o gatilho, retorna os campos limpos ou não.
    # Se a exclusão foi o gatilho, não queremos limpar os campos de cadastro.
    if triggered_id == "btn-cadastrar-paciente":
        return (elementos_lista, mensagem_feedback, 
                ret_nome, ret_cpf, ret_idade_str, 
                ret_rua, ret_numero_casa, ret_complemento, ret_bairro, ret_cidade, ret_estado, ret_cep,
                ret_telefone, ret_queixa)
    else: # Se foi btn-confirmar-excluir-paciente ou carregamento inicial (que não deveria acontecer aqui com prevent_initial_call=True)
        # Não limpar campos de cadastro, e o feedback de exclusão é tratado em outro callback
        return (elementos_lista, no_update, 
                no_update, no_update, no_update, 
                no_update, no_update, no_update, no_update, no_update, no_update, no_update,
                no_update, no_update)

# Callback para abrir o modal de confirmação de exclusão
@app.callback(
    Output("modal-confirmar-excluir-paciente", "is_open"),
    Output("modal-excluir-paciente-body", "children"),
    Output("store-paciente-para-excluir-id", "data"),
    Input({"type": "btn-excluir-paciente", "index": ALL}, "n_clicks"),
    State("modal-confirmar-excluir-paciente", "is_open"),
    prevent_initial_call=True
)
def abrir_modal_excluir_paciente(n_clicks_excluir, is_open):
    ctx = callback_context
    if not ctx.triggered_id or not any(n_clicks_excluir):
        return is_open, no_update, no_update

    triggered_prop_id = ctx.triggered_id
    paciente_id_para_excluir = triggered_prop_id["index"]

    db = SessionLocal()
    try:
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id_para_excluir).first()
        if paciente:
            modal_body_text = f"Tem certeza que deseja excluir o paciente '{paciente.nome_completo}' (CPF: {paciente.cpf})?"
            return True, modal_body_text, paciente_id_para_excluir
        else:
            # Paciente não encontrado, não deveria acontecer se o botão existe
            return False, "Erro: Paciente não encontrado.", no_update 
    finally:
        db.close()
    
    return is_open, no_update, no_update # Fallback

# Callback para lidar com a exclusão (confirmar ou cancelar)
@app.callback(
    Output("modal-confirmar-excluir-paciente", "is_open", allow_duplicate=True),
    Output("div-feedback-cadastro-pacientes", "children", allow_duplicate=True), # Usar o mesmo div de feedback
    Input("btn-confirmar-excluir-paciente", "n_clicks"),
    Input("btn-cancelar-excluir-paciente", "n_clicks"),
    State("store-paciente-para-excluir-id", "data"),
    prevent_initial_call=True
)
def lidar_com_exclusao_paciente(n_confirmar, n_cancelar, paciente_id):
    ctx = callback_context
    triggered_id = ctx.triggered_id

    if triggered_id == "btn-confirmar-excluir-paciente" and paciente_id is not None:
        sucesso, mensagem = delete_paciente_from_db(paciente_id)
        if sucesso:
            alert_color = "success"
        else:
            alert_color = "danger"
        feedback_msg = dbc.Alert(mensagem, color=alert_color, dismissable=True, duration=5000)
        return False, feedback_msg # Fecha modal e mostra feedback
    
    if triggered_id == "btn-cancelar-excluir-paciente":
        return False, no_update # Fecha modal, sem feedback

    return no_update, no_update
