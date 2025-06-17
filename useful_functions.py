import numpy as np
import pickle
import random
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as stats
from scipy.stats import t

import pandas as pd
pd.set_option('display.max_columns', None)

def coleta_estatisticas(query):
    dic = {}
    values = []
    describe = query['NU_NOTA_MT'].describe()


    
    media = describe['mean'].round(2)
    mediana = describe['50%'].round(2)
    std = describe['std'].round(2)
    n = query['NU_NOTA_MT'].shape[0]
    
    values.append(media)
    values.append(mediana)
    values.append(std)
    values.append(n)

    dic[query.loc[0, 'Q006']] = values

    return dic

def test_t(estatisticas1, estatisticas2, faixa):

    faixa = list(estatisticas1.keys())[0]

    
    mean1 = estatisticas1[faixa][0]
    mean2 = estatisticas2[faixa][0]
    
    std1 = estatisticas1[faixa][2]
    std2 = estatisticas2[faixa][2]
    
    n1 = estatisticas1[faixa][3]
    
    n2 = estatisticas2[faixa][3]
    
    se = np.sqrt((std1**2)/n1 + (std2**2)/n2)
    t_stat = (mean1 - mean2) / se
    
    
    ndf = ( (std1**2 / n1 + std2**2 / n2)**2 ) / (
        ((std1**2 / n1)**2 / (n1 - 1)) + ((std2**2 / n2)**2 / (n2 - 1))
    )
    
    # Two-tailed p-value
    p_value = 2 * t.sf(np.abs(t_stat), ndf)
    
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        print(f"A diferença de {abs(mean1 - mean2).round(3)} É estatísticamente significante!")
    else:
        print(f"A diferença de {abs(mean1 - mean2).round(3)} é NÃO estatísticamente significante!")