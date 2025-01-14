from flask import render_template, request, redirect, url_for, flash
from app import db
from models import Veiculo

def setup_routes(app):
    @app.route('/veiculos', methods=['GET', 'POST'])
    def veiculos():
        if request.method == 'POST':
            modelo = request.form['modelo']
            marca = request.form['marca']
            preco = float(request.form['preco'])
            ano = int(request.form['ano'])
            veiculo = Veiculo(modelo=modelo, marca=marca, preco=preco, ano=ano)
            db.session.add(veiculo)
            db.session.commit()
            flash("Veículo adicionado com sucesso!", "success")
            return redirect(url_for('veiculos'))
        veiculos = Veiculo.query.all()
        return render_template('veiculos.html', veiculos=veiculos)

    # Adicione outras rotas aqui
