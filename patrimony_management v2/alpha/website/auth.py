from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import secrets
from .models import User, Token
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from functools import wraps
import win32com.client as win32
import pythoncom

auth = Blueprint('auth', __name__)

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('Você já está logado.', category='error')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login efetuado!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            
            else:
                flash('Senha incorreta.', category='error')
        else:
            flash('E-mail não registrado.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    user = current_user
    logout_user()
    return redirect(url_for('auth.login'))
        
@auth.route('/sign-up', methods=['GET', 'POST'])
@logout_required
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('E-mail já registrado.', category='error')

        elif len(email) < 4:
            flash('E-mail precisa ter mais que 4 caracteres.', category='error')

        elif len(name) < 2:
            flash('Primeiro nome precisa ter mais que 2 caracteres.', category='error')

        elif password1 != password2:
            flash('As senhas não batem.', category='error')

        elif len(password1) < 7:
            flash('A senha precisa ter pelo menos 7 caracteres', category='error')

        else:
            new_user = User(email=email, first_name=name, password=generate_password_hash(password1, 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Conta criada!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        
    return render_template('sign_up.html', user=current_user)

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            
            token = secrets.token_urlsafe(32)
           
            new_token = Token(user_id = user.id, token=token, timestamp=datetime.utcnow())
            db.session.add(new_token)
            db.session.commit()
            
            reset_link = url_for('auth.reset_password_page', token=token, _external=True)
            outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
            mail = outlook.CreateItem(0)
            mail.To = f'{email}'
            mail.Subject = 'Redefinição de senha'
            mail.body = f'Segue o link para redefinição de senha\n{reset_link}'
            mail.Send()
            flash('Foi enviado um e-mail para o endereço registrado com as instruções para redefinição de senha.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('E-mail não registrado', 'error')
    return render_template('reset_password.html', user=current_user)

@auth.route('/change_password/<token>', methods=['GET', 'POST'])
def reset_password_page(token):

    token_obj = Token.query.filter_by(token=token).first()

    delta = datetime.now() - token_obj.timestamp

    if not token_obj:
        flash('Token inválido ou expirado', category='error')
        return redirect(url_for('auth.login'))
    
    if delta.total_seconds()/60 > 60:
        flash('Token expirado', category='error')
        db.session.delete(token_obj)
        db.session.commit()
        return redirect(url_for('auth.reset_password_request'))

    user = User.query.get(token_obj.user_id)

    if request.method == 'POST':
        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('As senhas não batem', category='error')
        elif len(password1)<7:
            flash('A senha precisa ter pelo menos 7 caracteres.', category='error')
        else:
            user.password = generate_password_hash(password1, 'sha256')
            db.session.delete(token_obj)
            db.session.commit()
            flash('Senha alterada com sucesso!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    
    return render_template('reset_pw_page.html', user=current_user)