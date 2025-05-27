import numpy as np
from datetime import datetime, timedelta

# Armazenamento de dados em memória (Temporário)
pacientes_cadastrados_web = []
dados_plot_exame = [np.zeros(500) for _ in range(8)]
ptr_exame = 0

# Dados para gerenciamento de suítes
TOTAL_SUITES = 10
marcacoes_suites = {}  # Formato: {data_str: {suite_id: {paciente_id, hora_inicio, hora_fim, status}}}

# Exemplo de inicialização (opcional, para teste)
# hoje_str = datetime.now().strftime("%Y-%m-%d")
# if hoje_str not in marcacoes_suites:
#     marcacoes_suites[hoje_str] = {}
# if pacientes_cadastrados_web and TOTAL_SUITES > 0:
#     # Exemplo: marcar o primeiro paciente na suíte 1 hoje
#     if 1 not in marcacoes_suites[hoje_str] and len(pacientes_cadastrados_web) > 0:
#          marcacoes_suites[hoje_str][1] = {
#             'paciente_id': 0,
#             'hora_inicio': '19:00',
#             'hora_fim': '07:00',
#             'status': 'agendado'
#         }
