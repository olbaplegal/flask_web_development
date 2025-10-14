# Flask: objeto de manejo para configurar o flask
# render_template: conecta funções do python com o html
from flask import Flask, render_template

# Flask(modulo main, template, static)
# __name__: refere-se ao modulo atual, nesse caso app.py
# template: html
# static: css, js...
app = Flask(__name__, template_folder='templates', static_folder='static')

# criação da rota
@app.route('/inicio')
def homepage():
    mensagem = 'Hello World!'

    # sobre os parametros:
    # pagina html para a qual será enviada a var, variavel passada
    # mensagem=mensagem:
    # 1 mensagemº nome da variavel no html
    # 2 mensagemº variavel em python
    return render_template('index.html', mensagem=mensagem)

# só executa o servidor do flask se o arquivo estiver sendo executado diretamente
# já que la em cima o app foi configurado como main, ent ele vai rodar
if __name__ == '__main__':
    app.run(debug=True)