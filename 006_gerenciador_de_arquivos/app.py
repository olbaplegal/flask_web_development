from flask import Flask, render_template, request, redirect, url_for, send_from_directory

#import os: Importa a biblioteca "os", que permite interagir com o sistema
#  operacional, como listar arquivos em um diretório
import os

# passa o filename e retonar uma versão segura dele
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "D:\\vault\dev\\flask\\006_gerenciador_de_arquivos>\\downloads"

#os.listdir(UPLOAD_FOLDER): Usa a biblioteca "os" para uma lista com os nomes de
# tudo que esta dentro da pasta UPLOAD_FOLDER

#os.path.isfile(caminho): Para cada item na pasta, ele verifica se é de fato um 
# arquivo (e não uma subpasta)

@app.route('/')
def index():
    arquivos = []
    for nome_arquivo in os.listdir(UPLOAD_FOLDER): #listando nomes
        caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        if os.path.isfile(caminho):
            arquivos.append(nome_arquivo)
        return render_template('index.html', arquivos=arquivos)

#UPLOAD
@app.route('/diretorio', methods=['POST'])
def upload():
    if 'meuArquivo' not in request.files:
        return redirect(request.url)
    
    file = request.files['meuArquivo']

    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        savePath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(savePath)
        return redirect(url_for('index'))
    return redirect(request.url)

#send_from_directory: função utilizada para manter a segurança do flask em downloads

#as_attachment=True: Esse parâmetro diz ao navegador para tratar o arquivo como
# um anexo, forçando a abertura de uma caixa de diálogo

#DOWNLOAD
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)