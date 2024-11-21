from flask import Blueprint, jsonify, request
from app import db
from app.models import Fornecedor, Produto, Venda

bp = Blueprint('main', __name__)

@bp.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    if request.method == 'POST':
        data = request.json
        novo_fornecedor = Fornecedor(nome=data['nome'], cnpj=data['cnpj'], email=data['email'])
        db.session.add(novo_fornecedor)
        db.session.commit()
        return jsonify({'message': 'Fornecedor adicionado com sucesso'}), 201
    
    fornecedores = Fornecedor.query.all()
    return jsonify([{'id': f.id, 'nome': f.nome, 'cnpj': f.cnpj, 'email': f.email} for f in fornecedores])

@bp.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if request.method == 'POST':
        data = request.json
        novo_produto = Produto(nome=data['nome'], descricao=data['descricao'], preco=data['preco'], 
                               quantidade=data['quantidade'], fornecedor_id=data['fornecedor_id'])
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify({'message': 'Produto adicionado com sucesso'}), 201
    
    produtos = Produto.query.all()
    return jsonify([{'id': p.id, 'nome': p.nome, 'descricao': p.descricao, 'preco': p.preco, 
                     'quantidade': p.quantidade, 'fornecedor_id': p.fornecedor_id} for p in produtos])

@bp.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if request.method == 'POST':
        data = request.json
        produto = Produto.query.get(data['produto_id'])
        if produto.quantidade < data['quantidade']:
            return jsonify({'message': 'Quantidade insuficiente em estoque'}), 400
        
        nova_venda = Venda(produto_id=data['produto_id'], quantidade=data['quantidade'], 
                           valor_total=data['quantidade'] * produto.preco)
        produto.quantidade -= data['quantidade']
        
        db.session.add(nova_venda)
        db.session.commit()
        return jsonify({'message': 'Venda registrada com sucesso'}), 201
    
    vendas = Venda.query.all()
    return jsonify([{'id': v.id, 'data': v.data, 'produto_id': v.produto_id, 
                     'quantidade': v.quantidade, 'valor_total': v.valor_total} for v in vendas])

@bp.route('/relatorio/vendas', methods=['GET'])
def relatorio_vendas():
    vendas = Venda.query.all()
    total_vendas = sum(v.valor_total for v in vendas)
    return jsonify({
        'total_vendas': total_vendas,
        'numero_vendas': len(vendas),
        'vendas': [{'id': v.id, 'data': v.data, 'produto_id': v.produto_id, 
                    'quantidade': v.quantidade, 'valor_total': v.valor_total} for v in vendas]
    })

@bp.route('/relatorio/estoque', methods=['GET'])
def relatorio_estoque():
    produtos = Produto.query.all()
    return jsonify([{'id': p.id, 'nome': p.nome, 'quantidade': p.quantidade, 'valor_total': p.quantidade * p.preco} 
                    for p in produtos])
