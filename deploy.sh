#!/bin/bash
# Script de deploy para Heroku

echo "🚀 Iniciando deploy para Heroku..."

# Verificar se estamos em um repositório git
if [ ! -d ".git" ]; then
    echo "📝 Inicializando repositório Git..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Verificar se Heroku CLI está instalado
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI não está instalado. Instale em: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Solicitar nome do app
read -p "Digite o nome do seu app no Heroku: " app_name

# Criar app no Heroku
echo "📦 Criando app no Heroku..."
heroku create $app_name

# Configurar variáveis de ambiente
echo "⚙️  Configurando variáveis de ambiente..."
heroku config:set DEBUG=False --app $app_name
heroku config:set HOST=0.0.0.0 --app $app_name
heroku config:set PORT=8050 --app $app_name

# Deploy
echo "🚀 Fazendo deploy..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Abrir aplicação
echo "✅ Deploy concluído! Abrindo aplicação..."
heroku open --app $app_name

echo "🎉 Aplicação deployada com sucesso!"
echo "URL: https://$app_name.herokuapp.com"
