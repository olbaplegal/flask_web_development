# request: acessa o valor passado aos input's
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def calculadora():
    resultado = None

    # recebe os inputs que foram passados no form
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operacao = request.form['operacao']

        # faz a operação referente ao valor "operacao"
        if operacao == 'soma':
            resultado = round(num1 + num2,2)
        elif operacao == 'subtracao':
            resultado = round(num1 - num2,2)
        elif operacao == 'mult':
            resultado = round(num1 * num2,2)
        elif operacao == 'divisao':
            resultado = (
                round(num1 / num2,2)
                if num2 != 0
                else "Erro: divisão por zero!"
            )
    
    # retorna a var resultado
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
