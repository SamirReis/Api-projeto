from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexão com o Banco de Dados
connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db_connection = client["Teste"]
collection = db_connection.get_collection("Livros")

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Teste"
mongo = PyMongo(app)

# Consultar todos os livros
@app.route('/livros', methods=['GET'])
def obter_livros():
    dados = list(mongo.db.Livros.find())
    for dado in dados:
        dado['_id'] = str(dado['_id'])
    return jsonify(dados), 200

# Consultar livro por ID
@app.route('/livros/<string:id>', methods=['GET'])
def obter_livro_por_id(id):
    livro = mongo.db.Livros.find_one({"_id": ObjectId(id)})
    if livro:
        livro['_id'] = str(livro['_id'])
        return jsonify(livro), 200
    else:
        return jsonify({"erro": "Livro não encontrado"}), 404

# Editar livro por ID
@app.route('/livros/<string:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    resultado = mongo.db.Livros.update_one({"_id": ObjectId(id)}, {"$set": livro_alterado})
    if resultado.matched_count:
        return jsonify({"message": "Livro atualizado com sucesso"}), 200
    else:
        return jsonify({"erro": "Livro não encontrado"}), 404

# Criar novo livro
@app.route('/livros', methods=['POST'])
def incluir_livro_novo():
    novo_livro = request.json
    livro_id = mongo.db.Livros.insert_one(novo_livro).inserted_id
    novo_livro['_id'] = str(livro_id)
    return jsonify(novo_livro), 201

# Excluir livro por ID
@app.route('/livros/<string:id>', methods=['DELETE'])
def excluir_livro(id):
    resultado = mongo.db.Livros.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count:
        return jsonify({"message": "Livro excluído com sucesso"}), 200
    else:
        return jsonify({"erro": "Livro não encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)

