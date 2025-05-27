import numpy as np
from datetime import datetime, timedelta

# Armazenamento de dados em memória (Temporário)
# Esta lista será populada a partir do banco de dados onde for necessário,
# ou os callbacks acessarão o banco diretamente.
pacientes_cadastrados_web = [] 
NUM_CANAIS_EXAME = 32
PONTOS_GRAFICO_EXAME = 500 # Mantendo 500 pontos por canal para visualização
dados_plot_exame = [np.zeros(PONTOS_GRAFICO_EXAME) for _ in range(NUM_CANAIS_EXAME)]
ptr_exame = 0

# Dados para gerenciamento de suítes
TOTAL_SUITES = 10
marcacoes_suites = {}  # Formato: {data_str: {suite_id: {paciente_id_db, hora_inicio, hora_fim, status}}}
# O 'paciente_id' aqui agora deve referenciar o ID do paciente no banco de dados.
