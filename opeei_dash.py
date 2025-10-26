import dash
from dash import dcc, html, Input, Output,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.express as px
import json
from dash.dash_table.Format import Format, Group, Scheme, Symbol

df = pd.read_csv('habitat_long_meta.csv') # carregando os dados
df = df.drop(df.columns[0], axis=1) #remove primeira coluna
habitat = df['habitat'].unique() # carregando os dados do popover do mapa
#print(habitat)

mapa_meta = gpd.read_file("vul_min.geojson")
mapa_meta= mapa_meta.to_crs(epsg=4326)
df_mapa = pd.DataFrame(mapa_meta)
df_mapa = df_mapa.drop(columns=['geometry', 'code_muni', 'code_state'])
df_mapa = df_mapa[['name_muni','quantile_class']]

df_meta = pd.read_csv('meta_map.csv')
meta_ = df_meta.merge(df_mapa, on='name_muni', how='left')
#print(meta_)

mapa = gpd.read_file("pr.geojson")
mapa_ = mapa.to_crs(epsg=4326)
mapa_['id'] = mapa_.index + 1
mapa_ = mapa_.reindex(
    columns = [
        'id',
        'code_muni',
        'name_muni', 
        'code_state',
        'abbrev_state',
        'geometry'
    ]
)

# Criando a instancia da aplicação
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.GRID]) 

app.layout = html.Div([ 
        html.Div(# Div para o Titulo Geral
            dbc.Row( # Linha
                dbc.Col( # Coluna
                    html.H3("Observatório Paranaense de Espécies Exóticas e Invasoras") # Aqui é o elemento de texto
                ), style = {'textAlign': 'center', 'color': 'black', 'font-weight': 'bold'} # deixando o conteúdo da coluna centralizado
            ), style = {'paddingTop': "20px", 'paddingBottom': "20px"} # adicionado espaçamento para a linha    
        ),
        html.Div( # Div para os dados do Brasil (mapa)
            [
                dbc.Row(# Titulo
                    dbc.Col(
                        html.H3(id="title-habitat"),
                    ), style = {'textAlign': 'center', 'paddingTop': '40px', 'paddingBottom': '40px'}
                ),
                dbc.Row(
                    [
                        dbc.Col( # texto
                            html.Label("Escolha um habitat"), # texto que será impresso
                            width = 3, # número de colunas que o texto irá preencher
                            align = 'left', # posição do elemento dentro do número de colunas setado por width
                            style = {'diplay': 'inline-block', 'font-weight': 'bold'}, # apenas estilo
                        ),
                        dbc.Col( # popover
                            html.Div(
                                [
                                    dbc.Button( # botão que compoe o popover
                                        "+ info", # Texto do botão
                                        outline = True, # Adiciona contorno ao botão para melhorar o stylo
                                        id = "popovertarget-mapa", # id do botão
                                        style= {'fontFamily': 'Garamond', }, # alterando a fonte do botão
                                        className="mr-2", # alterando o tipo do botão com uma classe do bootstrap
                                        color="success", # alterando a cor do botão
                                        size="sm", # alterando o tamanho do botão para pequeno
                                    ),
                                    dbc.Popover( # popover em si
                                        [
                                            dbc.PopoverHeader(id='popover-header-mapa'), # id do cabeçalho do popover
                                            dbc.PopoverBody( # O corpo do popover
                                                dcc.Markdown( # elemento para rodar tags markdown
                                                        id='popover-body-mapa', # id do corpo do popover
                                                        style={'textAlign': 'justify',} # deixando o texto do corpo justificado
                                                    ),
                                                    style= {'overflow': 'auto', # adicionado barra de rolagem ao corpo do popover
                                                            'max-height': '500px'} # colocando um tamanho máximo para a caixa do popover
                                                ),
                                        ],
                                        id ='popover-mapa', # setando a id
                                        target = "popovertarget-mapa", # setando o botão de target
                                        placement='bottom-end', # definindo a posição que o popver deve abrir na tela em relação ao botão
                                        is_open = False, # definindo que o estado inicial do popover é fechado
                                    ),
                                ]
                            ),
                            width = 2, # setando o numero de colunas que o elemento de ocupar
                            align = 'right', # setando a posição que o elemento deve ficar
                        ),
                    ], style = {'paddingLeft': '12%', 'paddingRight': '5%'}, # adicionando um espaçamento lateral
                       justify='between', # definindo que as colunas que "sobram" devem ficar entre as colunas setadas
                ),
                dbc.Row(# Dropdown
                    dbc.Col(
                            dcc.Dropdown(id = 'habitat-picker', # id do dropdown
                                         value = habitat[1], # seta o valor inicial,
                                         options = habitat, # as opções que vão aparecer no dropdown
                                         clearable = False, # permite remover o valor (acho importante manter false para evitar problemas)
                                         style = {'width': '50%'} # especifica que a largura do dropdown
                                         ),
                        ), style = {'paddingTop': "5px",'paddingLeft': '10%', 'paddingBottom': '10px'}                                    
                    ),
                dbc.Row( # mapa + tabela
                    [
                        dbc.Col( # mapa
                            dcc.Graph(id = 'map-brazil'), # id do mapa
                            width = 7, # numero de colunas que o mapa irá ocupar
                            align = 'center', # posição do elemento dentro das colunas
                            style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'} # adicionando um espaçamento para não ficar tudo grudado
                        ),
                        dbc.Col( # Tabela
                            html.Div(id = 'mapa-data-table'), # id da tabela do mapa
                            width = 3, # número de colunas que a tabela irá ocupar
                            align = 'center', # centralizando a tabela dentro das colunas
                            style = {'display': 'inline-block', 'paddingLeft': '1%', 'paddingRight': '1%'} # adicionando um espaçamento para não ficar tudo grudado
                        ),
                    ]
                ),            
            ]
        ),
    ]
)

# Função para atualizar a tabela do mapda quando o usuário alterar o dropdown
@app.callback(Output('mapa-data-table', 'children'),
            [Input('habitat-picker', 'value')])

def update_table_map(selected_habitat):
    bar_data = meta_[['name_muni', selected_habitat]]
    bar_ = bar_data[bar_data[selected_habitat] > 0]
    bar_ = bar_.nlargest(20, selected_habitat)
    bar_ = bar_.reindex(
    #columns = [
    #        'rank',
    #        'name_muni', 
    #        selected_habitat
    #        ]
        )
    bar_ = bar_.rename(
        columns = {
            'name_muni': 'municipio',
            str(selected_habitat): 'N'
            }
        )
    return [
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in bar_.columns], # passando o nome das colunas com um id
            data = bar_.to_dict('records'), # passando os dados
            fixed_rows={'headers': True}, # fixando o cabeçalho para que a barra de rolamento não esconda o cabeçalho
            style_table={'height': '400px', 'overflowY': 'auto'}, # adicionando uma barra de rolamento, e fixando o tamanho da tabela em 400px
            #style_table={'height': 'auto', 'overflowY': 'autvisible'}, # adicionando uma barra de rolamento, e fixando o tamanho da tabela em 400px
            style_data={'whiteSpace': 'normal','height': 'auto',
            },
            style_header={'textAlign': 'center'}, # centralizando o texto do cabeçalho
            style_cell={'textAlign': 'center', 'font-size': '14px'}, # centralizando o texto das céluas e alterando o tamanho da fonte
            style_as_list_view=True, # deixa a tabela sem bordas entre as colunas
            style_data_conditional=[ # este parametro altera a cor da célula quando o usuário clica na célula
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "rgba(205, 205, 205, 0.3)",
                    "border": "inherit !important",
                }
            ],
        )
    ]

## Função para atualizar o mapa quando o usuario alterar o dropdown
@app.callback(Output('map-brazil','figure'),
             [Input('habitat-picker','value')])

def update_map_brazil(selected_habitat):

    df_habitat = df[df['habitat'] == selected_habitat] # novo df com os dados de apenas 1 habitat por vez

    # criando o mapa
    fig = px.choropleth_mapbox(
                                df_habitat, # primeiro parâmetro é o dataframe com os dados
                                locations = 'name_muni', # coluna do DF que referencia as IDs do mapa
                                geojson = mapa_, # arquivo com os limites dos estados
                                color = 'quantile_class', # indicando qual coluna será utilizada para pintar os estados
                                featureidkey = "properties.name_muni",
                                mapbox_style="open-street-map", # estilo do mapa
                                center = {'lat': -24.845946,'lon': -51.557551}, # definindo a posição inicial do mapa
                                zoom = 5.4, # definindo o zoom do mapa (número inteiro entre 0 e 20)
                                opacity = 0.75, # definindo uma opacidade para a cor do mapa
                                hover_name = "name_muni", # nome do hover
                                color_discrete_sequence = px.colors.sequential.Reds
                                #color_continuous_scale = 'reds', # muda a escala de cor
                                #range_color = [0, df['quantile_class'].max()], # limites do eixo Y

    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(legend_title_text="")

    return fig
#
#
## Alterando o estado do popover, de False para True, de True para false ao clicar
@app.callback(Output("popover-mapa", "is_open"),
            [Input('popovertarget-mapa',"n_clicks")],
            [State("popover-mapa", "is_open")])
def toggle_popover_mapa(n, is_open):
    if n:
        return not is_open
    return is_open

## Header para o popover do mapa
@app.callback(Output('popover-header-mapa', 'children'),
             [Input('habitat-picker', 'value')])
def update_pop_over_header_mapa(selected_habitat):
    return "Tabela de síntese contendo os top 20 municipios com maior numero de observaçẽos por grupo"

## Conteudo do corpo para o popover do mapa
#@app.callback(Output('popover-body-mapa', 'children'),
#             [Input('habitat-picker', 'value')])
#def update_pop_over_body_mapa(selected_habitat):
#    return df_texto_ano[df_texto_ano['habitat'] == selected_habitat]['Texto']

## Função para atualizar o titulo da Div do Mapa + tabela
@app.callback(Output('title-habitat', 'children'),
             [Input('habitat-picker', 'value')])
def update_mapa(selected_habitat):
    return ""

# Rodando a aplicação através de um servidor
if __name__ == '__main__':
    app.run(debug = True)