import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 110)

# converter juros anuais em mensais
def anualToMensal(juros):
  return ((1+juros/100)**(1/12)-1)
  
class Financiamento():

  def __init__(self,divida,juros,tempo,cet,v_aporte,periodo_aporte):
    self.divida = divida
    self.juros_nominais = juros
    self.tempo = tempo
    self.cet = cet
    self.v_aporte = v_aporte
    self.periodo_aporte = periodo_aporte

  def calcular(self,v_aporte,periodo_aporte):
    amort = self.divida/self.tempo
    parcelas = []
    amort_juros = []
    seguro = []
    saldo_devedor = [self.divida]
    aporte = []
    juros = []
    aux = 0
    for i in range(self.tempo):
      
      aporte.append(0)
      if i%periodo_aporte ==0 and i>0:
        if v_aporte>saldo_devedor[i]:
          aporte[i]= saldo_devedor[i]
        else:
          aporte[i]+=v_aporte
        #aporte.append(5000)
        aux+=1
        saldo_devedor[i]-=aporte[i]
      if saldo_devedor[i]<0:
        #print(saldo_devedor[i])
        del saldo_devedor[i]
        del aporte[i]
        break
      v_juros = saldo_devedor[i]*anualToMensal(self.juros_nominais)
      juros.append(round(v_juros,2))
      parcelas.append(round(saldo_devedor[i]*anualToMensal(self.cet)+amort,2)) # parcela total
      amort_juros.append(round(v_juros+amort,2)) # juros + amort
      saldo_devedor.append(round(saldo_devedor[i]-amort,2))
      
    if len(saldo_devedor)>len(parcelas):
      #print(saldo_devedor[-1])
      del saldo_devedor[-1]
    #print(len(aporte))
    #print(len(saldo_devedor))
    #print(len(parcelas))
    #print(len(juros))
    #print(saldo_devedor[-1])
    dic = {"aj": amort_juros,"juros":juros,"parcela":parcelas,"aporte":aporte,"saldo":saldo_devedor}
    #print("antes do dict")
    #dic = {"aj": amort_juros,"juros":juros,"saldo":saldo_devedor}
    df = pd.DataFrame(dic)
    return df

  def tempoTotal(self):
    return len(self.calcular(self.v_aporte,self.periodo_aporte))

  def valorTotal(self):
    df = self.calcular(self.v_aporte,self.periodo_aporte)
    totalParcela = df['parcela'].sum()
    totalAporte = df['aporte'].sum()
    #print(df.columns)
    return round(totalParcela+totalAporte,2)

  def totalJuros(self):
    df = self.calcular(self.v_aporte,self.periodo_aporte)
    return round(df["juros"].sum(),2)

  def tabela(self):
    return self.calcular(self.v_aporte,self.periodo_aporte)
    
   
divida = 118205.05
tempo = 360 # meses 
taxa_seguro = 32.83/divida # % 0,0284
tarifas = 25
juros_nominais = 7.66 # % anual
cet = 10.47 # custo efetivo total
v_aporte = 10000 
periodo_aporte = 12
aporte_anual = 24000

fin = Financiamento(divida,juros_nominais,tempo,cet,aporte_anual/2,6)
fin2 = Financiamento(divida,juros_nominais,tempo,cet,aporte_anual,12)
fin3 = Financiamento(divida,juros_nominais,tempo,cet,aporte_anual/4,3)
fin4 = Financiamento(divida,juros_nominais,tempo,cet,10,361)

print(f"tempo de financiamento com 4 aportes de {aporte_anual/4}: {fin3.tempoTotal()} meses")
print(f"tempo de financiamento com 2 aportes de {aporte_anual/2}: {fin.tempoTotal()} meses")
print(f"tempo de financiamento com 1 aporte de {aporte_anual}: {fin2.tempoTotal()} meses")

print(f"valor total do financiamento com 4 aportes de {aporte_anual/4}: {fin3.valorTotal()} ")
print(f"valor total do financiamento com 2 aportes de {aporte_anual/2}: {fin.valorTotal()} ")
print(f"valor total do financiamento com 1 aporte de {aporte_anual}: {fin2.valorTotal()} ")

fin3.tabela()['juros'].cumsum().plot()
fin2.tabela()['juros'].cumsum().plot()
fin.tabela()['juros'].cumsum().plot()
