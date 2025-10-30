import mysql.connector

# Função para criar um hash para as senhas
# As senhas não serão armazenadas em texto puro no BD
from werkzeug.security import generate_password_hash
from config import Config

def inicia_bd():
    try:
        conn = mysql.connector.connect(**Config.DB_CONFIG)
        return conn # Retorna conexão com o BD
    except mysql.connector.Error as err:
        print(f'Erro de conexão com o BD: {err}')
        return None

class Login:
    @staticmethod
    def get_email(email): # Busca o usuário pelo e-mail
        conn = inicia_bd() # pega a conexão com o BD e coloca numa variavel qualquer
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM login_usuarios.usuarios WHERE email = %s', (email,))
            usuario = cursor.fetchone() # Retorna a primeira da consulta
            cursor.close()
            conn.close()
            return usuario
    
    @staticmethod
    def get_id(user_id): # Busca usuário pelo ID
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM login_usuarios.usuarios WHERE id = %s', (user_id,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()
            return usuario

    @staticmethod
    def criar_login_usuario(nome, email, senha): # Insert no BD
        conn = inicia_bd()
        if conn:
            hash_senha = generate_password_hash(senha) # Criptografando senha
            cursor = conn.cursor()
            cursor.execute('INSERT INTO login_usuarios.usuarios (nome, email, senha) VALUES (%s, %s, %s)', (nome, email, hash_senha))
            conn.commit()
            cursor.close()
            conn.close()