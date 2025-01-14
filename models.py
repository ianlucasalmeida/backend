from app import db

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    vendido = db.Column(db.Boolean, default=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    cliente_email = db.Column(db.String(100), nullable=False)
    data_venda = db.Column(db.DateTime, default=db.func.current_timestamp())
