from flask import Flask
from controllers import login_controller

app = Flask(__name__, template_folder='views/templates', static_folder='views/static')

# Carrega as informações do arquivo config.py
# Carrega as informações da SECRET_KEY e DB_CONFIG para dentro do objeto de configuração da aplicação
app.config.from_object('config.Config')

login_controller.configura_rotas(app)

if __name__ == '__main__':
    app.run(debug=True)