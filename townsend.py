import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



df=pd.read_table('covid19_result_0806.by_eid')
print(df.info())


covid_positive=list(df['eid'][df['final_result']==1])
covid_negative=list(df['eid'][df['final_result']==0])

del df


df=pd.read_table('Covid_information_20-08-18.csv')
print(df.info())



plt.title('Townsend deprivation index')
sns.distplot(df['189-0.0'][df['eid'].isin(covid_positive)],color = 'yellow')
sns.distplot(df['189-0.0'][df['eid'].isin(covid_negative)],color = 'red')
plt.show()
                    
