from apiflask import APIFlask, Schema, fields
from apiflask.validators import Length
import mysql.connector
from mysql.connector import errorcode
from flask import render_template

#Configurações do BD
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'crud_api'
}

#Criada conexão com o BD
def conexao():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f'Erro ao conectar ao DB: {err}')
        return None

#Função para iniciar o BD e a Tabela
def inicia_db():
    #Try para tratamento de erros -> Boa prática
    try:
        conn = mysql.connector.connect(
            host = db_config['host'],
            user = db_config['user'],
            password = db_config['password']
        )
        cursor = conn.cursor()  
        #Criação do Schema no mysql via python
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_config["database"]} DEFAULT CHARACTER SET "utf8"')
        print(f"Banco de dados '{db_config['database']}' criado.")

        cursor.close()
        conn.close()

        conn = conexao()
        if conn:
            #Criação da tabela livros no MySQL via python
            cursor = conn.cursor()
            query_tabela = """
            CREATE TABLE IF NOT EXISTS livros(
            id int AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            autor VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(query_tabela)
            print('Tabela "livros" criada')

            conn.commit()
            cursor.close()
            conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Erro - Verifique seu nome de usuário ou senha')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f'Erro - O BD "{db_config["database"]}" não existe')
        else:
            print(f'Ocorreu um erro: {err}')
        exit(1) #Encerra a ação senão conseguir conectar ao DB

#DEFINIÇÃO DO MODELO DE DADOS
#Propósito: Definir como devem ser os dados que um cliente envia
# para sua API para cirar um novo livro
class LivroInSchema(Schema):
    titulo = fields.String(required=True, validate=Length(min=1))
    autor = fields.String(required=True, validate=Length(min=1))

#Propósito: Definir o formato dos dados que a sua API, envia de volta
# como resposta, seja ao criar um novo livro ou listar os já existentes.
class LivroOutSchema(Schema):
    id = fields.Integer()
    titulo = fields.String()
    autor = fields.String()

#Inicia o flask
app = APIFlask(__name__, title='API de Livros', template_folder='templates', static_folder='static')

@app.get('/')
@app.doc(hide=True) #esconde o endpoint do Swagger
def index():
    return render_template('index.html')

#ENDPOINT POST
@app.post('/livros')
@app.input(LivroInSchema) #Valida os dados de entrada com o schema acima.
@app.output(LivroOutSchema, status_code=201)
def criar_livros(json_data):
    titulo = json_data['titulo']
    autor = json_data['autor']

    conn = conexao()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = 'INSERT INTO crud_api.livros (titulo, autor) VALUES (%s, %s)'
        cursor.execute(query, (titulo, autor))

        #lastrowid: É uma propriedade do conector MySQL que permite capturar o
        # último ID gerado em uma operação INSERT.
        novo_livro_id = cursor.lastrowid

        conn.commit()
        cursor.close()
        conn.close()
        
        #Retorna os dados do livro criado, incluindo o novo ID
        livro_criado = {'id':novo_livro_id, 'titulo':titulo, 'autor':autor}
        return livro_criado

#ENDPOINT GET
@app.get('/livros')
@app.output(LivroOutSchema(many=True)) #many=True indica que a saída é uma lista
def listar_livros():
    conn = conexao()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = 'SELECT * FROM crud_api.livros'
        cursor.execute(query)
        livros = cursor.fetchall()
        cursor.close()
        conn.close()
        return livros
    
if __name__ == '__main__':
    inicia_db() #Chamada função que cria a db e tabela
    app.run(debug=True)
        