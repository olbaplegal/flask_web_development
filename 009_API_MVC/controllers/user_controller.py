from flask import render_template, request, redirect, url_for
from models.user import User

def configure_routes(app):
    # Página raiz
    @app.route('/')
    def index():
        users = User.get_usuarios()
        return render_template('index.html', users=users)
    
    # Rota para adicionar usuário
    @app.route('/contato')
    def contato():
        return render_template('contato.html')
    
    # Rota que processa a adição de um novo usuário
    @app.route('/users/new', methods=['POST'])
    def create_users():
        name = request.form['name']
        email = request.form['email']

        # Chamando função para adicionar um usuário novo
        User.criar_usuario(name, email)
        return redirect(url_for('index')) # Redirecionando para