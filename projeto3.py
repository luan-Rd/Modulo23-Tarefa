import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc

def cria_graficos(df):
    fig1 = px.histogram(df, x='Nota', nbins=35, title='Distribuição das Notas dos Produtos')
    fig1.update_traces(marker_line_width=1, marker_line_color="black")
    fig1.update_layout(
        yaxis_title='Frequência',
        title_x=0.5,
        width=700,
        height=500)

    fig2 = px.scatter(df, x='Nota', y='N_Avaliações')
    fig2.update_layout(
        title='Dispersão - Relação entre Notas e Número de avaliações',
        yaxis_title='Número de Avaliações',
        title_x=0.5,
        width=700,
        height=500)

    df_corr = df[['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']].corr()
    fig3 = px.imshow(df_corr, text_auto=True, aspect='auto', color_continuous_scale='thermal',
                     title='Mapa de Calor de Correlação entre Variáveis')
    fig3.update_layout(
        title_x=0.5,
        width=700,
        height=500)

    vendas_por_marca = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum()
    threshold = 0.02 * vendas_por_marca.sum()
    marcas_relevantes = vendas_por_marca[vendas_por_marca >= threshold]
    outros = vendas_por_marca[vendas_por_marca < threshold].sum()

    if outros > 0:
        marcas_relevantes = pd.concat([marcas_relevantes, pd.Series({'Outros': outros})])

    x = marcas_relevantes.index
    y = marcas_relevantes.values

    fig4 = px.bar(x=x, y=y, )
    fig4.update_traces(marker_line_width=1, marker_line_color="black")
    fig4.update_layout(
        title='Vendas por Marca',
        title_x=0.5,
        xaxis_title='Marca',
        yaxis_title='Quantidade de Vendas',
        width=700,
        height=500
    )

    fig5 = px.pie(values=y, names=x, hole=0.2, title='Distribuição de Vendas por Marca',
                  color_discrete_sequence=px.colors.sequential.GnBu)
    fig5.update_traces(textinfo='percent+label', marker=dict(line=dict(color='black', width=1)))
    fig5.update_layout(title_x=0.5,width=700, height=500)

    fig6 = px.density_contour(df, x='Preço')
    fig6.update_traces(contours_coloring="fill", contours_showlabels=True)
    fig6.update_layout(
        xaxis_title='Preço R$',
        title='Densidade de Preços',
        title_x=0.5,
        width=700,
        height=500
    )
    return fig1, fig2, fig3, fig4, fig5, fig6

def cria_app(df):

    app = Dash(__name__)

    fig1, fig2, fig3, fig4, fig5, fig6 = cria_graficos(df)

    app.layout = html.Div([
        html.H1('Dashboard para visualização de gráficos'),
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6)
    ],)
    return app

df = pd.read_csv('ecommerce_estatistica.csv')

if __name__ == '__main__':
    app = cria_app(df)
    app.run_server(debug=True, port=8050)