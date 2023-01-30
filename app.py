# Importações de libraries importantes
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from sqlalchemy import create_engine
import plotly.express as px
import plotly.figure_factory as ff
import plotly
import pandas as pd

#Definição do app Flask
app = Flask(__name__)

#Parametros para conectar com SQL Server
parametros = ('Driver={SQL Server};'
        'Server=Kayky-PC;'
        'Database=app_sql;'
         'Trusted_Connection=yes;')

#Tranforma parametros em URL
url_db = quote_plus(parametros)

#Configura o SQLAlchemy para se conectar ao SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=%s' % url_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Define a db
db = SQLAlchemy(app)
app.app_context().push()

#Cria a tabela de compras e define as colunas
class Compras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Integer(), nullable=False)
    loja = db.Column(db.String(100), nullable=False)
    nota = db.Column(db.Integer())
    compra_denovo = db.Column(db.Integer())

db.create_all()

#Passa a rota de compras com método POST
@app.route('/compras/', methods=["POST"])

#Define a função comprar
def comprar():

    #Checa se o método é POST
    if request.method == "POST":

        #Pega os dados do JSON e armazena os dados na tabela
        dados = request.get_json()
        compra = Compras(nome_produto=dados["nome_produto"], valor=dados["valor"], loja=dados["loja"], nota=dados["nota"], compra_denovo=dados["compra_denovo"])
        db.session.add(compra)
        db.session.commit()
        #Retorna o status
        return {"status": "compra cadastrada"}

#Passa a rota de dados
@app.route('/dados/', methods=["GET", "POST"])

#Define a função mostrar
def mostrar():
    #Checa se o método é GET
    if request.method == "GET":

        #Passa a query no SQL Server e transforma em DataFrame do Pandas
        conexao = create_engine('mssql+pyodbc:///?odbc_connect=%s' % url_db)
        query = 'SELECT compras.nome_produto, compras.loja, compras.nota, compras.valor, compras.compra_denovo, categorias.categoria ' \
                'FROM compras ' \
                'INNER JOIN categorias ' \
                'ON categorias.nome_produto = compras.nome_produto;'
        df = pd.read_sql(query, conexao)

        #Define os graficos e converte para JSON
        fig1 = px.bar(df, x=df["nome_produto"], color=df["loja"])
        fig2 = ff.create_distplot([df["nota"]], ['nota'])
        fig3 = px.bar(df, x=df["categoria"], color=df["loja"])
        graph1 = plotly.io.to_json(fig1)
        graph2 = plotly.io.to_json(fig2)
        graph3 = plotly.io.to_json(fig3)

        #Retorna a página html com os gráficos
        return render_template('index.html', graph1=graph1, graph2=graph2, graph3=graph3)

#Inicia o app
if __name__ == '__main__':
    app.run(debug=True)