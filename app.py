import dotenv
import os
from flask import Flask, request
from bson.json_util import dumps
from flask_pymongo import PyMongo


dotenv.load_dotenv('./.env')

app = Flask(__name__)

app.config['MONGO_URI'] = os.environ['DATABASE_URI']

mongo = PyMongo(app)

produtos = mongo.db.produtos

@app.route('/', methods=['GET'])
def home():
  return 'Salve miguels'

# Lendo todos produtos
@app.route('/produtos', methods=['GET'])
def pegar_todos_produtos():
  todos_produtos = produtos.find()

  return dumps(todos_produtos)

# Lendo um produto
@app.route('/produtos/<ObjectId:id>', methods=['GET'])
def pegar_um_produto(id):
  produto = produtos.find_one({ "_id": id })

  return dumps(produto)

# Criando um produto
@app.route('/produtos/criar', methods=['POST'])
def criar_produto():
  dados = request.json

  produtos.insert_one(dados)

  return dumps('Criado com sucesso!')

# Atualizando um produto
@app.route('/produtos/<ObjectId:id>', methods=['PUT'])
def atualizar_produto(id):
  dados = request.json

  produtos.update_one({ "_id": id }, { "$set": dados })

  return dumps('Atualizado com sucesso =)')

# Deletando um produto
@app.route('/produtos/<ObjectId:id>', methods=['DELETE'])
def deletar_produto(id):
  produtos.delete_one({ "_id": id })

  return dumps('Deletado com sucesso =D')

if __name__ == '__main__':
  app.run(debug=True)
