from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
from sqlalchemy.exc import IntegrityError
from app import app
from app.models.paciente_model import Paciente
from app.database import SessionLocal
import logging # Adicionar para logging

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

def create_paciente_in_db(nome, cpf, idade, endereco, telefone, queixa):
    db = SessionLocal()
    try:
        logger.info(f"Tentando criar paciente: {nome}, CPF: {cpf}")
        novo_paciente = Paciente(
            nome_completo=nome,
            cpf=cpf,
            idade=idade,
            endereco=endereco,
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
        logger.info(f"Botão 'Cadastrar Paciente' clicado. Nome: {nome}, CPF: {cpf}")
        campos_obrigatorios_ok = nome and cpf and idade_str and endereco
        if campos_obrigatorios_ok:
            try:
                idade = int(idade_str)
                if idade < 0: raise ValueError("Idade negativa")
            except (ValueError, TypeError):
                logger.warning(f"Idade inválida fornecida: {idade_str}")
                mensagem_feedback = dbc.Alert("Erro: Idade inválida.", color="warning", dismissable=True, duration=5000)
            else:
                resultado_criacao, sucesso_ou_cpf_duplicado = create_paciente_in_db(nome, cpf, idade, endereco, telefone, queixa)
                if resultado_criacao and sucesso_ou_cpf_duplicado is True: # Sucesso
                    logger.info(f"Paciente '{nome}' cadastrado com sucesso no DB.")
                    mensagem_feedback = dbc.Alert(f"Paciente '{nome}' (CPF: {cpf}) cadastrado com sucesso no banco de dados!", color="success", dismissable=True, duration=4000)
                    ret_nome, ret_cpf, ret_idade_str, ret_endereco, ret_telefone, ret_queixa = "", "", None, "", "", ""
                elif sucesso_ou_cpf_duplicado is False: # CPF Duplicado
                    logger.warning(f"Falha ao criar paciente '{nome}' no DB. CPF duplicado.")
                    mensagem_feedback = dbc.Alert(f"Erro: CPF '{cpf}' já cadastrado!", color="danger", dismissable=True, duration=5000)
                else: # Outro erro
                    logger.error(f"Falha ao criar paciente '{nome}' no DB devido a um erro inesperado.")
                    mensagem_feedback = dbc.Alert(f"Erro inesperado ao cadastrar paciente '{nome}'. Consulte os logs.", color="danger", dismissable=True, duration=5000)
        else:
            logger.warning("Campos obrigatórios não preenchidos.")
            mensagem_feedback = dbc.Alert("Erro: Nome, CPF, Idade e Endereço são obrigatórios!", color="warning", dismissable=True, duration=5000)

    pacientes_do_banco = get_all_pacientes_from_db()
    if not pacientes_do_banco:
        elementos_lista = [html.P("Nenhum paciente cadastrado no banco de dados.")]
    else:
        elementos_lista = [dbc.ListGroup([dbc.ListGroupItem(f"{p.nome_completo} (CPF: {p.cpf})") for p in pacientes_do_banco])]
    
    return elementos_lista, mensagem_feedback, ret_nome, ret_cpf, ret_idade_str, ret_endereco, ret_telefone, ret_queixa
