"""
Componentes de Tabela Reutilizáveis
"""
from dash import dash_table
from config import Config

def create_data_table(data, table_id='data-table', height='500px'):
    """Cria uma tabela estilizada com fundo transparente"""
    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        fixed_rows={'headers': True},
        style_table={
            'height': height,
            'overflowY': 'auto',
            'backgroundColor': 'transparent',  # Totalmente transparente
            'border': 'none'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'transparent',  # Células transparentes
            'color': Config.COLORS['text'],
            'borderBottom': '1px solid rgba(255, 255, 255, 0.1)',  # Borda sutil
            'transition': 'background-color 0.2s ease'
        },
        style_header={
            'textAlign': 'center',
            'backgroundColor': '#375a7f',  # Header mantém cor
            'color': Config.COLORS['text'],
            'fontWeight': '600',
            'borderBottom': '2px solid rgba(255, 255, 255, 0.2)',
            'fontSize': '14px',
            'padding': '12px'
        },
        style_cell={
            'textAlign': 'center',
            'fontSize': '13px',
            'padding': '12px',
            'fontFamily': 'Arial, sans-serif'
        },
        style_as_list_view=True,
        style_data_conditional=[
            # Linhas ímpares - leve destaque
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "rgba(255, 255, 255, 0.02)",  # Muito sutil
            },
            # Hover - destaque
            {
                "if": {"state": "active"},
                "backgroundColor": "rgba(55, 90, 127, 0.3)",  # Hover semi-transparente
                "border": "none",
                "cursor": "pointer"
            },
            # Selecionada
            {
                "if": {"state": "selected"},
                "backgroundColor": "rgba(55, 90, 127, 0.4)",
                "border": "1px solid #375a7f",
            }
        ]
    )

# tabela chart
#def tabela_dados_grafico(df):
#    """
#    Gera a tabela para visualização dos dados filtrados, excluindo coluna geometry.
#    """
#    # Remove coluna 'geometry' se existir
#    df = df.drop(columns=['geometry'], errors='ignore')
#    # Dicionário de renomeação: original -> novo nome
#    colunas_novos_nomes = {
#        #'ID': 'Identificador',
#        'especie': 'Espécie',
#        'lon_gdec': 'Longitude',
#        'lat_dec': 'Latitude',
#        'ano_final': 'Ano'
#        # Adicione outros conforme necessário
#    }
#    # Renomeia todas que existirem no DataFrame
#    df = df.rename(columns=colunas_novos_nomes)
#    
#    return dash_table.DataTable(
#        id="tabela-dados-grafico",
#        columns=[{"name": col, "id": col} for col in df.columns],
#        data=df.to_dict('records'),
#        page_size=10,
#        style_table={'overflowX': 'auto', 'backgroundColor': 'transparent'},
#        style_cell={'textAlign': 'left', 'padding': '5px', 'backgroundColor': 'transparent'},
#        style_header={'backgroundColor': '#375a7f', 'color': 'white', 'fontWeight': 'bold'},
#    )

def tabela_dados_grafico(df):
    # Remove a coluna geometry se existir
    df = df.drop(columns=['geometry'], errors='ignore')

    # Agrupa pelos campos desejados e conta os registros
    df_grouped = (
        df
        .groupby(['especie', 'ID', 'ano_final'])
        .size()
        .reset_index(name='Nº registros')
    )

    # Dicionário de renomeação
    col_nomes = {
        'especie': 'Espécie',
        'ID': 'Identificador',
        'ano_final': 'Ano',
        'Nº registros': 'Nº de Registros'
    }

    # Renomeia colunas
    df_grouped = df_grouped.rename(columns=col_nomes).sort_values(by='Nº de Registros', ascending=False)

    # Monta colunas para o Dash
    columns_setup = [
        {"name": col_nomes.get(orig, orig), "id": nome}
        for orig, nome in zip(df_grouped.columns, df_grouped.columns)
    ]

    return dash_table.DataTable(
        id="tabela-dados-grafico",
        columns=columns_setup,
        data=df_grouped.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto', 'backgroundColor': 'transparent'},
        style_cell={'textAlign': 'left', 'padding': '5px', 'backgroundColor': 'transparent'},
        style_header={'backgroundColor': '#375a7f', 'color': 'white', 'fontWeight': 'bold'},
    )


