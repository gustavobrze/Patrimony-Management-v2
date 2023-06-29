import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly_express as px
import numpy as np

def generate_graph(obj, pv, pmt, pmt_real, nper, ir):
    # Calcular os rendimentos mensais com base nos parâmetros fornecidos (aporte ideal)
    saldos = []
    rendimentos = []
    saldo = pv
    for _ in range(nper + 1):
        valor = (saldo + pmt) * (1 + ir)
        rendimento = valor - (saldo +  pmt)
        saldo = valor
        rendimentos.append(rendimento)
        saldos.append(saldo)

    # Calcular os rendimentos mensais com base nos parâmetros fornecidos (aporte real)
    saldos_real = []
    rendimentos_real = []
    saldo = pv
    for _ in range(nper + 1):
        valor = (saldo + pmt_real) * (1 + ir)
        rendimento = valor - (saldo +  pmt_real)
        saldo = valor
        rendimentos_real.append(rendimento)
        saldos_real.append(saldo)
        
    anos = [i // 12 for i in range(nper + 1)]
    saldos_interpolados = np.interp(anos, [i/12 for i in range(nper + 1)], saldos)
    saldos_interpolados_real = np.interp(anos, [i/12 for i in range(nper + 1)], saldos_real)

    # Criar o gráfico de saldo acumulado
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if nper >= 24:
        #Ideal
        fig.add_trace(go.Scatter(x=anos, y=saldos_interpolados,
                             mode='lines', name='Investimento ideal', line=dict(color='#ED1B52'), text=[f'Ano: {ano}<br>Saldo: R$ {str(round(saldo,2))}' for ano, saldo in zip(anos, saldos_interpolados)]))
        #Real
        fig.add_trace(go.Scatter(x=anos, y=saldos_interpolados_real,
                             mode='lines', name='Investimento real', line=dict(color='#1BA2ED'), text=[f'Ano: {ano}<br>Saldo: R$ {str(round(saldo,2))}' for ano, saldo in zip(anos, saldos_interpolados_real)]))
        fig.update_layout(xaxis_title='Número de anos')
    else:
        #Ideal
        fig.add_trace(go.Scatter(x=list(range(0, nper+1)), y=saldos,
                             mode='lines', name='Investimento ideal', line=dict(color='#ED1B52'), text=[f'Ano: {ano}<br>Saldo: R$ {str(round(saldo,2))}' for ano, saldo in zip(list(range(0, nper+1)), saldos)]))
        #Real
        fig.add_trace(go.Scatter(x=list(range(0, nper+1)), y=saldos_real,
                             mode='lines', name='Investimento real', line=dict(color='#1BA2ED'), text=[f'Ano: {ano}<br>Saldo: R$ {str(round(saldo,2))}' for ano, saldo in zip(list(range(0, nper+1)), saldos_real)]))
        fig.update_layout(xaxis_title='Número de meses')
    fig.update_layout(title=obj,
                      yaxis_title='Valor',
                      legend=dict(x=0, y=1, traceorder='normal'),
                      template='plotly_white')
    fig.update_traces(mode="markers+lines")

    fig.update_layout(hovermode="x unified")

    fig.update_yaxes(nticks=10)
    # Converter o gráfico em um formato HTML string
    graph_html = fig.to_html(full_html=False, default_width='100%', default_height='100%')

    return [graph_html, saldos_real[-1]]

def pie_graph_bank(df):

    colors = {'Guide':'#133a3b', 'Safra': '#071742', 'Itaú':'#fe5900', 'Bradesco':'#fe5900', 'Santander':'#ea0000', 'BB':'#fdfc32',
          'XP':'#000000', 'BTG': '#195ab4', 'Rico':'#fe5200', 'Outros': '#ae0ee3'}
    
    gpdf = df.groupby(by='Instituição').sum()

    labels = gpdf.index.tolist()
    values = gpdf.values.flatten()

    colors2 = [colors[bank] for bank in labels]

    hover_text = [f'R$ {value:,.2f}' for value in values]
    hover_info = [f'{label}: {text}' for label, text in zip(labels, hover_text)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 hovertemplate='<b>%{label}</b>: %{percent}'+
                                               '<br><i>%{text}</i>',
                                 text=hover_info,
                                 marker=dict(colors=colors2, line=dict(color='#ffffff', width=1)))])
    
    fig.update_layout(title='Alocação atual por casa', showlegend=True)

    graph_html = fig.to_html(full_html=False, default_width='100%', default_height='100%')

    return graph_html

def pie_graph_class(df):

    colors = {'Conta Corrente':'#fcba03','CDI POS':'#fc3903', 'Inflação':'#03a9fc', 'CDI PRE': '#0349fc',
                'COE':'#fc0345','Multimercado':'#fc0345', 'Fundo Imobiliário':'#a9fc03',
                'Ação':'#03fca9', 'Hedge':'#03f8fc', 'Internacional':'#99067c', 'Outro':'#03f8fc'}

    
    gpdf = df.groupby(by='Classe').sum()

    labels = gpdf.index.tolist()
    values = gpdf.values.flatten()

    colors2 = [colors[cl] for cl in labels]

    hover_text = [f'R$ {value:,.2f}' for value in values]
    hover_info = [f'{label}: {text}' for label, text in zip(labels, hover_text)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 hovertemplate='<b>%{label}</b>: %{percent}'+
                                               '<br><i>%{text}</i>',
                                 text=hover_info,
                                 marker=dict(colors=colors2, line=dict(color='#ffffff', width=1)))])
    fig.update_layout(title='Alocação atual por classe', showlegend=True)

    graph_html = fig.to_html(full_html=False, default_width='100%', default_height='100%')

    return graph_html
