#flash: 
from flask import Flask, render_template, request, redirect, flash, url_for

# mysql.connector: conecta com a db
import mysql.connector

# secrets: usado para criptografia
import secrets

app = Flask(__name__, template_folder='template', static_folder='static')

# secret_key é uma chave secreta usada para garantir segurança em
# operações que dependem de sessões.
app.secret_key = secrets.token_hex(32)

# db_config = {...}: este é um dicionário python que armazena as credenciais de acesso a db
# configuração de coneção
db_config={
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': '005_db'
}

#conn = mysql.connector(**db_config): Estabelece a conexão com o DB MySQL.
#O parâmetro "**db_config" desempacota o dicionário, passando seus valores
#como argumentos para a função connect()

#data = cursor.fetchall(): Busca todos os resultados da consulta executada

#READ
@app.route('/')
def home():
    #estabelecendo conexão com a db usando o db_config como argumento
    conn = mysql.connector.connect(**db_config)
    
    #cursor: cria um ponteiro que permite executar queryes e processar resultados
    # o dictionary=True é para retornar as rows no formato dictonary
    cursor = conn.cursor(dictionary=True) #criando cursor
    cursor.execute('select * from crud.users') #executando query via cursor
    data = cursor.fetchall() # buscando resultados da consulta
    cursor.close() #fechando ponteiro
    conn.close() #fechando conexão
    return render_template('index.html', dados=data)

#CREATE
@app.route('/add', methods=['GET', 'POST'])
def addUsuarios():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        cidade = request.form['cidade']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        #VALUES (%s, %s, %s): os %s são placeholders. eles não são os valores reais ainda.
        #é uma boa pratica de segurança.
        query = 'INSERT INTO crud.users (nome, idade, cidade) VALUES (%s, %s, %s)'
        cursor.execute(query, (nome, idade, cidade)) #NÃO FICOU MARCADO. REVISAR
        conn.commit() #salvando as alterações na db
        cursor.close()
        conn.close()
        flash('Usuário cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('index'))
    return render_template('add.html')

#UPDATE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def editUsuarios(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        cidade = request.form['cidade']

        query = 'UPDATE crud.users SET nome = %s, idade = %s, cidade = %s WHERE id = %s'
        cursor.execute(query, (nome, idade, cidade, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuário atualizado com sucesso!', 'sucesso')
        return redirect(url_for('index'))
    
    #puxar os dados para edição (GET)
    select_query = 'SELECT * FROM crud.users WHERE id = %s'

    #cursor.execute(select_query, (id,)): executa a consulta. note que a virgula
    # em(id,). ela é essencial para que o python crie uma tupla de um único
    #elemento, que é o formato que o método execute espera para os parâmetros

    #user = cursor.fetchone(): busca apenas um único resultado da consulta.
    # como o id é único, sabemos que haverá no máximo um registro.

    cursor.execute(select_query, (id,))
    user = cursor.fetchone()
    return render_template('edit.html', infos=user)

#DELETE
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def deleteUsuarios(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    delete_query = 'DELETE FROM crud.users WHERE id = %s'
    cursor.execute(delete_query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuário deletado com sucesso!', 'sucesso')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
