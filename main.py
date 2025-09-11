from flask import Flask, request, jsonify, render_template_string 
import pandas as pd 
import sqlite3 
import os 
import plotly.graph_objs as go 
from dash import Dash, html, dcc 
import dash 
import numpy as np 
import config 
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler 

app = Flask(__name__)
DB_PATH = config.DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(mes TEXT PRIMARY KEY, inadimplencia REAL)
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic(mes TEXT PRIMARY KEY, selic_diaria REAL)
        ''')

vazio = 0

@app.route('/') 
def index():
    return render_template_string('''
        <h1> Upload de dados Economicos </h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <label for="campo_inadimplencia"> Arquivo de Inadimplencia: (CSV)</label>
            <input name="campo_inadimplencia" type="file" required>
            <br><br>
          <label for="campo_selic">  Arquivo de Taxa Selic: (CSV)</label>
            <input name="campo_selic" type="file" required>
            <br><br>                                  
            <input type="submit" value="Fazer Upload">                              
        </form>
        <br><br>                                  
        <hr>
            <br><a href="/consultar"> Consultar dados Armazenados </a>                              
            <br><a href="/graficos"> Visualizar Graficos </a>
            <br><a href="/editar_inadimplencia"> Editar dados de Inadimplencia </a>                                  
            <br><a href="/correlacao"> Analisar Correlação </a>
    ''')
@app.route('/upload', methods=["POST","GET"])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic') 

    # verificar se os arquivos foram recebidos 
    if not inad_file or not selic_file: 
        return jsonify({'Erro':"Ambos os arquivos devem ser enviados"})

    inad_df = pd.read_csv(
        inad_file, 
        sep = ';',
        names = ['data','inadimplencia'], 
        header = 0
    )

    selic_df = pd.read_csv(
        selic_file, 
        sep = ';',
        names = ['data','selic_diaria'], 
        header = 0
    )
    inad_df['data'] = pd.to_datetime(inad_df['data'], format='%d/%m/%Y')
    selic_df['data'] = pd.to_datetime(selic_df['data'], format= '%d/%m/%Y')

    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str) 
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)     

    inad_mensal = inad_df[['mes','inadimplencia']].drop_duplicates() 
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index() 

    with sqlite3.connect(DB_PATH) as conn: 
        inad_mensal.to_sql('inadimplencia', conn, if_exists='replace',index=False)
        selic_mensal.to_sql('selic', conn, if_exists='replace',index=False) 
    return jsonify({'Mensagem':'Dados armazenados com sucesso!'})

@app.route('/consultar', methods=['POST','GET'])
def consultar():
    if request.method == "POST":
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia','selic']:
            return jsonify({'Erro':'Tabela inválida'}),400 
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn) 
        return df.to_html(index=False)


    return render_template_string('''
        <h1>Consulta de tabelas</h1>
        <form method='POST'>
            <label for="campo_tabela">Escolha a tabela:</label>
            <select name="campo_tabela">
                <option value="inadimplencia">Inadimplencia</option>
                <option value="selic">Taxa Selic</option>
            </select> 
            <br>
            <input type="submit" value="Consultar">
        </form>
    ''')


@app.route('/graficos')
def graficos():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df = pd.read_sql_query('SELECT * FROM inadimplencia', conn)
        selic_df = pd.read_sql_query('SELECT * FROM selic', conn)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x = inad_df['mes'],
        y = inad_df['inadimplencia'],
        mode = 'lines+markers', 
        name = 'Inadimpência'
    ))
    # 
    fig1.update_layout(
        title = 'Evolução da Inadimplencia',
        xaxis_title = 'Mês',
        yaxis_title = '%',
        template = 'gridon'
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x = selic_df['mes'],
        y = selic_df['selic_diaria'],
        mode = 'lines+markers', 
        name = 'Selic'
    ))
    # 
    fig2.update_layout(
        title = 'Média Mensal da Selic',
        xaxis_title = 'Mês',
        yaxis_title = 'Taxa',
        template = 'gridon'
    )

    graph_html_1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    graph_html_2 = fig2.to_html(full_html=False, include_plotlyjs=False)

    return render_template_string('''
        <html>
            <head>
                <title> </title>
                <style>
                    .container{
                        display:flex;
                        justify-content:space-around;
                    }
                    .graph{
                        whidth:48%;
                    }        
                </style>
            </head>
            <body>
                <h1>Graficos Economicos</h1>
                    <div class="container">
                    <div class="graph">{{ grafico1|safe }}</div>
                    <div class="graph">{{ grafico2|safe }}</div>
                </div>
            </body>
        </html>
''', grafico1 = graph_html_1, grafico2 = graph_html_2)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)







