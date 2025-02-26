from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from dotenv import load_dotenv
from auth import login_required, register_user, login_user, logout_user
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Verifica variáveis de ambiente necessárias
required_env_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'FLASK_SECRET_KEY']
for var in required_env_vars:
    value = os.getenv(var)
    if not value:
        raise ValueError(f"A variável de ambiente {var} não está definida")
    logger.info(f"{var} está configurada")

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Configuração para servir arquivos estáticos
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    try:
        if 'user' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Erro na rota /: {str(e)}")
        flash('Ocorreu um erro ao carregar a página', 'error')
        return render_template('error.html'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Por favor, preencha todos os campos', 'error')
                return render_template('login.html')
            
            success, message = login_user(email, password)
            if success:
                flash(message, 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(message, 'error')
                
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Erro na rota /login: {str(e)}")
        flash('Ocorreu um erro ao fazer login', 'error')
        return render_template('error.html'), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            department = request.form.get('department')
            
            if not all([email, password, name]):
                flash('Por favor, preencha todos os campos obrigatórios', 'error')
                return render_template('register.html')
            
            success, message = register_user(email, password, name, department)
            if success:
                flash(message, 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'error')
                
        return render_template('register.html')
    except Exception as e:
        logger.error(f"Erro na rota /register: {str(e)}")
        flash('Ocorreu um erro ao fazer o registro', 'error')
        return render_template('error.html'), 500

@app.route('/logout')
def logout():
    try:
        success, message = logout_user()
        flash(message, 'success' if success else 'error')
        return redirect(url_for('login'))
    except Exception as e:
        logger.error(f"Erro na rota /logout: {str(e)}")
        flash('Ocorreu um erro ao fazer logout', 'error')
        return render_template('error.html'), 500

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        logger.error(f"Erro na rota /dashboard: {str(e)}")
        flash('Ocorreu um erro ao carregar o dashboard', 'error')
        return render_template('error.html'), 500

@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    try:
        if request.method == 'POST':
            # TODO: Implementar criação de projeto
            pass
        return render_template('new_project.html')
    except Exception as e:
        logger.error(f"Erro na rota /project/new: {str(e)}")
        flash('Ocorreu um erro ao criar novo projeto', 'error')
        return render_template('error.html'), 500

@app.route('/project/<int:project_id>/tasks')
@login_required
def project_tasks(project_id):
    try:
        # TODO: Implementar visualização de tarefas
        return render_template('project_tasks.html', project_id=project_id)
    except Exception as e:
        logger.error(f"Erro na rota /project/{project_id}/tasks: {str(e)}")
        flash('Ocorreu um erro ao carregar as tarefas', 'error')
        return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
