# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:40:34 2022

@author: Tina Liu
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

### setting matplotlib font sizes
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

st.title('LEXEO Regulatory Affairs: Correspondence Database')

### load database file

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = pd.read_csv("test.csv")
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


### display raw data
st.subheader('Regulatory Correspondence')
st.write("Find the original excel file [here](https://lexeotx.sharepoint.com/:x:/r/sites/RegulatoryGroup/RG%20Administrative/Tina/Correspondence%20database.xlsx?d=wbd8eb268ac6f4de09b648ec42417b939&csf=1&web=1&e=J1RrNz).")
'''
This site is better used to make visual analytics. To look at specific correspondence, it is recommended to access the original excel file. 
However, you can make basic searches here! To search for a keyword, click on cell in the table and use CMD+F to bring up the search bar :)
'''
st.write(data)

### format page into 2 columns - 1 for pie chart, 1 for keywords 
col1, col2 = st.columns([1, 1])

### create piechart for column of interest  
col1.header("Make pie chart analytics")

# selectbox to choose column of interest
option = col1.selectbox(
    'Create a pie chart for a column:',
     data.columns)

pie = data.groupby(option)[option].count()

col1.subheader('Pie chart for ' + option)

def pieChart():
    fig = plt.figure(figsize=(4,4))
    plt.pie(pie, labels=pie.index,autopct='%.1f',)
    col1.pyplot(fig)
    
pieChart()


### keyword bar graph 
col2.header("Top Keywords")

# separate keywords into list
kw_unsplit = list(data["Keywords"])
kw_list = []

for element in kw_unsplit:
    if type(element) == str:
        kw_list += element.lower().split("; ")
        
# make dict of keywords and counts
kw_dict = {}
for kw in kw_list:
    if kw in kw_dict:
        kw_dict[kw] += 1
    else:
        kw_dict[kw] = 1

# convert dict into dataframe
kw_df = pd.DataFrame.from_dict(kw_dict, orient='index')
kw_df.columns = ['count']

# slide to display certain number of keywords
x = col2.slider('Display the top ___ keywords',min_value=1,max_value=20,value=10)

# bar graph of top keywords   
def keywords(x):
    kw_counted = kw_df.sort_values(by = ['count'],ascending=False).head(x)
    fig = plt.figure(figsize=(4,4))
    bar = plt.bar(kw_counted.index,height = kw_counted['count'])
    plt.xticks(rotation='vertical')
    plt.bar_label(bar)
    col2.pyplot(fig)
    
keywords(x)



