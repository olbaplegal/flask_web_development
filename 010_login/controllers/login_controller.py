from flask import render_template, request, redirect, url_for, session, flash
from models.login import Login

# Importa a função que compara uma senha em texto puro com o hash armazenado no BD. É par dafunção generate_password_hash.
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError

# Rota principal e de login
def configura_rotas(app):
    @app.route('/')
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
            email = request.form['email'] # request.form é referente ao name
            senha_form = request.form['senha']

            # Ultiliza o Model para buscar o usuário no BD
            usuario = Login.get_email(email)


            # Verifica se o usuário existe e se a senha está correta
            # check_password_hash(): Compara a senha do formulário com o hash do BD. Retonar True se corresponderem
            # session['loggedin'] = True: Armazena na sessão que o usuário está logado.
            if usuario and check_password_hash(usuario['senha'], senha_form):
                session['loggedin'] = True # Usuário logado
                session['id'] = usuario['id'] # ID da sessão recebe o ID do usuário
                session['nome'] = usuario['nome'] # nome da sessão recebe nome do usuário
                return redirect(url_for('home')) # Volta pra home
            else:
                msg = 'E-mail ou senha incorretos.'

        return render_template('login.html', msg=msg)
    
    # Rota de Logout
    @app.route('/logout')
    def logout():
        # Remove os dados da sessão
        # session.pop(...) remove as chaves da sessão, efetivamente "deslogando" o usuário
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('nome', None)
        return redirect(url_for('login')) # Redireciona pra página de login
    
    # Rota de Registro
    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        msg = ''
        if request.method == 'POST' and 'nome' in request.form and 'senha' in request.form and 'email' in request.form:
            nome = request.form['nome']
            senha = request.form['senha']
            email = request.form['email']

            # Ultiliza o Model para verificar se já existe uma conta com o e-mail
            conta_existente = Login.get_email(email)

            if conta_existente:
                msg = 'Já existe uma conta com este e-mail'

            #isalnum(): Verifica se o nome de usuário contém apenas caracteres alfanumériocos
            elif not nome.isalnum():
                msg='O nome de usuário deve conter apenas letras e números.'
            elif not nome or not senha or not email:
                msg ='Por favor, preencha todos os campos.'
            else:
                try:
                    # Valida o e-mail
                    valid = validate_email(email)
                    email_normalizado = valid.email

                    # Ultiliza o Model para criar o novo usuário
                    Login.criar_login_usuario(nome, email_normalizado, senha)

                    flash('Você foi registrado com sucesso! Faça o login.')
                    return redirect(url_for('login'))
                except EmailNotValidError:
                    msg = 'Endereço de e-mail inválido.'

        elif request.method == 'POST':
            msg='Por favor, preencha o formulário.'

        return render_template('registro.html', msg=msg)
    
    # As rotas abaixo implementam o controle de acesso
    # if 'loggedin' in session: A primeira coisa que a função faz é verificar se a chage 'loggedin' existe na session 
    # Se existir (usuario logado): O conteúdo da página é renderizado e enviado ao usuário. A rota de perfil aproveita para buscar os dados atualizados do usuário no BD usando o id salvo na sessão
    @app.route('/home')
    def home():
        if 'loggedin' in session: # Verificando se a chama existe
            return render_template('home.html', nome=session['nome'])
        return redirect(url_for('login'))
    
    # Rota do Perfil(protegida)
    @app.route('/perfil')
    def perfil():
        if 'loggedin' in session:
            # Ultiliza o Model para buscar os dados do usuário logado
            usuario = Login.get_id(session['id'])
            return render_template('perfil.html', usuario=usuario)
        return redirect(url_for('login'))