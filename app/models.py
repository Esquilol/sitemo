from app import db
from datetime import datetime

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    fornecedor = db.relationship('Fornecedor', backref=db.backref('produtos', lazy=True))

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    produto = db.relationship('Produto', backref=db.backref('vendas', lazy=True))
    quantidade = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
