from functools import wraps
from flask import redirect, url_for, session, flash
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Verifica se as variáveis de ambiente estão definidas
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidas nas variáveis de ambiente")

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def register_user(email: str, password: str, name: str, department: str = None):
    try:
        # Registra o usuário no Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            # Cria o perfil do usuário na tabela profiles
            profile_data = {
                "id": auth_response.user.id,
                "email": email,
                "name": name,
                "department": department or "",
                "role": "user"  # Papel padrão para novos usuários
            }
            
            result = supabase.table('profiles').insert(profile_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar perfil: {result.error}")
                
            return True, "Registro realizado com sucesso!"
        else:
            raise Exception("Erro ao criar usuário")
            
    except Exception as e:
        print(f"Erro no registro: {str(e)}")  # Log do erro
        return False, str(e)

def login_user(email: str, password: str):
    try:
        # Tenta fazer login no Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            try:
                # Busca informações adicionais do perfil
                profile = supabase.table('profiles')\
                    .select("*")\
                    .eq('id', auth_response.user.id)\
                    .single()\
                    .execute()
                    
                if hasattr(profile, 'error') and profile.error:
                    raise Exception(f"Erro ao buscar perfil: {profile.error}")
                
                # Armazena dados do usuário na sessão
                session['user'] = {
                    'id': auth_response.user.id,
                    'email': email,
                    'name': profile.data.get('name'),
                    'department': profile.data.get('department'),
                    'role': profile.data.get('role')
                }
                return True, "Login realizado com sucesso!"
            except Exception as e:
                print(f"Erro ao buscar perfil: {str(e)}")  # Log do erro
                return False, f"Erro ao buscar perfil: {str(e)}"
    except Exception as e:
        print(f"Erro no login: {str(e)}")  # Log do erro
        return False, str(e)

def logout_user():
    try:
        supabase.auth.sign_out()
        session.pop('user', None)
        return True, "Logout realizado com sucesso!"
    except Exception as e:
        print(f"Erro no logout: {str(e)}")  # Log do erro
        return False, str(e)
