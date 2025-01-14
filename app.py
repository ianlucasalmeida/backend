from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Inicialização do app
app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:senha@localhost/concessionaria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Numeric(12, 2), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    vendido = db.Column(db.Boolean, default=False)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)

class Venda(db.Model):
    __tablename__ = 'vendas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    data_venda = db.Column(db.DateTime, default=db.func.current_timestamp())
    valor_total = db.Column(db.Numeric(12, 2), nullable=False)

# Rotas para CRUD de Veículos
@app.route('/veiculos', methods=['GET'])
def get_veiculos():
    veiculos = Veiculo.query.all()
    return jsonify([{
        'id': v.id,
        'modelo': v.modelo,
        'marca': v.marca,
        'preco': float(v.preco),
        'ano': v.ano,
        'vendido': v.vendido
    } for v in veiculos])

@app.route('/veiculos', methods=['POST'])
def add_veiculo():
    data = request.json
    novo_veiculo = Veiculo(
        modelo=data['modelo'],
        marca=data['marca'],
        preco=data['preco'],
        ano=data['ano']
    )
    db.session.add(novo_veiculo)
    db.session.commit()
    return jsonify({'message': 'Veículo adicionado com sucesso!'})

@app.route('/veiculos/<int:id>', methods=['PUT'])
def update_veiculo(id):
    data = request.json
    veiculo = Veiculo.query.get(id)
    if not veiculo:
        return jsonify({'error': 'Veículo não encontrado'}), 404
    veiculo.modelo = data.get('modelo', veiculo.modelo)
    veiculo.marca = data.get('marca', veiculo.marca)
    veiculo.preco = data.get('preco', veiculo.preco)
    veiculo.ano = data.get('ano', veiculo.ano)
    veiculo.vendido = data.get('vendido', veiculo.vendido)
    db.session.commit()
    return jsonify({'message': 'Veículo atualizado com sucesso!'})

@app.route('/veiculos/<int:id>', methods=['DELETE'])
def delete_veiculo(id):
    veiculo = Veiculo.query.get(id)
    if not veiculo:
        return jsonify({'error': 'Veículo não encontrado'}), 404
    db.session.delete(veiculo)
    db.session.commit()
    return jsonify({'message': 'Veículo deletado com sucesso!'})

# Rotas para Clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        'id': c.id,
        'nome': c.nome,
        'email': c.email,
        'telefone': c.telefone
    } for c in clientes])

@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.json
    novo_cliente = Cliente(
        nome=data['nome'],
        email=data['email'],
        telefone=data['telefone']
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente adicionado com sucesso!'})

# Rotas para Vendas
@app.route('/vendas', methods=['POST'])
def add_venda():
    data = request.json
    nova_venda = Venda(
        veiculo_id=data['veiculo_id'],
        cliente_id=data['cliente_id'],
        funcionario_id=data['funcionario_id'],
        valor_total=data['valor_total']
    )
    db.session.add(nova_venda)
    db.session.commit()
    return jsonify({'message': 'Venda realizada com sucesso!'})

# Inicializar o banco de dados (opcional, para testes locais)
'''@app.before_first_request_funcs.append
def create_tables():
    db.create_all()'''

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
