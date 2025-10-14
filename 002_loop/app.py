from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/times')
def timesbr():
    mensagem = 'Times Brasileiros'
    lista_times = ['Palmeiras', 'Corinthians', 'Coritiba', 'Goiás', "São Paulo", 'Cruzeiro']
    return render_template('index.html', mensagem=mensagem, lista=lista_times)

if __name__ == '__main__':
    app.run(debug=True)