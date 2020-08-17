import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot


covid19_testfile='covid19_result_0806'


# re_organize the test result by eid
# data will be re_organized using dictionary
# dictionary is very common data format, and can easily convert to dataframe. It is easy for beginner
# In this script, I will try to avoid use dataframe. Later we will mostly use dataframe

# Here we want to want summarize the test result, number of tests, number of positive tests, test date of each subject (unique eid),

# for final test result, if any test shows positive, then positive, otherwise negative
# for test date, earliest positive date or latest negative date

def latestDate(dateList):
    #the origin date format is DD/MM/YYYY, we will change to YYYY/MM/DD, then we can sort the string
    revised_dateList=[]
    for d in dateList:
        d_old=d.split('/')
        d_old.reverse()
        revised_dateList.append('/'.join(d_old))

    #sort date
    revised_dateList.sort()
    #return last element
    return revised_dateList[-1]

def earliestDate(dateList):
    #the origin date format is DD/MM/YYYY, we will change to YYYY/MM/DD, then we can sort the string
    revised_dateList=[]
    for d in dateList:
        d_old=d.split('/')
        d_old.reverse()
        revised_dateList.append('/'.join(d_old))
    #sort date
    revised_dateList.sort()
    #return first element
    return revised_dateList[0]




#get unique IDs of test objects
#There are many ways to get unique IDs. Here I just walk through all file to get eid using set. 

eidList=set([])

f=open(covid19_testfile+'.txt','r')
#skip header
f.readline()

# n for total test number. each row is one test
n=0
for l in f:
    eid=l.split('\t')[0]
    eidList.add(eid)
    n += 1

f.close()

print('There are total %s tests and %s unique IDs.' % (n,len(eidList)))

#sort eid
eidList=list(eidList)
eidList.sort()

print('Sorting eid is done.')
print('First 5 eid:')
print(eidList[:5])


#now for each ID, create a dictionary

result=[]

for eid in eidList:
    eid_tests={
        'eid':eid,
        # list all test result of this subject
        'tests': [],      
        #list all positive test result of this subject
        'positive_tests':[],
        #list all test date
        'test_date':[],
        #list all positive test date
        'positive_test_date':[]
        }
    result.append(eid_tests)

#walk through file again to add test result and date


f=open(covid19_testfile+'.txt','r')
f.readline()

for l in f:
    info=l[:-1].split('\t')
    eid=info[0]
    #this single test result and date
    s_result=info[5]
    s_date=info[1]


    #in result list, find match eid
    for r in result:
        if(r['eid'] == eid):
            #add test result
            r['tests'].append(s_result)
            #add positive test result
            if(s_result == '1'):
                r['positive_tests'].append(s_result)
                r['positive_test_date'].append(s_date)
            r['test_date'].append(s_date)
            #since the eid is unique, once you find match eid, you don't need go through the rest eids.
            break
f.close()

#write result to new file
#new file use same name, but different extension, so we can identify file easily

f=open(covid19_testfile+'.by_eid','w+')

f.write('eid\t#tests\t#positive_test\tfinal_result\tfinal_date\n')


for r in result:
    total_test=len(r['tests'])
    total_positive=len(r['positive_tests'])
    final_result=0
    final_date=''
    if(total_positive>0):
        final_result=1
    if(final_result == 0):
        final_date=latestDate(r['test_date'])
    else:
        final_date=earliestDate(r['positive_test_date'])
    f.write(r['eid']+'\t'+str(total_test)+'\t'+str(total_positive)+'\t'+str(final_result)+'\t'+final_date+'\n')
f.close()
        


#use dataframe to draw some figures

df=pd.read_table(covid19_testfile+'.by_eid')
print(df.info())

test_result=[0,1]
subs=[df['eid'][df['final_result']==0].count(),df['eid'][df['final_result']==1].count()]
trace = go.Pie(labels = test_result, values = subs)
data=[trace]
fig=go.Figure(data = data)
fig.update_layout(title="Covid test positive by subjects")
fig.write_image(covid19_testfile+"positive_rate.png")



plt.title('# subject by total test number')
sns.distplot(df['#tests'],kde=False)
plt.xticks(np.arange(0, df['#tests'].max(), step=1))
plt.autoscale(enable=True, axis='both', tight=None)
plt.savefig(covid19_testfile+"_test_distribution.png")








































