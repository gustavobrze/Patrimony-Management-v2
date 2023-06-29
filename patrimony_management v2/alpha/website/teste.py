import pandas as pd
from IPython.display import display
import plotly.graph_objects as go

classes = ['CDI', 'Ação', 'IPCA', 'Conta Corrente', 'Ação']
value = [15000, 35000, 14000, 7500, 10000]
bank = ['XP', 'Guide', 'Itaú', 'Safra', 'Safra']

df = pd.DataFrame({'Classe':classes, 'Valor':value, 'Instituição': bank})

df5 = df.drop(['Instituição'], axis=1)

df6 = df5.groupby(['Classe']).sum()

display(df6)
