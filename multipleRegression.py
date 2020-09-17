import os
import pandas as pd
import requests
import json
import math
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
import statsmodels.api as sm
import numpy as np


file='Covid_result_with_PCA.txt'

df=pd.read_table(file)
print(df.info())


df['intercept']=1.0
ind_var=['PC1','PC2','PC3','PC4','PC5','intercept']
logit=sm.Logit(df['final_result'],df[ind_var])
result=logit.fit()
print(result.summary())

for i in ind_var:
    print(i + '\t p value is: '+ str(result.pvalues.loc[i]))
