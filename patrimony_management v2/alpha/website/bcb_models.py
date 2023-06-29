from bcb import sgs
from datetime import date
import numpy_financial as npf

class Indicadores():

    def __init__(self):
        
        self.hoje = str(date.today())
        self.ano = int(self.hoje[0:4])
        self.ano_passado = self.hoje.replace(self.hoje[0:4], str(self.ano - 1))
        self.vinte_anos = self.hoje.replace(self.hoje[0:4], str(self.ano - 20))

    def ipca_medio_20a(self):
        
        self.ipca_20a = list()

        for i in range(int(self.vinte_anos[0:4]), self.ano+1):
            self.ipca = sgs.get({'ipca':433}, start=str(f'{i}-01-01'), end=str(f'{i+1}-01-01'))
            lista_ipca = list(self.ipca['ipca']/100)
            fatores_acumulados = [1 + valor for valor in lista_ipca]
            fator_acumulado = 1
            for fator in fatores_acumulados:
                fator_acumulado *= fator
            ipca_acumulado_ano = (fator_acumulado - 1) * 100
            self.ipca_20a.append(ipca_acumulado_ano)
        
        self.ipca_medio_20a = 0
        
        for i in self.ipca_20a:
            self.ipca_medio_20a += i
        
        return round(self.ipca_medio_20a/(len(self.ipca_20a)-1),2)

    def cdi_12m(self):

        self.cdi_12m = sgs.get({'cdi': 4392}, start = self.ano_passado)

        return self.cdi_12m
    
    def selic_12m(self):

        self.selic_12m = sgs.get({'selic': 432}, start=self.ano_passado)

        return self.selic_12m
    
    def ipca_12m(self):

        ipca = sgs.get({'ipca': 433}, start=self.ano_passado)
        lista_ipca = list(ipca['ipca']/100)
        fatores_acumulados = [1 + valor for valor in lista_ipca]
        fator_acumulado = 1
        for fator in fatores_acumulados:
            fator_acumulado *= fator
        self.ipca_acumulado_12m = (fator_acumulado - 1) * 100

        return self.ipca_acumulado_12m

    def cdi_20a(self):

        self.cdi_20a = sgs.get({'cdi': 4392}, start=self.vinte_anos)

        return self.cdi_20a
    
    def selic_20a(self):

        self.selic_20a = sgs.get({'selic':432}, start=self.vinte_anos)

        return self.selic_20a
    
    def ipca_acumulado_20a(self):

        ipca_20a = sgs.get({'ipca':433}, start=self.vinte_anos)
        lista_ipca_20a = list(ipca_20a['ipca']/100)
        fatores_acumulados_20a = [1 + valor for valor in lista_ipca_20a]
        fator_acumulado_20a = 1
        for fator in fatores_acumulados_20a:
            fator_acumulado_20a *= fator
        self.ipca_acumulado_20a = (fator_acumulado_20a - 1) * 100

        return self.ipca_acumulado_20a

    def cdi_medio_20a(self):

        self.cdi_20a = sgs.get({'cdi': 4392}, start=self.vinte_anos)

        soma = 0

        for i in self.cdi_20a['cdi']:
            soma += i

        sum2 = soma/len(self.cdi_20a)

        return round(sum2,2)
