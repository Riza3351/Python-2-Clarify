import pandas as pd 
import numpy as np 
import plotly.graph_objects as go 

folder = 'C:/Users/noturno/Desktop/Riza3351-main/Airbnb/'
t_ny = 'ny.csv'
t_rj = 'rj.csv'



def standartize_columns(df : pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    lat_candidate = ['lat', 'latitude', 'Latidute', 'LAT', 'Lat', 'LATITUDE']
    lon_candidates = ['lon', 'LON', 'Lon', 'Longitude', 'LONGITUDE', 'lONG', 'Lng']
    cost_candidates = ['custo', 'valor', 'coust', 'cost', 'price', 'preço']
    name_candidates = ['nome', 'name', 'titulo', 'title', 'local','place', 'descricao'] 

    def pick(colnames, candidates): 
        # colnames: lista de nomes das colunas da tabela 
        #candidates: lista de possiveis nomes das colunas a serem encontradas 
        for c in candidates: 
            #percorre cada candidato (c) dentro da lista de candidatos 
            if c in colnames:
            # se o candidato for exatamente igual a um dos nomes em colnames (tabela) 
                return c 
            #retorna esse candidato imediatamente 
        for c in candidates: 
            #se não encontrou a correspondencia 
            # percorre novamente cada coluna 
            for col in colnames:
                #aqui percorre cada nome da coluna 
                if c.lower() in col.lower(): 
                #faz igual o de cima, mas trabalhando em minusculas aoenas
                    return col 
                    # retorna a coluna imediatamente
        return None 
        #se não encontrou nenhuma coluna, nem exato nem parcial, retorna none (nenhum match encontrado)









