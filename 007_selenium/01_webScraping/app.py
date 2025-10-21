from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

#adicionados devido ao pupup da página
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#criando um objeto com a localização do driver do navegador que eu vou usar,
# neste caso: firefox. para procurar o de outros navegadores é só ir no site do selenium
service = Service(r'D:\\vault\dev\\flask\\007_selenium\\geckodriver.exe')

#botando options em uma classe para melhor controler
firefox_options = Options()

#maximiza a janela do navegador
firefox_options.add_argument('--start-maximized')

#outra forma de definir tamanho da tela:
# firefox_options.add_argument('--window-position=960,0')
# firefox_options.add_argument('--window-size=800,800')

navegador = webdriver.Firefox(service=service, options=firefox_options)
navegador.get('https://www.airbnb.com.br/')

#aguardando carregamento da página
time.sleep(5)

##---
# #a partir do momento que abrir a página, vai aparecer um popup de aceitar cookies
# # desta maneira tem 2 maneiras proseguir, uma é usando a função contains() e a
# # outra é com as bibilotecas importadas a cima, a seguir as duas maneiras

# #CONTAINS()
# #caso o texto possa variar ligeiramente (por exemplo, ter espaços extras), você
# # pode usar a função contains(), que é um pouco mais flexivel

# #navegador.find_element(...): este é o comando para procurar o único elemento na página
# #By.XPATH: especifica que a busca será feita usando um seletor XPath
# #campo_input.send_keys("São Paulo"): se o campo de busca for encontrado, este comando 
# # simula o usuário digitando o texto "São Paulo" dentro dele
# botao_aceitar = navegador.find_element(By.XPATH, '//button[contains(text(), "Aceitar todos")]')
# botao_aceitar.click()
##---

#USANDO AS BIBLIOTECAS
#ultilizar as bibliotecas deixa as coisas mais dinâmicas pois ela espera o elemento ser carregado na página
#WebDriverWait espera 10s ou até o elemento HTML especificado seja carregado
try:
    botao_aceitar = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Aceitar todos"]'))
    )
    botao_aceitar.click()
    print('Botão "Aceitar todos" clicado com sucesso!')

except Exception as e:
    print(f'Não foi possivel entrar ou clicar no botão: {e}')

campo_input = navegador.find_element(By.XPATH, '//input[contains(@placeholder, "Buscar destinos")]')
campo_input.send_keys("São Paulo")
campo_input.send_keys(Keys.ENTER)

input('Pressione ENTER para fechar o navegador...')
navegador.quit()