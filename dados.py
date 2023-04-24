# Importanto a biblioteca para tratar os dados
import pandas as pd

# Definindo o caminho para o Arquivo CSV
path = '/Users/gus/tcc/IMDb movies.csv'

# Tratando o tipo das colunas e selecionando as colunas principais
filmes_imdb = pd.read_csv(path, delimiter=',', 
                          usecols=['imdb_title_id', 'title', 'original_title', 'year', 'date_published', 'genre', 'duration', 'country', 'language', 'director', 'writer', 'production_company', 'actors', 
                                   'description', 'avg_vote', 'votes', 'budget', 'usa_gross_income', 'worlwide_gross_income', 'metascore', 'reviews_from_users', 'reviews_from_critics'], 
                          dtype={'imdb_title_id' : 'string', 'title' : 'string', 'original_title' : 'string', 'genre' : 'string','country': 'string', 'language': 'string', 'director': 'string', 'writer': 'string', 'production_company': 'string', 'actors': 'string', 
                                 'description' : 'string', 'year': 'int', 'duration': 'int', 'votes': 'int', 'avg_vote': 'float', 'metascore': 'float'}, parse_dates=['date_published'])

#ajustando a coluna year
filmes_imdb['year'] = pd.to_datetime(filmes_imdb['year'], format='%Y').dt.strftime('%Y-%m-%d')

# separando o genero principal dos filmes para vacilitar a analise
filmes_imdb['genre'] = filmes_imdb['genre'].apply(lambda x: x.split()[0].rstrip(','))

# separando as colunas por valor financeiro e moeda
filmes_imdb[["moeda_budget", "fi_budget"]] = filmes_imdb["budget"].str.split(expand=True)
filmes_imdb[["moeda_usa_gross_income", "fi_usa_gross_income"]] = filmes_imdb["usa_gross_income"].str.split(expand=True)
filmes_imdb[["moeda_worlwide_gross_income", "fi_worlwide_gross_income"]] = filmes_imdb["worlwide_gross_income"].str.split(expand=True)

# removendo a coluna com informação financeira sem tratamento
filmes_imdb.drop(["budget", "usa_gross_income", "worlwide_gross_income"], axis=1, inplace=True)

# trocando os valores Nulos das colunas por 0 
filmes_imdb["fi_budget"].fillna(0, inplace=True)
filmes_imdb["fi_usa_gross_income"].fillna(0, inplace=True)
filmes_imdb["fi_worlwide_gross_income"].fillna(0, inplace=True)

# corrigindo o tipo das colunas criadas e depois transformando no formado internacional
filmes_imdb["fi_budget"] = filmes_imdb["fi_budget"].astype(float)
filmes_imdb["fi_usa_gross_income"] = filmes_imdb["fi_usa_gross_income"].astype(float)
filmes_imdb["fi_worlwide_gross_income"] = filmes_imdb["fi_worlwide_gross_income"].astype(float)
filmes_imdb["fi_budget"] = filmes_imdb["fi_budget"].apply(lambda x: str(x).replace(".", ","))
filmes_imdb["fi_usa_gross_income"] = filmes_imdb["fi_usa_gross_income"].apply(lambda x: str(x).replace(".", ","))
filmes_imdb["fi_worlwide_gross_income"] = filmes_imdb["fi_worlwide_gross_income"].apply(lambda x: str(x).replace(".", ","))

# ponderando as notas do publico e da critica
filmes_imdb['nota_ponderada'] = (((filmes_imdb['avg_vote'] * filmes_imdb['votes']) / filmes_imdb['votes'].sum()) * 100).round(4)
filmes_imdb['metascore_ponderada'] = (((filmes_imdb['metascore'] * filmes_imdb['reviews_from_critics']) / filmes_imdb['votes'].sum()) * 100).round(6)

# corrigindo o tipo da coluna
filmes_imdb["nota_ponderada"] = filmes_imdb["nota_ponderada"].apply(lambda x: str(x).replace(".", ","))
filmes_imdb["metascore_ponderada"] = filmes_imdb["metascore_ponderada"].apply(lambda x: str(x).replace(".", ","))
filmes_imdb["avg_vote"] = filmes_imdb["avg_vote"].astype(str).str.replace(".", ",")
filmes_imdb["reviews_from_users"] = filmes_imdb["reviews_from_users"].astype(str).str.replace(".", ",")
filmes_imdb["reviews_from_critics"] = filmes_imdb["reviews_from_critics"].astype(str).str.replace(".", ",")
filmes_imdb["metascore"] = filmes_imdb["metascore"].astype(str).str.replace(".", ",")

# ordenando os resultados
filmes_imdb = filmes_imdb.sort_values(by='nota_ponderada', ascending=False)

# validando os dados
print (filmes_imdb.head(5))

# salvando os dados tratados
filmes_imdb.to_csv('filmes_imdb_cleaned.csv', encoding='utf-8', sep=';')