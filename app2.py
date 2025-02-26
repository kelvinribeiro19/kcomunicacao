from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Inicializa o cliente Supabase
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        
        # Cria um novo usuário no Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": data['email'],
            "password": data['password']
        })
        
        # Se o usuário foi criado com sucesso, adiciona os dados adicionais
        if auth_response.user:
            user_data = {
                "id": auth_response.user.id,
                "name": data['name'],
                "email": data['email'],
                "department": data['department'],
                "role": data['role']
            }
            
            # Insere os dados do usuário na tabela profiles
            supabase.table('profiles').insert(user_data).execute()
            
            return jsonify({
                "success": True,
                "message": "Usuário criado com sucesso!"
            })
            
    except Exception as e:
        print(f"Erro no registro: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Erro ao criar usuário. Por favor, tente novamente."
        }), 400

@app.route('/login', methods=['POST'])
def login_post():
    try:
        data = request.form
        
        # Tenta fazer login no Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": data['email'],
            "password": data['password']
        })
        
        if auth_response.user:
            session['user_id'] = auth_response.user.id
            return jsonify({
                "success": True,
                "message": "Login realizado com sucesso!"
            })
            
    except Exception as e:
        print(f"Erro no login: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Email ou senha inválidos."
        }), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
