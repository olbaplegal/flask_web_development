import mysql.connector
from config import db_config

def inicia_bd():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f'Erro de conexão com o BD {err}')
        return None
    
class User:
    # get_usuarios faz a query para pegar os usuários e retorna os users em uma lista
    @staticmethod
    def get_usuarios():
        users = []
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor(dictionary=True) # Criando cursor no formato dictionary
            try:
                cursor.execute('SELECT * FROM bd_mvc.users')
                users = cursor.fetchall()
            except mysql.connector.Error as err:
                print(f'Erro ao buscar usuários: {err}')
            finally:
                cursor.close()
                conn.close()
        return users
    
    @staticmethod
    # criar_usuario faz o insert dos dados no bd
    def criar_usuario(name, email):
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor()
            try:
                query = 'INSERT INTO bd_mvc.users (name, email) VALUES (%s, %s)'
                cursor.execute(query, (name, email))
                conn.commit()
            except mysql.connector.Error as err:
                print(f'Erro ao criar um usuário: {err}')
                conn.rollback() # Dá um rollback na query
            finally:
                cursor.close()
                conn.close()