#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 20:55:31 2024

@author: yadir
"""
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  

# Leer el archivo CSV
data_ventas = 'PRODUCT-SALES.csv'
df = pd.read_csv(data_ventas)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) 

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Div(
            [
                html.H1(children='Análisis del volumen de ventas', style={'textAlign': 'center'}),
                dcc.Dropdown(
                    options=[{'label': 'All Countries', 'value': 'All'}] + [{'label': country, 'value': country} for country in df['Country'].unique()],
                    value='All',
                    id='dropdown-country'
                ),
                dcc.Graph(id='graph-content'),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.RadioItems(
                                id='year-radio',
                                options=[{'label': 'All Years', 'value': 'All'}] + [{'label': str(year), 'value': year} for year in df['Year'].unique()],
                                value='All',
                                inline=True,
                                labelStyle={'margin-right': '15px'} 
                            ),
                            width={'size': 6, 'order': 1, 'offset': 0}  # Utilizar 6 columnas en pantallas pequeñas
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='dropdown-product-category',
                                options=[{'label': 'All Product Categories', 'value': 'All'}] + [{'label': product, 'value': product} for product in df['Product_Category'].unique()],
                                value='All',
                            ),
                            width={'size': 6, 'order': 2, 'offset': 0}  # Utilizar 6 columnas en pantallas pequeñas
                        ),
                    ],
                    className="mb-2",
                    style={'width': '100%'} 
                ),

                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(id='total-en-ventas', color="primary", className="mb-1", style={'textAlign': 'center'}),  
                        dbc.ListGroupItem(id='media', color="primary", className="mb-1", style={'textAlign': 'center'}),  
                        dbc.ListGroupItem(id='moda', color="primary", className="mb-1", style={'textAlign': 'center'}),  
                        dbc.ListGroupItem(id='mediana', color="primary", style={'textAlign': 'center'}),  
                    ],
                    id='stats-info',  # Cambio de className a id para poder actualizar el contenido
                    className="mb-2",
                    style={'width': '100%'}  
                )
            ],
            style={'margin': '15px'} 
        )
    ]
)

@app.callback(
    [Output('graph-content', 'figure'),
     Output('total-en-ventas', 'children'),  
     Output('media', 'children'),  
     Output('moda', 'children'),  
     Output('mediana', 'children')],
    [Input('dropdown-country', 'value'),
     Input('dropdown-product-category', 'value'),
     Input('year-radio', 'value')]
)
def update_graph(country, product_category, year):
    filtered_df = df.copy()
    
    if country != 'All':
        filtered_df = filtered_df[filtered_df['Country'] == country]
    if product_category != 'All':
        filtered_df = filtered_df[filtered_df['Product_Category'] == product_category]
    if year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == year]
    
    # Calcular el total de ventas y estadisticos
    total_sales = round(filtered_df['Revenue'].sum(), 2)
    media = round(filtered_df['Revenue'].mean(), 2)
    mediana = round(filtered_df['Revenue'].median(), 2)
    moda = round(filtered_df['Revenue'].mode()[0], 2)
    
    # Crear el gráfico
    fig = px.histogram(filtered_df, x='Product_Category', y='Order_Quantity', color='Product_Category')
    
    # Cambiar el nombre del eje X y del eje Y
    fig.update_layout(
        xaxis_title='Categorías de productos',
        yaxis_title='Cantidad de órdenes vendidas',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.1,
            xanchor="right",
            x=1,
            traceorder="normal",
            title='',
            font=dict(
                family="Arial",
                size=12,
                color="black"
            ),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            borderwidth=0
        )
    )
    

    
    return fig, f'Total Sales: {total_sales}', f'Mean: {media}', f'Mode: {moda}', f'Median: {mediana}'



# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

