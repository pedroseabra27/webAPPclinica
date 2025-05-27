import numpy as np
from datetime import datetime, timedelta

# Armazenamento de dados em memória (Temporário)
# Esta lista será populada a partir do banco de dados onde for necessário,
# ou os callbacks acessarão o banco diretamente.
pacientes_cadastrados_web = [] 
dados_plot_exame = [np.zeros(500) for _ in range(8)]
ptr_exame = 0

# Dados para gerenciamento de suítes
TOTAL_SUITES = 10
marcacoes_suites = {}  # Formato: {data_str: {suite_id: {paciente_id_db, hora_inicio, hora_fim, status}}}
# O 'paciente_id' aqui agora deve referenciar o ID do paciente no banco de dados.
