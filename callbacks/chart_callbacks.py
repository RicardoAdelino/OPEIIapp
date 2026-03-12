
"""
Callbacks da Página de graficos
"""
from dash import Input, Output
import plotly.express as px
from services.data_processor import DataProcessor
from services.data_loader import DataLoader
from components.tables import create_data_table,tabela_dados_grafico
from config import Config
import plotly.graph_objects as go

# Adiciona imagem da estatistica descritiva
def register_line_callbacks(app):
    """Registra callbacks da página do grafico de linhas"""
    processor = DataProcessor()
    #loader = DataLoader()

    #Versão atual (Funcionando)
    #@app.callback(
    #Output('time-series-graph', 'figure'),
    #Input('time-series-graph', 'id'))

    # Versao drop down
    @app.callback(
    [Output('time-series-graph', 'figure'),
     Output('tabela-dados-container', 'children')],
    [Input('id-dropdown', 'value'),
     Input('ano-slider', 'value')]
    )
    def update_oco_chart(selected_id,ano_inicial):
        oc = processor.loader.load_oco_data()
        # Sempre filtra pelo ano
        oc = oc[oc['ano_final'] >= ano_inicial]
        # Só filtra por ID se houver seleção não vazia
        if selected_id:
            oc = oc[oc['ID'] == selected_id]
        #oc = processor.loader.load_oco_data()
        ## Filtra os dados pelo ID, se houver seleção
        #if selected_id:
        #    oc = oc[oc['ID'] == selected_id]
        #    # Filtra por ano inicial
        #    oc = oc[oc['ano_final'] >= ano_inicial] #Slider
        ## Filtra por ID se houver
        #if selected_id is not None and selected_id != "":
        #    oc = oc[oc['ID'] == selected_id]
        #  # --- GRÁFICO
        n_ano = (
            oc
            .groupby('ano_final')
            .size()
            .rename('n_obs')
            .reset_index()
        )
        n_ano['acc_'] = n_ano['n_obs'].cumsum()
        #n_ano = oc.groupby('ano_final').size().rename('n_obs').reset_index()
        #n_ano['acc_'] = n_ano['n_obs'].cumsum()
        
        fig = px.line(
            n_ano,
            x='ano_final',
            y='acc_',
            labels={'acc_': 'acumulados'},
            hover_name='ano_final',
            hover_data={'n_obs': False, 'acc_': True}
        )
        fig.update_traces(
            hovertemplate='Acumulados: %{y}',
            name='acumulados'
        )
        fig.add_trace(
            go.Scatter(
                x=n_ano['ano_final'],
                y=n_ano['n_obs'],
                mode='lines',
                name='observado',
                line=dict(color='orange'),
                hovertemplate='Observados: %{y}',
                customdata=n_ano['n_obs'],
                showlegend=False
            )
        )
        fig.update_layout(hovermode='x unified')

       #        fig.update_layout(hovermode='x unified')

        fig.update_xaxes(
            title='Ano dos registro observados',              # Título do eixo x
            range=[1950, n_ano['ano_final'].max()],
            dtick=4,
            showgrid=True,                        # Mostra linhas de grade
            gridcolor='grey',                # Cor da grade
            tickfont=dict(color='white'),          # Cor dos valores (ticks) do eixo x
            title_font=dict(size = 20, color='white')         # Cor do título do eixo x (use title_font, não titlefont)
        )

        fig.update_yaxes(
            title='Quantidade de <br> registros observados',      # Título do eixo y
            showgrid=True,
            gridcolor='grey',
            tickfont=dict(color='white'),         # Cor dos valores do eixo y
            title_font=dict(size = 20, color='white')        # Cor do título do eixo y (use title_font)
        )

        fig.add_annotation(
            text="Fonte: Observatório de Espécies Exóticas do Paraná, 2025",
            xref="paper",
            yref="paper",
            x= .5,
            y= -0.2,  # Posição abaixo do gráfico
            showarrow=False,
            font=dict(size=15, color="white"),
            xanchor="center",
            yanchor="top"
        )

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)', #rgba(0,0,0,0)',  # Fundo transparente
            paper_bgcolor='rgba(0, 0, 0, 0)', #  '#1f1f1f' #rgba(0,0,0,0)'  # Fundo do papel (externo ao gráfico) também transparente, se necessário
            hoverlabel=dict(
                bgcolor="beige",
                font_size=16,
                font_family="Arial"
            ), 
            #title ='Registros de ocorrência para o Estado do Paraná',  # Define o título
            title ='',  # Define o título
            title_font=dict(size=15, color='white'),  # Define cor e tamanho da fonte do título
            title_x = 0.5  # Centraliza o título
        )


        fig.add_annotation(
            x = 1958,
            y = 0,  # Substitua 0 pelo valor que deseja no eixo y (ou use um valor dinâmico)
            text = "The Biology of invasions by <br> animal and plants",
            showarrow = True,
            arrowcolor = 'white',
            arrowhead = 5,
            font = dict(color="white", size = 13),
            ax = 0,
            ay = -100,  # Posição do texto em relação ao marcador
            bgcolor="rgba(0,255,255,0.25)"
        )

        fig.add_annotation(
            x = 1986,
            y = 0,  # Substitua 0 pelo valor que deseja no eixo y (ou use um valor dinâmico)
            text = "Inicio do mapeamento de <br>uso da terra no Brasil<br><b>MapBiomas</b>",
            showarrow = True,
            arrowcolor = 'white',
            arrowhead = 5,
            font = dict(color="white", size = 13),
            ax = 0,
            ay = -155,  # Posição do texto em relação ao marcador
            bgcolor="rgba(0,255,255,0.25)"
        )

        fig.add_annotation(
            x = 2024,
            y = 0,  # Substitua 0 pelo valor que deseja no eixo y (ou use um valor dinâmico)
            text = "Relatório Técnico<br><b>IPBES</b>",
            showarrow = True,
            arrowcolor = 'white',
            arrowhead = 5,
            font = dict(color="white", size = 13),
            ax = 0,
            ay = -220,  # Posição do texto em relação ao marcador
            bgcolor="rgba(0,255,255,0.25)"
        )
        tabela_dados = tabela_dados_grafico(oc)
        return fig, tabela_dados
        

 
   # versão funciona 
#    def update_oco_chart(_):
#        n_ano = processor.get_oco_data_for_ts()
#
#        fig = px.line(
#        n_ano, 
#        x = 'ano_final', 
#        y = 'acc_',
#        labels = {'acc_': 'acumulados'},
#        hover_name ='ano_final',
#        hover_data = {'n_obs': False, 'acc_': True}
#    )
#
#        # Define o nome da legenda para a linha azul
#        fig.update_traces(
#            hovertemplate='<b>Acumulados:</b> %{y}<extra></extra>',
#            name ='acumulados'
#        )
#
#        fig.add_trace(
#            go.Scatter(
#                x = n_ano['ano_final'], 
#                y = n_ano['n_obs'], 
#                mode = 'lines', 
#                name = 'observado',
#                line = dict(color='orange'),
#                hovertemplate='<b>Observados:</b> %{y}<extra></extra>',
#                customdata = n_ano['n_obs'], 
#                showlegend = False
#            )
#        )
#
#        fig.update_layout(hovermode='x unified')
#
#        fig.update_xaxes(
#            title='Ano dos registro observados',              # Título do eixo x
#            showgrid=True,                        # Mostra linhas de grade
#            gridcolor='grey',                # Cor da grade
#            tickfont=dict(color='white'),          # Cor dos valores (ticks) do eixo x
#            title_font=dict(size = 20, color='white')         # Cor do título do eixo x (use title_font, não titlefont)
#        )
#
#        fig.update_yaxes(
#            title='Quantidade de <br> registros observados',      # Título do eixo y
#            showgrid=True,
#            gridcolor='grey',
#            tickfont=dict(color='white'),         # Cor dos valores do eixo y
#            title_font=dict(size = 20, color='white')        # Cor do título do eixo y (use title_font)
#        )
#
#        fig.add_annotation(
#            text="Fonte: Observatório de Espécies Exóticas do Paraná, 2025",
#            xref="paper",
#            yref="paper",
#            x= .5,
#            y= -0.2,  # Posição abaixo do gráfico
#            showarrow=False,
#            font=dict(size=15, color="white"),
#            xanchor="center",
#            yanchor="top"
#        )
#
#        fig.update_layout(
#            plot_bgcolor='#1f1f1f', #rgba(0,0,0,0)',  # Fundo transparente
#            paper_bgcolor= '#1f1f1f', #rgba(0,0,0,0)'  # Fundo do papel (externo ao gráfico) também transparente, se necessário
#            hoverlabel=dict(
#                bgcolor="beige",
#                font_size=16,
#                font_family="Arial"
#            ), 
#            title ='Registros de ocorrência para o Estado do Paraná',  # Define o título
#            title_font=dict(size=20, color='white'),  # Define cor e tamanho da fonte do título
#            title_x = 0.5  # Centraliza o título
#        )
#
#
#        fig.add_annotation(
#            x = 1957,
#            y = 0,  # Substitua 0 pelo valor que deseja no eixo y (ou use um valor dinâmico)
#            text = "The Biology of invasions by <br> animal and plants",
#            showarrow = True,
#            arrowcolor = 'white',
#            arrowhead = 5,
#            font = dict(color="white", size = 13),
#            ax = 0,
#            ay = -100  # Posição do texto em relação ao marcador
#        )
#        return fig
#
#    
#
#