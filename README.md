# WebApp Clínica - Deploy Guide

Aplicação web para gerenciamento de clínica com exames em tempo real.

## 🚀 Opções de Deploy

### 1. Heroku (Recomendado)

#### Pré-requisitos:
- Conta no [Heroku](https://heroku.com)
- Git instalado
- Heroku CLI instalado

#### Passos:
1. **Criar app no Heroku:**
   ```bash
   heroku create nome-do-seu-app
   ```

2. **Configurar variáveis de ambiente:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set HOST=0.0.0.0
   heroku config:set PORT=8050
   ```

3. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

4. **Abrir aplicação:**
   ```bash
   heroku open
   ```

### 2. Railway (Mais Fácil)

#### Pré-requisitos:
- Conta no [Railway](https://railway.app)

#### Passos:
1. **Conectar repositório:**
   - Faça upload do código para GitHub
   - Conecte o repositório no Railway

2. **Deploy automático:**
   - Railway detectará automaticamente como app Python
   - As configurações estão no `railway.toml`

3. **Configurar variáveis de ambiente:**
   ```
   DEBUG=False
   HOST=0.0.0.0
   PORT=8050
   ```

4. **Deploy:**
   - Railway fará o deploy automaticamente
   - A URL será gerada automaticamente

### 3. Render

#### Pré-requisitos:
- Conta no [Render](https://render.com)

#### Passos:
1. Conectar repositório GitHub
2. Selecionar "Web Service"
3. Configurar:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app_web:server --bind 0.0.0.0:$PORT`
4. Configurar variáveis de ambiente
5. Deploy

### 4. Vercel (Não recomendado para este projeto)

Vercel é otimizado para aplicações serverless e não é ideal para aplicações Dash que precisam manter estado em tempo real. Use Heroku, Railway ou Render.

## 📋 Estrutura do Projeto

```
webAPPclinica/
├── app_web.py              # Ponto de entrada
├── requirements.txt        # Dependências
├── Procfile               # Configuração Heroku
├── runtime.txt           # Versão Python
├── .env.example          # Exemplo variáveis ambiente
├── app/
│   ├── callbacks/        # Callbacks Dash
│   ├── layouts/          # Layouts das páginas
│   ├── models/           # Modelos de dados
│   └── components/       # Componentes reutilizáveis
└── assets/
    └── style.css         # Estilos CSS
```

## 🔧 Configuração Local

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar aplicação:**
   ```bash
   python app_web.py
   ```

3. **Acessar:** http://127.0.0.1:8050

## 🌐 Próximos Passos

- [ ] Migrar para HTML/CSS/JS frontend (opcional)
- [ ] Integrar dados reais do Raspberry Pi
- [ ] Configurar banco PostgreSQL para produção
- [ ] Implementar autenticação de usuários
