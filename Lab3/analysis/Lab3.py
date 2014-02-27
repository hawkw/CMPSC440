# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # CMPSC440 Lab 3 Data Analysis
# **Hawk Weisman**
# 
# In this notebook, we will analyze and plot data collected from the producer-consumer model experiment carried out in Laboratory Assignment 3 for Computer Science 440: Principles of Operating Systems.

# <codecell>

# First, set up the environment for analysis and graphing.
# We will be using pandas for handling our data.
import pandas

# Paths to the directory where the data is stored and to where figures will be saved.
datapath = "/Users/hawk/Documents/DOCUMENTS/School/2014S/CMPSC440/Lab3/data/"
figpath = "/Users/hawk/Documents/DOCUMENTS/School/2014S/CMPSC440/Lab3/figures/"

# Read the CSV file for the experiment and print out a summary.
experiment = pandas.read_csv(datapath + "lrgexperiment 2014-02-18 12:32:49.592060.csv")
print experiment

# <codecell>

# get mean times for each data/consumers combination
means = experiment.groupby(['consumers', 'data']).mean()

# get standard deviations as well
means['std dev'] = experiment.groupby(['consumers', 'data']).std()['time']

# drop the replicates column from the means dataframe
# we don't need this any more
means = means.drop(['replicate'], 1)

print means

# <codecell>

# output the processed dataset to a file
means.to_csv(datapath + "means.csv")

# <codecell>

# set up the environment for plotting

from scipy import stats
from pylab import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline

# <codecell>

# Plot the relationship between time and number of data items

consumers = [2,4,6,8,10,12]

with sns.palette_context('husl'):

    plt.figure(figsize=(8,8))
    ax = plt.gca()

    for count in consumers:
        segment = means.loc[count].reset_index()
        segment.plot(y='time', x='data', label='{0} consumers'.format(count))
        
    plt.xlabel('Number of data items')
    plt.ylabel('Time (seconds)')
    plt.title('Time vs. Number of Data Items for Varying Numbers of Consumers')
    plt.legend()
    plt.savefig(figpath + 'timevsdatas.pdf')
    plt.show()

# <codecell>

# Since every line fell pretty much over each other in the last plot, 
# let's try a separate plot for each number of consumers
mpl.rc("figure", figsize=(4, 4))
# we're gonna use the lmplot() function from the Seaborn package for this.
sns.lmplot('data', 'time', experiment, color = 'consumers', col = 'consumers', col_wrap = 2)
plt.savefig(figpath + 'lmplot.pdf')

# <codecell>

# Plot the correlation heatmap for the dataset
mpl.rc("figure", figsize=(5, 5))
sns.corrplot(experiment)
plt.savefig(figpath + 'corrplot.pdf')

# <codecell>


