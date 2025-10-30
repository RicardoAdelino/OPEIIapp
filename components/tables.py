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
