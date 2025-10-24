from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import os
import csv

service = Service(r'D:\\vault\dev\\flask\\007_selenium\\geckodriver.exe')

firefox_options = Options()
firefox_options.add_argument('--start-maximized')

navegador = webdriver.Firefox(service=service, options=firefox_options)
navegador.get('https://books.toscrape.com/')

livros = []

time.sleep(5)

livros_dados = navegador.find_elements(By.CSS_SELECTOR, 'article.product_pod')

for livro in livros_dados:
    titulo_livro = livro.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('title')
    preco_livro = livro.find_element(By.CLASS_NAME, 'price_color').text

    preco_01 = float(preco_livro.replace('£', '').strip())
    preco_reais = preco_01 * 6.5
    preco_livro = f'R$ {preco_reais:.2f}'

    estoque_livro = livro.find_element(By.CLASS_NAME, 'instock').text
    livros.append([titulo_livro, preco_livro, estoque_livro])

    caminho_pasta = 'D:\\vault\dev\\flask\\007_selenium\\03_webScraping\\biblioteca'
    nome_arquivo = 'livro.csv'
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

    os.makedirs(caminho_pasta, exist_ok=True)

    #'w': Modo de abertura (write). Se o arquivo existir, será sobrescrito.
    #newline='': Evita linhas em branco extras entre os registros no arquivo CSV
    #csv.writer(): Cria um objeto para gerar o arquivo CSV.
    #writerow(): Escreve uma única linha no CSV(cabeçalho)
    #writerows(): Escrete múltiplas linhas de uma vez

with open(caminho_completo, 'w', newline='', encoding='utf-8-sig') as arquivo_csv:
    writer = csv.writer(arquivo_csv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Título', 'Preço', 'Estoque'])
    writer.writerows(livros)

print(f'Arquivo salvo em: {caminho_completo}')

navegador.quit()