from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import mysql.connector

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'password',
    'database':'biblioteca'
}

service = Service(r'D:\\vault\dev\\flask\\007_selenium\\geckodriver.exe')

firefox_options = Options()
firefox_options.add_argument('--start-maximized')

navegador = webdriver.Edge(service=service, options=firefox_options)
navegador.get('https://books.toscrape.com/')

#lista para armazenar os livros
livros=[]

time.sleep(5)

#extração de dados da página
livros_dados = navegador.find_elements(By.CSS_SELECTOR, 'article.product_pod')
for livro in livros_dados:
    titulo_livro = livro.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'A').get_attribute('title')
    preco_livro = livro.find_element(By.CLASS_NAME, 'price_color').text

    #CONVERSÃO DE MOEDA
    preco_01 = float(preco_livro.replace('£', '').strip())
    preco_reais = preco_01 * 6.50 # daria pra fazer uma conversão mais precisa fazendo uma requisição pra uma api dedicada. mas neste exemplo vou deixar dessa forma
    preco_livro = f'R$ {preco_reais:.2f}'

    estoque_livro = livro.find_element(By.CLASS_NAME, 'instock').text

    livros.append([titulo_livro, preco_livro, estoque_livro])
conexao = mysql.connector.connect(**db_config)
cursor = conexao.cursor()

cursor.execute('''
    create table if not exists livros(
        id int auto_increment primary key,
        titulo varchar(255) not null,
        preco varchar (20),
        estoque varchar(50)    
    );
''')

# cursor.execute('''
#     insert into livros (titulo, preco, estoque)
#     values (%s, %s, %s);
# ''', livros)

#o MySLQ espera uma lista de tuplas, mas seus dados podem estar como lista de 
# listas, que correspondem a linha acima do insert. Abaixo a lista de listas 
# é convertida explecitamente para tuplas

dados = [tuple(livro) for livro in livros] #converte cada lista interna em tupla
cursor.executemany('insert into livros (titulo, preco, estoque) values(%s, %s, %s)', dados)

conexao.commit()
print(f'Dados salvos no MySQL! {cursor.rowcount} registros inseridos')

navegador.quit()
cursor.close()
conexao.close()