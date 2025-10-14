# request: acessa o valor passado aos input's
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template', static_folder='static')

# conectando e configurando o app com o sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# botando em uma instancia para facilitar o manejo
db = SQLAlchemy(app)

# criando a tabela -> "Tarefas"
class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), unique=True, nullable=False)

# READ
@app.route('/')
def index():
    # .query: função para acessar propriedades de query
    # .all: retorna todos os resultados em formato JSON
    tarefas = Tarefas.query.all()
    return render_template('index.html', tarefas=tarefas)

# CREATE
@app.route('/criar', methods=['POST'])
def criar_tarefas():
    # botando os dados passados no input. request.form se refere ao name dado a tag 
    descricao = request.form['descricao']

    # verificando se já axiste no bd
    tarefa_existente = Tarefas.query.filter_by(descricao=descricao).first()
    if tarefa_existente:
        return 'Erro: Tarefa já foi cadastrada', 400
    
    # sobre os valores passados nos parâmetros: 
    # 1º descrição = no do campo na table
    # 2º descrição = dados informados no form                                           
    new_task = Tarefas(descricao = descricao)

    # adicionando dados ao bd
    db.session.add(new_task)

    # salvando alterações
    db.session.commit()

    # redirecionando o usuario para url raiz
    return redirect('/')

# DELETE
@app.route('/deletar/<int:id_tarefa>', methods=['POST'])
def deletar_tarefas(id_tarefa):
    tarefa = Tarefas.query.get(id_tarefa)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    return redirect('/')

# PUT
@app.route('/atualizar/<int:id_tarefa>', methods=['POST'])
def atualizar_tarefas(id_tarefa):
    tarefa = Tarefas.query.get(id_tarefa)
    if tarefa:
        tarefa.descricao = request.form['descricao']
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    
    # especificando em que app vai criar a db
    with app.app_context():
        
        # cria as tabelas na db baseado na minha classe db
        db.create_all()
    app.run(debug=True)