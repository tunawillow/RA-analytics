# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:40:34 2022

@author: Tina Liu
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### setting matplotlib font sizes
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

### define functions
def pieChart(option,features):
    # Display percentage? 
    if features:
        pct='%.1f' 
    else:
        pct = ''
    # build chart    
    pie = data.groupby(option)[option].count()
    fig = plt.figure(figsize=(4,4))
    plt.pie(pie, labels=pie.index,autopct=pct)
    col1.pyplot(fig)
    
# bar graph of top keywords   
def keywords(x):
    kw_counted = kw_df.sort_values(by = ['count'],ascending=False).head(x)
    fig = plt.figure(figsize=(4,4))
    bar = plt.barh(kw_counted.index, width = kw_counted['count']) # horizontal bar graph
    ax = plt.gca()
    ax.invert_yaxis() # most frequent keyword is on top
    
    if display_count: 
        plt.bar_label(bar)
    col2.pyplot(fig)
    

st.title('LEXEO Regulatory Affairs: Correspondence Database')

st.write("Find the original excel file [here](https://lexeotx.sharepoint.com/:x:/s/RegulatoryGroup/EZ_cepeDLUhKoaMpKHD3xD4BVhmlCIzK-jKiJe0q7SFFBA?e=3fHYr5).")
'''
This site is better used to make visual analytics. To look at specific correspondence, it is recommended to access the original excel file. 
However, you can make basic searches here! To search for a keyword, click on cell in the table and use Ctrl+F to bring up the search bar :)
'''

### upload database file
file = st.file_uploader('Upload the database Excel file here.')

if file is not None:
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = pd.read_excel(file, usecols=[0,1,2,3,4,5,6,7,8,9,10])
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done!")
    st.write(data)

    ### format page into 2 columns - 1 for pie chart, 1 for keywords 
    col1, col2 = st.columns([1, 1.3])
    
    ### create piechart for column of interest  
    col1.header("Make pie chart analytics")
    
    # selectbox to choose column of interest
    pie_option = col1.selectbox(
        'Create a pie chart for a column:',
         data.columns)
    
    # piechart features
    pie_features = col1.checkbox('Display percentage')
    
    # make the piechart
    col1.subheader('Pie chart for ' + pie_option)
        
    pieChart(pie_option,pie_features)
    
    
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
    kw_number = col2.slider('Display the top ___ keywords',min_value=1,max_value=20,value=10)
    
    # display count?
    display_count = col2.checkbox('Display keyword counts')
        
    keywords(kw_number)
