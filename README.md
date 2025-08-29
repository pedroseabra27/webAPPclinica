# 🏥 ClinicaPolis - Polissonography Management System

A comprehensive web application for managing polissonography clinics, designed to handle real-time patient monitoring, exam scheduling, and data visualization for sleep studies and neurological assessments.

## 📋 About the Project

This application was developed as part of a Software Engineering project to create an efficient system for polissonography clinics. Polissonography is a comprehensive sleep study that records multiple physiological parameters simultaneously, including:

- **EEG (Electroencephalography)** - Brain activity monitoring
- **EOG (Electrooculography)** - Eye movement tracking
- **EMG (Electromyography)** - Muscle activity measurement
- **ECG (Electrocardiography)** - Heart rhythm monitoring
- **Respiratory parameters** - Breathing patterns and oxygen levels
- **Body position** - Sleep posture analysis

## 🎯 Key Features

- **📊 Real-time Data Visualization** - Live graphs for EEG and other physiological signals
- **👥 Patient Management** - Complete patient registration and history
- **📅 Exam Scheduling** - Efficient appointment management system
- **🔄 Live Monitoring** - Real-time exam progress tracking
- **📈 Data Analysis** - Advanced signal processing and analysis tools
- **🌐 Web Interface** - Modern, responsive dashboard built with Dash

## 🛠️ Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** Dash, Plotly, Bootstrap
- **Database:** SQLite (development) / PostgreSQL (production)
- **Deployment:** Render
- **Version Control:** Git, GitHub

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pedroseabra27/webAPPclinica.git
   cd webAPPclinica
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app_web.py
   ```

5. **Access the application:**
   - Open your browser and go to: `http://127.0.0.1:10000`
   - Default login credentials will be displayed in the terminal

## 📁 Project Structure

```
webAPPclinica/
├── app_web.py              # Main application entry point
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version specification
├── render.yaml            # Render deployment configuration
├── app/                   # Main application package
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   ├── callbacks/         # Dash callbacks for interactivity
│   │   ├── exames_callbacks.py
│   │   ├── pacientes_callbacks.py
│   │   ├── suites_callbacks.py
│   │   └── navigation.py
│   ├── layouts/           # Page layouts and UI components
│   │   ├── home.py
│   │   ├── pacientes.py
│   │   ├── exames.py
│   │   └── suites_layout.py
│   ├── models/            # Data models
│   │   ├── paciente_model.py
│   │   └── data_store.py
│   └── components/        # Reusable UI components
│       └── sidebar.py
├── assets/                # Static files (CSS, images)
│   └── style.css
└── utils/                 # Utility functions
    ├── constants.py
    └── __init__.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
DEBUG=False
HOST=0.0.0.0
PORT=10000
DATABASE_URL=sqlite:///clinicadata.db
```

### Database Setup
The application uses SQLite by default. For production, configure PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🌐 Deployment

### Render (Recommended)
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app_web.py`
4. Configure environment variables as above

### Local Production
```bash
gunicorn app_web:server --bind 0.0.0.0:10000
```

## 📊 Usage Guide

### For Clinic Staff
1. **Patient Registration:** Add new patients with complete medical history
2. **Exam Scheduling:** Book appointments and manage exam rooms
3. **Live Monitoring:** Track exam progress in real-time
4. **Data Analysis:** Review and analyze collected physiological data

### For Administrators
1. **System Configuration:** Manage clinic settings and parameters
2. **User Management:** Control access and permissions
3. **Reports:** Generate comprehensive reports and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Pedro Seabra**  
*Software Engineering Student at PUC Minas*  
Passionate about technology and development, constantly seeking to learn new tools and create innovative solutions.

*Estudante de Engenharia de Software na PUC Minas. Apaixonado por tecnologia e desenvolvimento, busco constantemente aprender novas ferramentas e criar soluções inovadoras.*

## 🙏 Acknowledgments

- PUC Minas for the academic support
- Open source community for the amazing tools and libraries
- Sleep medicine professionals for their valuable insights

---

**Note:** This is an academic project developed for educational purposes. For production use in real clinical environments, additional security measures and regulatory compliance would be required.ica - Deploy Guide

Aplicação web para gerenciamento de clínica com exames em tempo real.

## �‍💻 Author / Autor

**Pedro Seabra**  
*Software Engineering Student at PUC Minas*  
Passionate about technology and development, constantly seeking to learn new tools and create innovative solutions.

Estudante de Engenharia de Software na PUC Minas. Apaixonado por tecnologia e desenvolvimento, busco constantemente aprender novas ferramentas e criar soluções inovadoras.

## �🚀 Deploy no Render (Recomendado)

### Pré-requisitos:
- Conta no [Render](https://render.com)
- Repositório no GitHub (pode ser privado)

### Passos para Deploy:

1. **Acesse o Render:**
   - Vá para [render.com](https://render.com)
   - Clique em "New" → "Web Service"

2. **Conecte seu repositório:**
   - Selecione "Connect GitHub"
   - Autorize o acesso ao seu repositório
   - Selecione `webAPPclinica`

3. **Configure o serviço:**
   - **Name:** webapp-clinica
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app_web.py`

4. **Variáveis de ambiente:**
   ```
   DEBUG=False
   HOST=0.0.0.0
   PORT=10000
   ```

5. **Deploy:**
   - Clique em "Create Web Service"
   - O Render fará o deploy automaticamente
   - A URL será gerada automaticamente

### ✅ Vantagens do Render:
- ✅ Aceita repositórios privados
- ✅ Deploy automático a cada push
- ✅ Gratuito para projetos pessoais
- ✅ Suporte nativo a Python
- ✅ Interface simples e intuitiva

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
