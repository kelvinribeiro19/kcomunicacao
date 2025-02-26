from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from auth import login_required, register_user, login_user, logout_user
import os

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        success, message = login_user(email, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(message, 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        department = request.form.get('department')
        
        success, message = register_user(email, password, name, department)
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    success, message = logout_user()
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/new-project', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        # TODO: Implementar criação de projeto
        pass
    return render_template('new_project.html')

@app.route('/project/<project_id>/tasks')
@login_required
def project_tasks(project_id):
    # TODO: Implementar visualização de tarefas do projeto
    return render_template('project_tasks.html', project_id=project_id)

if __name__ == '__main__':
    app.run(debug=True)
