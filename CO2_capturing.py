#!/usr/bin/env python
# coding: utf-8

# In[1]:



# # <center> Co2 Capturing <br> <br>    <font size='4'>$\color{purple}{\text{Mahmoud Maheri}}$
# 
# 

#  

# # Importing libreries
# 



import os
import shap
import random
import warnings
import matplotlib
import tensorflow
import latextable
import numpy as np
import pandas as pd 
import seaborn as sns
from math import sqrt
import tensorflow as tf
from scipy import stats
import missingno as msno
import plotly.express as px
from tensorflow import keras
import statsmodels.api as sm
from keras import backend as K
from texttable import Texttable
import matplotlib.pyplot as plt
from keras.layers import Dropout
import plotly.graph_objects as go
from scipy.stats import pearsonr
from sklearn.utils import shuffle
from relativeImp import relativeImp
from tensorflow.keras import models
from sklearn.metrics import r2_score
from numpy import arange,mean,std,absolute
from pandas.plotting import scatter_matrix
from sklearn.feature_selection import RFECV
from scikeras.wrappers import KerasRegressor
from tensorflow.keras.optimizers import Adam
from sklearn.ensemble import BaggingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from matplotlib.font_manager import FontProperties
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import QuantileTransformer
from sklearn.inspection import plot_partial_dependence
from sklearn.ensemble import GradientBoostingRegressor
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv1D, Dense, Flatten
from IPython.core.interactiveshell import InteractiveShell  
from sklearn.feature_selection import mutual_info_regression
from sklearn.model_selection import RepeatedKFold, cross_validate

np.set_printoptions(precision=6)
plt.rcParams['figure.dpi'] = 100
warnings.filterwarnings("ignore")
plt.rcParams['figure.figsize'] = (6, 4)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
InteractiveShell.ast_node_interactivity = "all"
plt.rcParams['image.interpolation'] = 'spline16'
pd.options.display.float_format = "{:.4f}".format
#InteractiveShell.ast_node_interactivity = "last_expr"


# In[2]:



warnings.filterwarnings("ignore")
InteractiveShell.ast_node_interactivity = "all"
pd.options.display.float_format = "{:.4f}".format
#InteractiveShell.ast_node_interactivity = "last_expr"
np.set_printoptions(precision=6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (6, 4)
plt.rcParams['image.interpolation'] = 'spline16'


# print(scores)
# print(r2_score(y_train, train_preds))
# print(r2_score(y_test, test_preds))
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# # Importing Dataset


# In[3]:


# Dataset imported, and a copy has been generated for future feature utilization.
df = pd.read_excel("Processed 527 datapoints.xlsx")
BWDPS=df.copy()
BWDPSf=df.copy()
BWDPSm=df.copy()


# In[4]:


# Extracting Initial Insights from the Dataset
print(' shape of data set is = ',df.shape)
print()
print(' shape of data set is = ',BWDPS.shape)
print()
print(' shape of data set is = ',BWDPSf.shape)
print()
print(' dataset head:\n')
df.head()
print()
print(' dataset info:\n')
dfinfo=df.info()
print()
print(' describtion of data set:\n')
df_des=df.describe().transpose()
df_des
df_firstf=BWDPSf[:193]
df_firstf.describe().transpose()
df_secondf=BWDPSf[193:]

df_secondf.describe().transpose()


# # Distribution and analysing dataset


# In[5]:


# Exploring Data Distribution through Analysis and Visualization
plt.figure(dpi=200)
plt.style.use('fivethirtyeight')
BWDPSf.plot(subplots=True,
        layout=(6, 2),
        figsize=(22,22),
        fontsize=10, 
        linewidth=2,
        sharex=False)
plt.show()


# In[6]:


#disribution of the primary dataset
plt.figure(dpi=200)
BWDPSf.plot(kind='density',subplots=True,layout=(4, 3), figsize=(22,22),
           fontsize=10, linewidth=2, sharex=False);
plt.show()


# In[7]:


#CO2 uptake by box plot for the primary dataset

fig = px.box(BWDPSf, y="CO2 uptake (mmol/g)")
fig.show()


# In[8]:


#This code creates a pair of plots using matplotlib and seaborn. 
#The first plot is a boxplot showing the distribution of CO2 uptake values at 25°C temperature. 
#The second plot is a corresponding histogram. Both plots include markers for mean and median values. 
#The goal is to visualize and compare the distribution of CO2 uptake data.

f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw= {"height_ratios": (0.2, 1)},
                                    figsize=(8, 6), dpi = 400)

sns.boxplot(BWDPSf["CO2 uptake (mmol/g)"][BWDPSf["Temp (°C)"] == 25], ax=ax_box , color='skyblue',linewidth=1.7
            ,medianprops = dict(color="red",linewidth=1.7))

ax_box.set(xlabel='')
sns.distplot(BWDPSf["CO2 uptake (mmol/g)"][BWDPSf["Temp (°C)"] == 25], ax=ax_hist, color='skyblue')

plt.axvline(BWDPSf["CO2 uptake (mmol/g)"][BWDPSf["Temp (°C)"] == 25].median(), color = 'red',linewidth=1.7)
plt.axvline(BWDPSf["CO2 uptake (mmol/g)"][BWDPSf["Temp (°C)"] == 25].mean(), color = "blue",
            linestyle='--',linewidth=1.7)

plt.text(5, .3,'Mean= %.2f'%BWDPSf["CO2 uptake (mmol/g)"][BWDPSf["Temp (°C)"] == 25].mean(), color='blue')
plt.text(5, .2,'Median= %.2f'%BWDPSf["CO2 uptake (mmol/g)"][BWDPSf["Temp (°C)"] == 25].median(), color='r')

ax_box.set(xlabel='')
plt.show()


# In[9]:


df_first1=BWDPSf[:193]
df_first2=BWDPSf[193:]


# In[10]:


# BWDPSf["CO2 uptake (mmol/g)"]

def density_features_manual(dataset, feature_name):
    '''The purpose of this function is to create a standardized way to visualize the distribution 
    of a specific feature within different datasets.
    The function takes two arguments: the dataset and the name of the feature to visualize. It uses 
    seaborn to create a histogram with a blue color, adds vertical lines for the mean and median values
    in red and blue respectively'''
    print(dataset.columns)
    sns.set(style="darkgrid")

    # Define the figure and axis
    f, ax_hist = plt.subplots(figsize=(8, 6), dpi=400)

    # Plot the histogram
    sns.distplot(dataset[feature_name], ax=ax_hist, color='skyblue')

    # Plot vertical lines for mean and median
    plt.axvline(dataset[feature_name].median(), color = 'red', linewidth=1.7)
    plt.axvline(dataset[feature_name].mean(), color = "blue", linestyle='--', linewidth=1.7)

    # Add text labels for mean and median
    plt.text(6, .30, 'Mean   = %.2f' % dataset[feature_name].mean(), color='blue')
    plt.text(6, .25, 'Median= %.2f' % dataset[feature_name].median(), color='red')

    plt.xlabel(feature_name, fontsize=18)
    plt.ylabel('Density', fontsize=18)
    plt.show()


# In[11]:


def density_features(dataset, feature_name='Surface Area (m2/g)'):
    '''The purpose of this function is to create a standardized way to visualize the distribution 
    of a specific feature within different datasets.
    The function takes two arguments: the dataset and the name of the feature to visualize. It uses 
    seaborn to create a histogram with a blue color, adds vertical lines for the mean and median values
    in red and blue respectively based on the feture max and min values'''
    print(dataset.columns)
    sns.set(style="darkgrid")

    # Define the figure and axis
    f, ax_hist = plt.subplots(figsize=(8, 6), dpi=400)

    # Plot the histogram
    sns.distplot(dataset[feature_name], ax=ax_hist, color='skyblue')

    # Plot vertical lines for mean and median
    mean_value = dataset[feature_name].mean()
    median_value = dataset[feature_name].median()
    plt.axvline(median_value, color='red', linewidth=1.7)
    plt.axvline(mean_value, color="blue", linestyle='--', linewidth=1.7)

    # Add text labels for mean and median
    plt.text(mean_value, ax_hist.get_ylim()[1] * 0.9, 'Mean   = %.2f' % mean_value, color='blue', ha='center')
    plt.text(median_value, ax_hist.get_ylim()[1] * 0.85, 'Median = %.2f' % median_value, color='red', ha='center')

    plt.xlabel(feature_name, fontsize=18)
    plt.ylabel('Density', fontsize=18)
    plt.show()


# Example usage


# In[12]:


density_features_manual(BWDPSf, 'CO2 uptake (mmol/g)') 


# In[13]:


density_features(BWDPSf, 'CO2 uptake (mmol/g)') 


# In[14]:


fig = px.violin(BWDPS, y="CO2 uptake (mmol/g)", x="Temp (°C)",
                color=BWDPSf["Temp (°C)"] , box=True, points="all", hover_data=['CO2 uptake (mmol/g)'])
fig.show()


# In[15]:


fig = px.violin(BWDPS, y="CO2 uptake (mmol/g)", x="Pressure (bar)", 
                color=BWDPSf["Pressure (bar)"] , box=True, points="all", hover_data=['CO2 uptake (mmol/g)'])
fig.show()


# In[16]:


#effect of adsorption in different presures
df_first1=BWDPSf[:193]
df_first2=BWDPSf[193:]

fig = go.Figure()

presures = [0.1, 0.15, 1.0, 1.013]

for pres in presures:
    fig.add_trace(go.Violin(x=BWDPSf['Pressure (bar)'][BWDPSf['Pressure (bar)'] == pres],
                            y=BWDPSf['CO2 uptake (mmol/g)'][BWDPSf['Pressure (bar)'] == pres],
                            name=pres, box_visible=True, meanline_visible=True))

fig.show()


# ## relative importance of features


# In[17]:


#relative importance of features

yName = 'CO2 uptake (mmol/g)'
xNames = ['Surface Area (m2/g)', 'Total Pore Volume(cm3/g)',
       'Micropore Volume (cm3/g)', 'C (%)', 'H (%)', 'N (%)', 'O (%)', 'S (%)',
       'Temp (°C)', 'Pressure (bar)']

df_results = relativeImp(BWDPSf, outcomeName = yName, driverNames = xNames)
df_results=df_results.sort_values('normRelaImpt',ascending=False)
df_results


# In[18]:


#plt.plot(df_results['normRelaImpt'])
plt.plot(sorted(df_results['normRelaImpt']))


# # initial data processing of primary dataset


# In[19]:


def missing_values(dataset):
    '''This function identifies and returns a list of column names in the given dataset that
    contain missing values.'''
    missing = dataset.columns[dataset.isnull().any()].tolist()
    return missing
def print_missing_values(dataset):
    '''This function prints the names of columns with missing values and then displays
    the corresponding count of missing values in those columns. The goal of these functions
    is to help identify and understand missing data within a dataset.'''
    missing_values(dataset)
    print('missing values based on attibutes are in columns:\n')
    dataset[missing_values(dataset)].isnull().sum()
    print()


# In[20]:


# BWDPS is the primary dataset
missing_values(BWDPS)


# In[21]:


def imputation(dataset, target):
    '''The code defines a function, imputation, that uses a Random Forest Regressor to fill in missing values
    in a target column based on the "Surface Area (m2/g)" feature. It trains the model, predicts missing values,
    and adds them as a new column.'''
    
    dataset_mv = dataset[["Surface Area (m2/g)", target]].copy()
    print(dataset_mv)

    dataset_mv = dataset_mv.dropna()
    print(dataset_mv)


    x = np.array(dataset_mv["Surface Area (m2/g)"]).reshape(-1,1)
    y = np.array(dataset_mv[target]).reshape(-1,1)

    x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2, random_state = 42)

    print("Random Forest: ")
    rf = RandomForestRegressor(random_state =42)
    rf.fit(x_train, y_train)
    pred = rf.predict(x_test)
    scores = cross_val_score(rf, x_train, y_train , cv=5, scoring='r2')
    score = np.mean(scores)
    print("Train R2: %.2f (+/- %.2f) \n" %(score, scores.std()))
    print("Test R2: %.2f \n" %(r2_score(y_test, pred)))


    print(len(x))

#     print(x[:10])
#     print(y[:10])
    name = target + "_imputed"
    p = rf.predict(np.array(dataset["Surface Area (m2/g)"]).reshape(-1,1))
    dataset[name] = p
    return dataset


# In[22]:


#BWDPS_poly is dataset that missing values will be filled by three order Newton interpolation 
BWDPS_poly=BWDPS.copy()


# In[23]:


imputation(BWDPS, "Total Pore Volume(cm3/g)")
imputation(BWDPS, "Micropore Volume (cm3/g)")


# In[24]:


#dropping imputed columns
BWDPS["Total Pore Volume(cm3/g)"] = BWDPS["Total Pore Volume(cm3/g)"].fillna(BWDPS["Total Pore Volume(cm3/g)_imputed"])
BWDPS["Micropore Volume (cm3/g)"] = BWDPS["Micropore Volume (cm3/g)"].fillna(BWDPS["Micropore Volume (cm3/g)_imputed"])


# In[25]:


#BWDPSs is the primary dataset that Sulphur feature is kept
BWDPSs = BWDPS.drop(['Total Pore Volume(cm3/g)_imputed','Micropore Volume (cm3/g)_imputed'], axis = 1)


# In[26]:


BWDPS = BWDPSs.drop(['S (%)'], axis = 1)


# In[27]:


# BWDPS_poly is the dataset which missing values will be filled using Newton's three order interpolation method
BWDPS_poly


# ##
# because of the high correlation between columns $\color{blue}{\text{ "Total Pore Volume(cm3/g)"}}$ and $\color{blue}{\text{ "Micropore Volume (cm3/g)"}}$ to column $\color{blue}{\text{ "Surface Area (m2/g)"}}$, missed values will be filled by imputation.
# 
# Also, We applied Newton three oreder interpolation for imputation.


# In[28]:


def _poly_newton_coefficient(x, y):
    '''This function calculates the divided differences coefficients for the Newton polynomial
    interpolation. It takes two arrays, x and y, representing the data points and their corresponding 
    function values. It iteratively computes the divided differences coefficients and returns them.'''
    
    m = len(x)

    x = np.copy(x)
    a = np.copy(y)
    for k in range(1, m):
        a[k:m] = (a[k:m] - a[k - 1])/(x[k:m] - x[k - 1])

    return a

def newton_polynomial(x_data, y_data, x):
    '''This function uses the divided differences coefficients from _poly_newton_coefficient
    to perform Newton polynomial interpolation. It takes three arguments: x_data and y_data represent
    the known data points, and x is the point at which the polynomial is evaluated. The function calculates
    the interpolated value using the Newton polynomial interpolation formula and returns it.'''
    a = _poly_newton_coefficient(x_data, y_data)
    n = len(x_data) - 1  # Degree of polynomial
    p = a[n]

    for k in range(1, n + 1):
        p = a[n - k] + (x - x_data[n - k])*p

    return p


# In[29]:


def poly_imputation(dataset, target):
    '''The poly_imputation function uses polynomial interpolation to fill missing values in the target
    column of a dataset. It finds nearby data points, performs interpolation, and adjusts negative values
    if necessary. The imputed values are added to the dataset and used to replace the original target column.'''
    
    dataset_mv = dataset[["Surface Area (m2/g)", target]].copy()

    
    x1 = np.array(dataset_mv["Surface Area (m2/g)"])#.reshape(-1,1)
    y1 = np.array(dataset_mv[target])#.reshape(-1,1)

    xx=x1
    yy=y1

    for i in range(len(y1)):

        if np.isnan(y1[i]):

            print(i)
            y1[i]
            x2=np.array([  xx[i-4],  xx[i-3],xx[i-2],xx[i-1]])
            print(x2)

            for j in range(len(x2)):
                if x2[j]==x2[j-1]:
                    x2[j]=x2[j]+0.001
            print(x2)

            y2=np.array([ yy[i-4],  yy[i-3],yy[i-2],yy[i-1]])
            print(y2)

            for j in range(len(y2)):
                if y2[j]==y2[j-1]:
                    y2[j]=y2[j]+0.001
            print(y2)

            x2,y2=zip( *sorted( zip(x2, y2) ) )

            x2=np.array(x2)
            y2=np.array(y2)

            if xx[i]<=x2[0]:
                x3=xx[i]+(x2[0]-xx[i])-10#(x2[0]-xx[i])/100
                
            elif x2[0]<xx[i]<x2[1] :
                x3=xx[i]+(-xx[i]+x2[1])-10
                
            elif x2[1]<xx[i]<x2[2] :
                x3=xx[i]+(-xx[i]+x2[2])-10
                
            elif x2[2]<xx[i]<x2[3] :
                x3=xx[i]+(-xx[i]+x2[3])-10
                
            else:
                x3=xx[i]-(xx[i]-x2[3])-10#(-x2[0]+xx[i])/100

            p=newton_polynomial(x2, y2,x3 )

            if p<0:
                p=p*(-1)

            print(x2,xx[i],x3)
            print(y2,p)
            y1[i]=p

    print(y1[:8])

    name = target + "_poly_imputed"
    p = y1   #rf.predict(np.array(dataset["Surface Area (m2/g)"]).reshape(-1,1))
    dataset[name] = p
    dataset[target] = p
    return dataset


# In[30]:


poly_imputation(BWDPS_poly, 'Micropore Volume (cm3/g)')


# In[31]:


poly_imputation(BWDPS_poly,"Total Pore Volume(cm3/g)")


# In[32]:


BWDPS_poly=BWDPS_poly.drop(['Total Pore Volume(cm3/g)_poly_imputed','Micropore Volume (cm3/g)_poly_imputed'],axis=1)
BWDPS_poly


# In[33]:


#some new datasets
df_first=BWDPS[:193] #RPC dataset
df_second=BWDPS[193:] #BDPC dataset

BWDPS_shuffled=BWDPS.sample(frac=1)
df_first_shuffled = df_first.sample(frac=1)
df_second_shuffled = df_second.sample(frac=1)

BWDPSs_shuffled=BWDPSs.sample(frac=1)

df_original= BWDPS
df_original_shuffled=df_original.sample(frac=1)

df_first_poly=BWDPS_poly[:193]
df_second_poly=BWDPS_poly[193:]

BWDPS_poly_shuffled=BWDPS_poly.sample(frac=1)
df_first_poly_shuffled = df_first_poly.sample(frac=1)
df_second_poly_shuffled = df_second_poly.sample(frac=1)



df_original= BWDPS
df_original_shuffled=df_original.sample(frac=1)


# In[34]:


def primary_code(dataset,n,size,case):
    '''The primary_code function performs machine learning regression analysis. It includes
    steps for data scaling, model training, evaluation, cross-validation, scatterplot visualization,
    and feature importance analysis. The function provides insights into the model's performance and 
    the impact of different features on the target prediction.'''
    
    case_name=['cross validation using x_train', 'cross validation using x']
    
    print(case_name[case],'\n')
    print('Dataset shape: ',dataset.shape)
    x = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)

    
    matplotlib.rcParams['font.sans-serif'] = 'Times New Roman'
    label_size = 20
    matplotlib.rcParams['xtick.labelsize'] = label_size 
    matplotlib.rcParams['ytick.labelsize'] = label_size 


    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    
    scaler_Min =scalers[n]
    if n==0:
        x_train=x_train
        x_test=x_test
        x=x
    else:
        x_train = scaler_Min.fit_transform(x_train)
        x_test = scaler_Min.fit_transform(x_test)
        x = scaler_Min.fit_transform(x)
    
    

    model =  GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1, min_samples_split = 2, 
                                       n_estimators = 300, subsample = 0.5, random_state=42)

    model.fit(x_train, y_train)

    print("The training R2 is: %.2f" % (model.score(x_train, y_train)*100))
    print("The test R2 is: %.2f "% (model.score(x_test, y_test)*100))

    

    y_predicted = model.predict(x_test)

    print("MSE: %.2f"% mean_squared_error(y_test, y_predicted))
    print("RMSE: %.2f"% sqrt(mean_squared_error(y_test, y_predicted)))
    
    if case==0:
        train_x=x_train
        train_y=y_train
        x=x
    else:
        train_x = x
        train_y = y

    accuracies = cross_val_score(estimator = model, X = train_x, y=train_y, cv=5)
    scores = cross_validate( model, X=x, y=y, scoring='r2')

    sorted(scores.keys())

    
    
    print("The mean training accuracy is: %.2f"% (accuracies.mean()*100))
    print("The standard daviation training accuracy is: %.2f"% (accuracies.std()*100))
    print("fit times: ", scores['fit_time'])


    pp_tr = model.predict(x_train)

    
    g1 = sns.JointGrid(data=x_test, x=y_test, y=y_predicted)
    
    sns.scatterplot(data=x_train,x=y_train, y=pp_tr, s=100, color='orange', ax=g1.ax_joint)
    sns.scatterplot(data=x_test,x=y_test, y=y_predicted, s=100, color='blue', ax=g1.ax_joint)
   
    sns.regplot(data=x_test,x=y_test, y=y_predicted, ax=g1.ax_joint)
    sns.regplot(data=x_train,x=y_train, y=pp_tr, ax=g1.ax_joint)

    plt.ylim(0, 8.5)
    plt.xlim(0, 8.5)

    g1.set_axis_labels("Actual CO\u2082 adsorbed (mmol/g)", "Predicted CO\u2082 adsorbed (mmol/g)", fontsize =14, fontname = 'Times New Roman')
    sns.histplot(data=x_train,x=y_train,ax=g1.ax_marg_x, color ='orange')
    sns.histplot(data=x_test,x=y_test, ax=g1.ax_marg_x, color ='blue')
    g1.ax_marg_x.legend(["Train", "Test"])

    plt.show()
    names = dataset.columns[0:len(dataset)]

    perm_importance = permutation_importance(model, x_train, y_train)

    sorted_idx = perm_importance.importances_mean.argsort()
    plt.barh(names[sorted_idx], perm_importance.importances_mean[sorted_idx])
    plt.xlabel("Permutation Importance")

   
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    
    
    feature_name='O (%)'
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300, facecolor='#FFFFFF')
    plot_partial_dependence(model, x_train,[feature_name],feature_names = names,
                            target = 0, n_jobs = 3, grid_resolution = 50,ax=ax)
        
    ax = plt.gca()
    ax.set_facecolor('#FFFFFF')
    plt.xlabel(f'{feature_name}', color='black', fontsize =18)
    plt.ylabel('Partial dependence', color='black', fontsize =18)
    plt.tick_params(axis='x', labelsize=22, colors='black')
    plt.tick_params(axis='y', labelsize=22, colors='black')
    plt.grid(True, color='lightgray')
    for line in ax.get_lines():
        line.set_color('blue')
    plt.show()


# In[35]:


def primary_code_s(dataset,n,size,case):
    '''The primary_code_s function performs machine learning regression analysis by shuffling. It includes
    steps for data scaling, model training, evaluation, cross-validation, scatterplot visualization,
    and feature importance analysis. The function provides insights into the model's performance and 
    the impact of different features on the target prediction.'''
    
    case_name=['cross validation just x_train', 'cross validation with whole x']
    
    print(case_name[case],'\n')
    print('Dataset shape: ',dataset.shape)
    dataset=shuffle(dataset)
    x = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)

    
    matplotlib.rcParams['font.sans-serif'] = 'Times New Roman'
    label_size = 20
    matplotlib.rcParams['xtick.labelsize'] = label_size 
    matplotlib.rcParams['ytick.labelsize'] = label_size 


    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    
    scaler_Min =scalers[n]
    if n==0:
        x_train=x_train
        x_test=x_test
        x=x
    else:
        x_train = scaler_Min.fit_transform(x_train)
        x_test = scaler_Min.fit_transform(x_test)
        x = scaler_Min.fit_transform(x)
    
    

    model =  GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1, min_samples_split = 2, 
                                       n_estimators = 300, subsample = 0.5, random_state=42)

    model.fit(x_train, y_train)

    print("The training R2 is: %.3f" % (model.score(x_train, y_train)*100))
    print("The test R2 is: %.3f "% (model.score(x_test, y_test)*100))

    

    y_predicted = model.predict(x_test)

    print("MSE: %.3f"% mean_squared_error(y_test, y_predicted))
    print("RMSE: %.3f"% sqrt(mean_squared_error(y_test, y_predicted)))
    
    if case==0:
        train_x=x_train
        train_y=y_train
        x=x
    else:
        train_x = x
        train_y = y

    accuracies = cross_val_score(estimator = model, X = train_x, y=train_y, cv=5)
    scores = cross_validate( model, X=x, y=y, scoring='r2')

    sorted(scores.keys())

    
    
    print("The mean training accuracy is: %.3f"% (accuracies.mean()*100))
    print("The standard daviation training accuracy is: %.3f"% (accuracies.std()*100))
    print("fit times: ", scores['fit_time'])


    pp_tr = model.predict(x_train)

    
    g1 = sns.JointGrid(data=x_test, x=y_test, y=y_predicted)
    
    sns.scatterplot(data=x_train,x=y_train, y=pp_tr, s=100, color='orange', ax=g1.ax_joint)
    sns.scatterplot(data=x_test,x=y_test, y=y_predicted, s=100, color='blue', ax=g1.ax_joint)
   
    sns.regplot(data=x_test,x=y_test, y=y_predicted, ax=g1.ax_joint)
    sns.regplot(data=x_train,x=y_train, y=pp_tr, ax=g1.ax_joint)

    plt.ylim(0, 8.5)
    plt.xlim(0, 8.5)

    g1.set_axis_labels("Actual CO\u2082 adsorbed (mmol/g)", "Predicted CO\u2082 adsorbed (mmol/g)", fontsize =14, fontname = 'Times New Roman')
    sns.histplot(data=x_train,x=y_train,ax=g1.ax_marg_x, color ='orange')
    sns.histplot(data=x_test,x=y_test, ax=g1.ax_marg_x, color ='blue')
    g1.ax_marg_x.legend(["Train", "Test"])

    plt.show()
    names = dataset.columns[0:len(dataset)]

    perm_importance = permutation_importance(model, x_train, y_train)

    sorted_idx = perm_importance.importances_mean.argsort()
    plt.barh(names[sorted_idx], perm_importance.importances_mean[sorted_idx])
    plt.xlabel("Permutation Importance")

   
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    
    
    feature_name='O (%)'
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300, facecolor='#FFFFFF')
    plot_partial_dependence(model, x_train,[feature_name],feature_names = names,
                            target = 0, n_jobs = 3, grid_resolution = 50,ax=ax)
    
    
    ax = plt.gca()
    ax.set_facecolor('#FFFFFF')
    #plt.plot(feature_values, pdp_values, color='red')
    plt.xlabel(f'{feature_name}', color='black', fontsize =18)
    plt.ylabel('Partial dependence', color='black', fontsize =18)
    plt.tick_params(axis='x', labelsize=22, colors='black')
    plt.tick_params(axis='y', labelsize=22, colors='black')
    plt.grid(True, color='lightgray')
    for line in ax.get_lines():
        line.set_color('red')
    plt.show()


# In[36]:


def primary_code2(dataset,n,size,case):
    '''The primary_code_s function performs machine learning regression analysis by shuffling. It includes
    steps for data scaling, model training, evaluation, cross-validation, scatterplot visualization,
    and feature importance analysis calculate the effect of different values of tempreture and pressure 
    features on CO2 uptake after shuffleing. The function provides insights into the model's performance and 
    the impact of different features on the target prediction. '''
    case_name=['cross validation using x_train', 'cross validation using x']
    
    dataset=shuffle(dataset)
    print(case_name[case],'\n')
    print('Dataset shape: ',dataset.shape)
    x = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)

    matplotlib.rcParams['font.sans-serif'] = 'Times New Roman'
    label_size = 20
    matplotlib.rcParams['xtick.labelsize'] = label_size 
    matplotlib.rcParams['ytick.labelsize'] = label_size 

    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    
    scaler_Min =scalers[n]
    if n==0:
        x_train=x_train
        x_test=x_test
        x=x
    else:
        x_train = scaler_Min.fit_transform(x_train)
        x_test = scaler_Min.fit_transform(x_test)
        x = scaler_Min.fit_transform(x)
    
    model =  GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1, min_samples_split = 2, 
                                       n_estimators = 300, subsample = 0.5, random_state=42)

    model.fit(x_train, y_train)

    print("The training R2 is: %.3f" % (model.score(x_train, y_train)*100))
    print("The test R2 is: %.3f "% (model.score(x_test, y_test)*100))

    y_predicted = model.predict(x_test)

    print("MSE: %.3f"% mean_squared_error(y_test, y_predicted))
    print("RMSE: %.3f"% sqrt(mean_squared_error(y_test, y_predicted)))
    
    if case==0:
        train_x=x_train
        train_y=y_train
        x=x
    else:
        train_x = x
        train_y = y

    accuracies = cross_val_score(estimator = model, X = train_x, y=train_y, cv=5)
    scores = cross_validate( model, X=x, y=y, scoring='r2')

    sorted(scores.keys())

    print("The mean training accuracy is: %.3f"% (accuracies.mean()*100))
    print("The standard daviation training accuracy is: %.3f"% (accuracies.std()*100))
    print("fit times: ", scores['fit_time'])

    pp_tr = model.predict(x_train)

    g1 = sns.JointGrid(data=x_test, x=y_test, y=y_predicted)
    
    sns.scatterplot(data=x_train,x=y_train, y=pp_tr, s=100, color='orange', ax=g1.ax_joint)
    sns.scatterplot(data=x_test,x=y_test, y=y_predicted, s=100, color='blue', ax=g1.ax_joint)
   
    sns.regplot(data=x_test,x=y_test, y=y_predicted, ax=g1.ax_joint)
    sns.regplot(data=x_train,x=y_train, y=pp_tr, ax=g1.ax_joint)

    plt.ylim(0, 8.5)
    plt.xlim(0, 8.5)

    g1.set_axis_labels("Actual CO\u2082 adsorbed (mmol/g)", "Predicted CO\u2082 adsorbed (mmol/g)", fontsize =14, fontname = 'Times New Roman')
    sns.histplot(data=x_train,x=y_train,ax=g1.ax_marg_x, color ='orange')
    sns.histplot(data=x_test,x=y_test, ax=g1.ax_marg_x, color ='blue')
    g1.ax_marg_x.legend(["Train", "Test"])

    plt.show()
    names = dataset.columns[0:len(dataset)]

    perm_importance = permutation_importance(model, x_train, y_train)

    sorted_idx = perm_importance.importances_mean.argsort()
    plt.barh(names[sorted_idx], perm_importance.importances_mean[sorted_idx])
    plt.xlabel("Permutation Importance")

    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    
    featurename='Temp (°C)'#'Pressure (bar)'
        # Specific range for Temp (°C)
    temp_values = np.arange(0, 37, 2)

    # Manually compute partial dependence
    pd_values = []
    for value in temp_values:
        X_temp = x_train.copy()
        X_temp[featurename] = value
        preds = model.predict(X_temp)
        pd_values.append(np.mean(preds))

    # Plotting
    feature_name='Temp (°C)'#'Pressure (bar)'
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300, facecolor='#FFFFFF')
    ax.plot(temp_values, pd_values, '-b', linewidth=2.5)#,color='red')

    ax = plt.gca()
    ax.set_facecolor('#FFFFFF')
    #plt.plot(feature_values, pdp_values, color='red')
    plt.xlabel(f'{feature_name}', color='black', fontsize =18)
    plt.ylabel('Partial dependence', color='black', fontsize =18)
    plt.tick_params(axis='x', labelsize=22, colors='black')
    plt.tick_params(axis='y', labelsize=22, colors='black')
    plt.grid(True, color='lightgray')
    for line in ax.get_lines():
        line.set_color('red')
    plt.show()


# In[37]:


def primary_code_latex(data,n,k,size):
    '''primar_code_latext function in additinion doing calculation same as primary_code_s function,
    returns latext table'''
    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    xx = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]
    print('cross validation using whole dataset\n')
    print('Dataset shape: ',data.shape)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)
    
    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    
    scaler_Min =scalers[n]
    if n==0:
        x_train=x_train
        x_test=x_test
        x=x
    else:
        x_train = scaler_Min.fit_transform(x_train)
        x_test = scaler_Min.fit_transform(x_test)
        x = scaler_Min.fit_transform(x)

    matplotlib.rcParams['font.sans-serif'] = 'Times New Roman'
    label_size = 20
    matplotlib.rcParams['xtick.labelsize'] = label_size 
    matplotlib.rcParams['ytick.labelsize'] = label_size 
    
  
    model =  GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1,
                                       min_samples_split = 2, n_estimators = 300, 
                                       subsample = 0.5, random_state=42)
    model.fit(x_train, y_train)

    
    print("The training R2 is: %.2f" % (model.score(x_train, y_train)*100))
    print("The test R2 is: %.2f "% (model.score(x_test, y_test)*100))

    
    acc_trai=model.score(x_train, y_train)*100
    acc_tes=model.score(x_test, y_test)*100
    
    
    y_predicted = model.predict(x_test)

    print("MSE: %.4f"% mean_squared_error(y_test, y_predicted))
    print("RMSE: %.4f"% sqrt(mean_squared_error(y_test, y_predicted)))
    mer=mean_squared_error(y_test, y_predicted)

    
    
    accuracies = cross_val_score(estimator = model, X = x, y=y, cv=k)
    accuracy=accuracies.mean()*100
    
    scores = cross_validate( model, X=x, y=y, scoring='r2')
    
    print(sorted(scores.keys()))
    results4 = {'r2':[], 'coef':[]}
    print(results4['coef'])
    print(results4)
    print("The mean training accuracy is: %.3f"% (accuracies.mean()*100))
    print("The standard daviation training accuracy is: %.3f"% (accuracies.std()*100))
    print("fit times: ", scores['fit_time'])


    
    pp_tr = model.predict(x_train)
    plt.figure(figsize=(8,6),dpi=200)
    ###########################
    feature_importance = model.feature_importances_
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    fig = plt.figure(figsize=(8, 8))
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, np.array(xx.columns)[sorted_idx], fontsize =18)
    plt.title('Feature Importance (MDI)')
    result = permutation_importance(model, x_test, y_test, n_repeats=10,
                                    random_state=42, n_jobs=2)
    sorted_idx = result.importances_mean.argsort()
    fig.tight_layout()
    plt.show()
    ###############################

    gg = sns.JointGrid(data=x_test,x=y_test, y=y_predicted)
    sns.scatterplot(data=x_train,x=y_train, y=pp_tr, s=100, color='red', ax=gg.ax_joint)
    sns.regplot(data=x_train,x=y_train, y=pp_tr, color='green', ax=gg.ax_joint)

    
    sns.scatterplot(data=x_test,x=y_test, y=y_predicted, s=100, color='blue', ax=gg.ax_joint)
    sns.regplot(data=x_test,x=y_test, y=y_predicted, color='purple',ax=gg.ax_joint)
    #sns.lineplot(x=y_test, y=y_predicted, ax=g.ax_joint)
    plt.ylim(0, 7.5)
    plt.xlim(0, 7.5)

    gg.set_axis_labels("Actual CO2 uptake (mmol/g)",
                      "Predicted CO2 uptake (mmol/g)", fontsize =22, fontname = 'Times New Roman')
    sns.histplot(data=x_train,x=y_train,ax=gg.ax_marg_x, color ='red')
    sns.histplot(data=x_test,x=y_test, ax=gg.ax_marg_x, color ='blue')
    gg.ax_marg_x.legend(["Train", "Test"])
    plt.locator_params(tight=None, nbins=4)

    plt.show()
    
    
    table_1 = Texttable()
    table_1.set_cols_align(["l", "c", "c", "c", "c", "c", "c", "c"])
    table_1.set_cols_valign(["m", "m", "m", "m", "m", "m", "m", "m"])
    table_1.add_rows([["performance \ dataset","cv_1",'cv_2','cv_3','cv_4','cv_4','cv_mean','STD'],
        ['Accuracy','%.2f'%(accuracies[0]*100),'%.2f'%(accuracies[1]*100),
                       '%.2f'%(accuracies[2]*100),'%.2f'%(accuracies[3]*100),'%.2f'%(accuracies[4]*100),
                       '%.2f'%(accuracies.mean()*100),'%.2f'%(accuracies.std()*100)]])
    print('-- Example 1: Basic --')
    print('Texttable Output:')
    print(table_1.draw())
    print('\nLatextable Output:')
    print(latextable.draw_latex(table_1, caption="An example table.", label="table:example_table"))
    print('\n')
    
    
    return accuracies,accuracy,mer,acc_trai,acc_tes


# ## Deep learning functions


# In[38]:


os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


np.random.seed(42)
tf.random.set_seed(42)
random.seed(42)

def deep_conv2(dataset, test_size, lr, batch_size):
    '''The deep_conv2 function performs deep learning regression using Convolutional Neural Networks (CNNs)
    on structured data. This function applies Conv1D layers to a structured dataset for regression. 
    It scales the data using StandardScaler, reshapes it for CNN compatibility, and then splits it into 
    training and test sets. The function constructs a neural network with Conv1D and Dense layers, compiles it
    , and trains it on the training data. It evaluates the model's performance on both the test and 
    training sets, calculates metrics like Mean Squared Error (MSE) and R-squared, and visualizes loss 
    and predicted vs. original values. The function returns the R-squared score on the test set, 
    R-squared score on the training set, and the standard deviation of predictions on the test set.'''
    
    
    # Split dataset into features and target variable
    X = dataset.drop("CO2 uptake (mmol/g)", axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Reshape the features into a 3D tensor for Conv1D layer
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)
    y_scaler = StandardScaler()
    y_scaled = y_scaler.fit_transform(y.values.reshape(-1, 1)).flatten()
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_scaled, test_size=test_size, random_state=42)
    
    model = Sequential()
    model.add(Conv1D(X_reshaped.shape[1], 1, activation="relu", input_shape=(X_reshaped.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(X_reshaped.shape[1], activation="relu"))
    model.add(Dense(1))
    optimizer = Adam(learning_rate=lr)
    model.compile(loss="mse", optimizer=optimizer)
    # Fit the model to the training data
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=120, verbose=0, validation_split=test_size)

    #history = model.fit(xtrain, ytrain, batch_size=batch, epochs=120, verbose=0, validation_split=size)
    xtest=X_test
    ytest=y_test
    xtrain=X_train
    ytrain=y_train
    ypred = model.predict(xtest)
    print("MSE_test: %.4f" % mean_squared_error(ytest, ypred))
    score = r2_score(ytest, ypred)
    print("r2_test: %.4f" % score)

    ypredtr = model.predict(xtrain)
    print("MSE_train: %.4f" % mean_squared_error(ytrain, ypredtr))
    scoretr = r2_score(ytrain, ypredtr)
    print("r2_train: %.4f" % scoretr)

    
    ytest =np.array(ytest)
    ypred = np.array(ypred)
    std = np.std(ytest - ypred)
    print("Standard deviation of predictions on test set: %.4f" % std)

    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'val_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()
    
    plt.figure(figsize=(8,6),dpi=100);

    x_ax = range(len(ypred))
    plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
    plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()

    return score, scoretr, std


## results of applying functions on the datasets


# In[39]:


# results achived by the Yaun and his collegues 
primary_code(BWDPS,0,.2,1)


# In[40]:


primary_code_s(BWDPS,0,.2,1)


# In[41]:


primary_code2(BWDPS,0,.2,1)


# In[42]:


primary_code_latex(BWDPS, 0, 5, 0.2)


# In[43]:


# ## results of applying deep learning on intial cleaned data sets


# In[44]:


#deep_conv2(BWDPS, 0.15, 0.001, 16)


# In[45]:


#deep_conv2(shuffle(BWDPS), 0.15, 0.001, 16)


# In[46]:


# # Cleaning and preparation of the datasets


# In[47]:


#uncomment next line if you want to use imputed data set with Newton's second corder polynomial
#BWDPS=BWDPS_poly.copy()


# ## Checking and removing duplicated data


# In[48]:


dfk=BWDPS.copy()
dfk['Temp (°C)']=dfk['Temp (°C)']+273.15


# In[49]:


def duplicat_row(dataset):
    '''This function checks for duplicate rows in a dataset and returns those duplicate rows. 
    It helps identify and analyze instances of data duplication within the dataset.'''
    print(dataset.shape)
    duplicate= dataset[dataset.duplicated()]
    return duplicate

duplicate=duplicat_row(BWDPS)
duplicate
#df[(df['Surface Area (m2/g)']==1636.0000) & (df['CO2 uptake (mmol/g)']==2.8600) ]
#df = df.drop_duplicates()


# In[50]:


df0=BWDPS.copy()


# In[51]:


df0.drop(208,axis=0,inplace=True)
df0.reset_index(drop=True, inplace=True)
df0


# In[52]:




dfs=BWDPSs
dfs.drop(208,axis=0,inplace=True)
dfs.reset_index(drop=True, inplace=True)
dfs
dfs_first=BWDPSs[:193]
dfs_second=BWDPSs[193:]


# ## Checking for missing values


# In[53]:


msno.bar(df0, figsize=(12, 6), fontsize=12, color='steelblue')


# In[54]:


def missing_values(dataset):
    '''This function detects and returns the names of columns in the dataset that have missing values. 
    It helps pinpoint which attributes are incomplete within the dataset.'''
    missing = dataset.columns[dataset.isnull().any()].tolist()
    return missing


# In[55]:


print()
print('missing values based on attibutes are in columns:\n')
dfs_second[missing_values(dfs_second)].isnull().sum()
print()


# ## Checking for zero values


# In[56]:


def zeros_check(data):
    '''This function iterates through the columns of the dataset, counting and printing the number of zeros
    present in each column. It assists in identifying columns with a significant number of zero values within
    the dataset.'''
    for column_name in data.columns:
        column = data[column_name]
        count = (column == 0).sum()
        print('Count of zeros in column ', column_name, ' is : ', count)
        
zeros_check(BWDPS)
    


# In[57]:


table_1 = Texttable()
table_1.set_cols_align(["l", "c"])
table_1.set_cols_valign(["m", "c"])
table_1.add_rows([["Columns","Number zeros"],
                  ['S (%)',316],
                  ['Temp (°C)',72],
                  ['H (%)',91],
                  ['N (%)',1],
                  ['O (%)',4]])
print('-- Example 1: Basic --')
print('Texttable Output:')
print(table_1.draw())
print('\nLatextable Output:')
print(latextable.draw_latex(table_1, caption="An example table.", label="table:example_table"))


# ## Replacing zero values


# In[58]:


# we have two primary df0 and df datasets
#df0 will be the dataset which temperature zeros are left unchanged and df will be dataset which it's zero going 
#to fill out by different methods
#other features zeros will be replaced in both datasets
df=df0.copy()
dfs0=dfs.copy()
df


# In[59]:


dfs['Total Pore Volume(cm3/g)']=BWDPS['Total Pore Volume(cm3/g)']
dfs['Micropore Volume (cm3/g)']=BWDPS['Micropore Volume (cm3/g)']

df0['H (%)']=df0['H (%)'].replace(0,np.NaN)#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
df0['H (%)']=df0['H (%)'].interpolate(method ='pad', limit_direction ='forward')

df0['N (%)']=df0['N (%)'].replace(0,np.NaN)#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
df0['N (%)']=df0['N (%)'].interpolate(method ='pad', limit_direction ='forward')

df0['O (%)']=df0['O (%)'].replace(0,np.NaN)#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
df0['O (%)']=df0['O (%)'].interpolate(method ='pad', limit_direction ='forward')


# In[60]:


df['H (%)']=df['H (%)'].replace(0,np.NaN)#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
df['H (%)']=df['H (%)'].interpolate(method ='pad', limit_direction ='forward')

df['N (%)']=df['N (%)'].replace(0,np.NaN)#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
df['N (%)']=df['N (%)'].interpolate(method ='pad', limit_direction ='forward')

df['O (%)']=df['O (%)'].replace(0,np.NaN)#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
df['O (%)']=df['O (%)'].interpolate(method ='pad', limit_direction ='forward')

df['Temp (°C)']=df['Temp (°C)'].replace(0,df['Temp (°C)'].mean())#df['H (%)'].mean())
#df['H (%)']=df['H (%)'].fillna(method ='pad')#df.fillna(method ='bfill')
dfs['Temp (°C)']=dfs['Temp (°C)'].replace(0,dfs['Temp (°C)'].mean())
dfs['S (%)']=dfs['S (%)'].replace(0,BWDPSs['S (%)'].mean())


# In[61]:


#effect of replacing temperature zeros
plt.figure(dpi=200)
plt.style.use('fivethirtyeight')
dfs.plot(subplots=True,
        layout=(6, 2),
        figsize=(22,22),
        fontsize=10, 
        linewidth=2,
        sharex=False)#,
        #title='Visualization of the original Time Series')
plt.show()


# ## copies of primary datasets


# In[62]:


mdf=df.copy()
mdf0=df0.copy()

mdfs=dfs.copy()
mdfs0=dfs0.copy()
    
mdf0_first=mdf0[:193]
mdf0_second=mdf0[193:]

mdf_first=mdf[:193]
mdf_second=mdf[193:]

mdfs0_first=dfs0[:193]
mdfs0_second=dfs0[193:]

mdfs_first=dfs[:193]
mdfs_second=dfs[193:]

mdf0_first_shuffled = shuffle(mdf0_first)
mdf_first_shuffled = shuffle(mdf_first)
mdfs0_first_shuffled = shuffle(mdfs0_first)
mdfs_first_shuffled = shuffle(mdfs_first)


mdf0_second_shuffled = shuffle(mdf0_second)
mdf_second_shuffled = shuffle(mdf_second)
mdfs0_second_shuffled = shuffle(mdfs0_second)
mdfs_second_shuffled = shuffle(mdfs_second)


mdf0_shuffled = shuffle(mdf0)
mdfs0_shuffled = shuffle(mdfs0)
mdf_shuffled = shuffle(mdf)
mdfs_shuffled = shuffle(mdfs)

ds=df.copy()
ds0=df0.copy()


# ## Checking the correlation between features


# In[63]:


corr_matrix=df.corr()
corr_matrix.sort_values(ascending=False,by='CO2 uptake (mmol/g)')


# In[64]:


#InteractiveShell.ast_node_interactivity = "all"
InteractiveShell.ast_node_interactivity = "last_expr"


# In[65]:


plt.figure(figsize=(8,6),dpi=100);
featuers=['Total Pore Volume(cm3/g)','Micropore Volume (cm3/g)','CO2 uptake (mmol/g)']#for nonlinear relations
scatter_matrix(df[featuers],figsize=(12,8),cmap='blue');
#plt.show();


# In[66]:


plt.figure(figsize=(8,6),dpi=100);
featuers=['Total Pore Volume(cm3/g)','Micropore Volume (cm3/g)','CO2 uptake (mmol/g)']#for nonlinear relations
scatter_matrix(df0[featuers],figsize=(12,8),cmap='blue');


# In[67]:


df['Temp (°C)'].unique()
df['Temp (°C)'].value_counts()


# In[69]:


def calculate_pvalues(dataset):
    '''This function generates a DataFrame to hold p-values and iterates through pairs of columns. 
    For each pair, it calculates the p-value of the Pearson correlation coefficient, considering only rows
    with non-null values for both columns. The resulting p-values matrix is returned. This function helps
    assess the significance of correlations between various attributes in the dataset.'''
    dfcols = pd.DataFrame(columns=dataset.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in dataset.columns:
        for c in dataset.columns:
            tmp = dataset[dataset[r].notnull() & dataset[c].notnull()]
            pvalues[r][c] = round(pearsonr(tmp[r], tmp[c])[1], 4)
    return pvalues


# In[70]:


calculate_pvalues(BWDPS) 


# In[71]:


def corr_heat(dataset):
    '''This function creates a heatmap using seaborn's heatmap function to display the rounded correlation
    coefficients between columns in the dataset. The color map used is 'PRGn', and 
    correlation values are annotated on the heatmap. The function adjusts the font size and 
    rotation of axis labels for better readability. The heatmap provides insights into the 
    strength and direction of relationships between attributes within the dataset.'''
    plt.figure(figsize=(12,10),dpi=200);
    sns.heatmap(np.round(dataset.corr(),3),cmap='PRGn', annot=True);
    plt.xticks(rotation = 30, horizontalalignment='right', fontsize= 18, fontname = "Times New Roman");
    plt.yticks(rotation = 0, fontsize= 18, fontname = "Times New Roman");
    plt.show();
    
    


# In[72]:


corr_heat(df_first)


# In[73]:


corr_heat(df_second)


# In[74]:


def P_OLS_all(dataset):
    '''This function prepares the dataset by separating features (X) from the target (y). 
    It then adds a constant column to the features and conducts OLS regression using the statsmodels library.
    The regression results, including statistical summary information, are printed. The function helps analyze
    the relationships between independent variables and the target variable in the dataset.'''
    X = dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y = dataset['CO2 uptake (mmol/g)']
    X2 = sm.add_constant(X)
    est = sm.OLS(y, X2)
    est2 = est.fit()
    print(est2.summary())


# In[75]:


P_OLS_all(BWDPS)


# In[76]:


def p_value_data0(dataset): 
    '''This function performs linear regression analysis on the dataset to assess the significance
    of coefficients. It fits a linear regression model, calculates parameters, and then computes 
    standard deviations, t-values, and associated p-values for each coefficient. The resulting DataFrame
    presents these statistical values for analysis. The function aids in determining the statistical
    significance of different attributes in relation to the target variable.'''
    X = dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y = dataset['CO2 uptake (mmol/g)']
    lm = LinearRegression()
    lm.fit(X,y)
    params = np.append(lm.intercept_,lm.coef_)
    
    predictions = lm.predict(X)

    # newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
    # MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

    # Note if you don't want to use a DataFrame replace the two lines above with
    newX = np.append(np.ones((len(X),1)), X, axis=1)
    MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

    var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = params/ sd_b

    p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX[0])))) for i in ts_b]

    sd_b = np.round(sd_b,4)
    ts_b = np.round(ts_b,4)
    p_values = np.round(p_values,6)
    params = np.round(params,4)

    DF = pd.DataFrame(index=X.columns)
    DF["Coeff."],DF["std"],DF[" t_values"],DF[" P_values"] = [params[1:],sd_b[1:],ts_b[1:],p_values[1:]]

    #myDF3["features"],myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilities"] = [BWDPS.columns,params,sd_b,ts_b,p_values]
    return DF


# In[77]:


DF=p_value_data0(BWDPS)
DF


# In[78]:


def p_value_data(dataset):
    '''This function performs linear regression analysis on the dataset to determine the significance of 
    coefficients. It fits a linear regression model, computes coefficients, and calculates standard deviations,
    t-values, and corresponding p-values. The function returns a DataFrame containing these statistical values,
    helping to assess the statistical relevance of different attributes in relation to the target variable.'''
    
    X = dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y = dataset['CO2 uptake (mmol/g)']
    lm = LinearRegression()
    lm.fit(X,y)
    params = np.append(lm.intercept_,lm.coef_)
    predictions = lm.predict(X)

    # newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
    # MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

    # Note if you don't want to use a DataFrame replace the two lines above with
    newX = np.append(np.ones((len(X),1)), X, axis=1)
    MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

    var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
    sd_b = np.sqrt(var_b)
    ts_b = params/ sd_b

    p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX[0])))) for i in ts_b]

    sd_b = np.round(sd_b,3)
    ts_b = np.round(ts_b,3)
    p_values = np.round(p_values,4)
    params = np.round(params,4)

    DF = pd.DataFrame()
    #DF[" Coeff."],DF[" Stan.Err."],DF[" t-values"],DF[" P_values"] = [params,sd_b,ts_b,p_values]
    t1=dataset.columns
    t0=pd.Index(['constant'])
    t0=t0.append([t1])[:dataset.shape[1]]

    DF["Coeff"],DF["StanEr"],DF["t-values"],DF["Prob"] = [params,sd_b,ts_b,p_values]
    print(DF)
    return DF


# In[79]:


p_value_data(df_first)
# ## Partial dependence of features respect to co2 adsorption


# In[80]:


def PDP_co2(dataset,i):
    '''Given a dataset, the function performs regression using a Gradient Boosting Regressor and then generates
    a PDP for a specific feature (i). The PDP illustrates the average effect of the chosen feature on 
    the predicted CO2 uptake. The plot is created using the plot_partial_dependence function from the 
    scikit-learn library. This visualization provides insights into the relationship between the selected 
    feature and the target variable.'''

    x = dataset.drop('CO2 uptake (mmol/g)',axis=1)
    y = dataset['CO2 uptake (mmol/g)']
    
    
    feature=x.columns
    x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2, random_state = 42)
    model =  GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1,
                                           min_samples_split = 2, n_estimators = 300, 
                                           subsample = 0.5, random_state=42)
    model.fit(x,y)
    
    
       
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')

    fig, ax = plt.subplots(figsize =(8, 6),dpi=300)


    plot_partial_dependence(model, x,[feature[i]],feature_names = feature,kind='average' ,target = 0,
                            n_jobs = 3, grid_resolution = 50, ax=ax,
                            line_kw=None,ice_lines_kw=None,contour_kw=None,pd_line_kw={'color':'skyblue'})
    
    ax.grid(False)

    
    
    
#     plt.tick_params(axis = 'x', labelsize = 22)
#     plt.tick_params(axis = 'y', labelsize = 22)
#     ax.set_xlabel('Temperature', fontsize='large')
#     ax.set_ylabel('PI', fontsize='large')
    plt.show()


# In[81]:


def PDP_shap_co2(dataset,i,j):
    '''the function uses a Gradient Boosting Regressor to train a model and then creates a SHAP PDP for a 
    specific feature (i). The SHAP library is utilized to generate this plot, allowing for a detailed 
    visualization of the average effect of the selected feature on the predicted CO2 uptake. The j parameter 
    determines the curve color in the plot. The SHAP PDP helps in understanding the impact of individual 
    features on the target variable.'''
    if j==0:
        curve_color='red'
    else:
        curve_color='skyblue'
    x = BWDPS.drop('CO2 uptake (mmol/g)',axis=1)
    y = BWDPS['CO2 uptake (mmol/g)']
    feature=x.columns
    X100 = x.sample(n=200)
    feature=x.columns
    x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2, random_state = 42)
    model =  GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1,
                                           min_samples_split = 2, n_estimators = 300, 
                                           subsample = 0.5, random_state=42)
    model.fit(x,y)
    shap.plots.partial_dependence(
        feature[i], model.predict, X100, ice=False,
        model_expected_value=True, feature_expected_value=True)


# In[82]:


PDP_shap_co2(BWDPS,2,1)


# In[83]:


BWDPS_shuffled=shuffle(BWDPS)
PDP_shap_co2(BWDPS_shuffled,2,1)


# ## Adding new possible featuers


# In[84]:


df['Surfacem2/TotalPor(cm3)']=df['Surface Area (m2/g)']/df['Total Pore Volume(cm3/g)']
df['Surfacem2/Micropore(cm3)']=df['Surface Area (m2/g)']/df['Micropore Volume (cm3/g)']
df['Surface2/C']=df['Surface Area (m2/g)']/df['C (%)']
df['Surface2/H (%)']=df['Surface Area (m2/g)']/df['H (%)']
df['Surface2/N (%)']=df['Surface Area (m2/g)']/df['N (%)']
df['Surface2/O']=df['Surface Area (m2/g)']/df['O (%)']
df['Surface2/Temp']=df['Surface Area (m2/g)']/df['Temp (°C)']
df['Surface2/Pressure']=df['Surface Area (m2/g)']/df['Pressure (bar)']
#############
df['Total(cm3)/Micropore(cm3)']=df['Total Pore Volume(cm3/g)']/df['Micropore Volume (cm3/g)']
df['Total(cm3)/C']=df['Total Pore Volume(cm3/g)']/df['C (%)']
df['(Total(cm3)/g)/H (%)']=df['Total Pore Volume(cm3/g)']/df['H (%)']
df['Total(cm3)/N (%)']=df['Total Pore Volume(cm3/g)']/df['N (%)']
df['Total(cm3)/O']=df['Total Pore Volume(cm3/g)']/df['O (%)']
df['Total(cm3)/Temp']=df['Total Pore Volume(cm3/g)']/df['Temp (°C)']
df['Total(cm3)/Pressure']=df['Total Pore Volume(cm3/g)']/df['Pressure (bar)']
###########

df['Micropore(cm3/g)/C']=df['Micropore Volume (cm3/g)']/df['C (%)']
df['Micropore(cm3/g)/H (%)']=df['Micropore Volume (cm3/g)']/df['H (%)']
df['Micropore(cm3/g)/N (%)']=df['Micropore Volume (cm3/g)']/df['N (%)']
df['Micropore(cm3/g)/O']=df['Micropore Volume (cm3/g)']/df['O (%)']
df['Micropore(cm3/g)/Temp']=df['Micropore Volume (cm3/g)']/df['Temp (°C)']
df['Micropore(cm3/g)/Pressure']=df['Micropore Volume (cm3/g)']/df['Pressure (bar)']
###########

df['C/H (%)']=df['C (%)']/df['H (%)']
df['C/N (%)']=df['C (%)']/df['N (%)']
df['C/O']=df['C (%)']/df['O (%)']
df['C/Temp']=df['C (%)']/df['Temp (°C)']
df['C/Pressure']=df['C (%)']/df['Pressure (bar)']
############
df['H/N (%)']=df['H (%)']/df['N (%)']
df['H/O']=df['H (%)']/df['O (%)']
df['H/Temp']=df['H (%)']/df['Temp (°C)']
df['H/Pressure']=df['H (%)']/df['Pressure (bar)']
############
df['N/O']=df['N (%)']/df['O (%)']
df['N/Temp']=df['N (%)']/df['Temp (°C)']
df['N/Pressure']=df['N (%)']/df['Pressure (bar)']
################
df['O/Temp']=df['O (%)']/df['Temp (°C)']
df['O/Pressure']=df['O (%)']/df['Pressure (bar)']
###################
df['Temp/Pressure']=df['Temp (°C)']/df['Pressure (bar)']
print()
print('new shape of data set is: ', df.shape)
df.head(5)


# In[85]:


zeros_check(df0)


# In[86]:


df0['Surfacem2/TotalPor(cm3)']=df0['Surface Area (m2/g)']/df0['Total Pore Volume(cm3/g)']
df0['Surfacem2/Micropore(cm3)']=df0['Surface Area (m2/g)']/df0['Micropore Volume (cm3/g)']
df0['Surface2/C']=df0['Surface Area (m2/g)']/df0['C (%)']
df0['Surface2/H (%)']=df0['Surface Area (m2/g)']/df0['H (%)']
df0['Surface2/N (%)']=df0['Surface Area (m2/g)']/df0['N (%)']
df0['Surface2/O']=df0['Surface Area (m2/g)']/df0['O (%)']
#df0['Surface2/Temp)']=df0['Surface Area (m2/g)']/df0['Temp (°C)']
df0['Surface2/Pressure']=df0['Surface Area (m2/g)']/df0['Pressure (bar)']
#############
df0['Total(cm3)/Micropore(cm3)']=df0['Total Pore Volume(cm3/g)']/df0['Micropore Volume (cm3/g)']
df0['Total(cm3)/C']=df0['Total Pore Volume(cm3/g)']/df0['C (%)']
df0['(Total(cm3)/g)/H (%)']=df0['Total Pore Volume(cm3/g)']/df0['H (%)']
df0['Total(cm3)/N (%)']=df0['Total Pore Volume(cm3/g)']/df0['N (%)']
df0['Total(cm3)/O']=df0['Total Pore Volume(cm3/g)']/df0['O (%)']
#df0['Total(cm3)/Temp)']=df0['Total Pore Volume(cm3/g)']/df0['Temp (°C)']
df0['Total(cm3)/Pressure']=df0['Total Pore Volume(cm3/g)']/df0['Pressure (bar)']
###########

df0['Micropore(cm3/g)/C']=df0['Micropore Volume (cm3/g)']/df0['C (%)']
df0['Micropore(cm3/g)/H (%)']=df0['Micropore Volume (cm3/g)']/df0['H (%)']
df0['Micropore(cm3/g)/N (%)']=df0['Micropore Volume (cm3/g)']/df0['N (%)']
df0['Micropore(cm3/g)/O']=df0['Micropore Volume (cm3/g)']/df0['O (%)']
#df0['Micropore(cm3/g)/Temp)']=df0['Micropore Volume (cm3/g)']/df0['Temp (°C)']
df0['Micropore(cm3/g)/Pressure']=df0['Micropore Volume (cm3/g)']/df0['Pressure (bar)']
###########

df0['C/H (%)']=df0['C (%)']/df0['H (%)']
df0['C/N (%)']=df0['C (%)']/df0['N (%)']
df0['C/O']=df0['C (%)']/df0['O (%)']
#df0['C/Temp)']=df0['C (%)']/df0['Temp (°C)']
df0['C/Pressure']=df0['C (%)']/df0['Pressure (bar)']
############
df0['H/N (%)']=df0['H (%)']/df0['N (%)']
df0['H/O']=df0['H (%)']/df0['O (%)']
#df0['H/Temp)']=df0['H (%)']/df0['Temp (°C)']
df0['H/Pressure']=df0['H (%)']/df0['Pressure (bar)']
############
df0['N/O']=df0['N (%)']/df0['O (%)']
#df0['N/Temp)']=df0['N (%)']/df0['Temp (°C)']
df0['N/Pressure']=df0['N (%)']/df0['Pressure (bar)']
################
#df0['O/Temp)']=df0['O (%)']/df0['Temp (°C)']
df0['O/Pressure']=df0['O (%)']/df0['Pressure (bar)']
###################
#df0['Temp/Pressure']=df0['Temp (°C)']/df0['Pressure (bar)']
print()
print('new shape of data set is: ', df0.shape)
df0.head(5)


# ## Correlation between target and all othert features


# In[87]:


def correlation_matrix(dataset):
    '''This function calculates the correlation matrix of the dataset's attributes. It then sorts the correlation
    coefficients with respect to the target variable ("CO2 uptake (mmol/g)") in descending order. 
    The top 10 correlated attributes are printed, along with a LaTeX representation of the correlation 
    coefficients. This function is useful for understanding the relationships between different attributes 
    and the target variable in the dataset.'''
    corr_matrix=dataset.corr()
    aa=corr_matrix['CO2 uptake (mmol/g)'].sort_values(ascending=False)
    print(aa[:10])
    print(aa.to_latex(index=True))


# In[88]:


correlation_matrix(df)


# In[89]:


BWDPS_38=df0.copy()
BWDPS_46=df.copy()
print(BWDPS_38.shape)
print(BWDPS_46.shape)


# ## Removing high and low correlated features to target and feature selection


# In[90]:


def remove_high_corr_features(dataset):
    '''This function computes the correlation matrix and identifies features that have both high positive and
    low positive correlations with other features. It then removes these features to mitigate multicollinearity. 
    The function outputs the new dataset shape and the remaining features. It's a valuable step in preprocessing
    data to enhance model performance and interpretability.'''
    corr_matrix = dataset.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    to_drop = [column for column in upper.columns if (any(upper[column] > 0.95)& any(upper[column] < 0.05) )]
    dataset.drop(to_drop, axis=1, inplace=True)
    print()
    print('new shape after removing some features based on correlation: ', dataset.shape)
    print()
    print('dataset fetures after removing high correlated ones:\n',dataset.columns)


# In[91]:




remove_high_corr_features(df)


# ## important feature  selection for zero values filled up temperature feature


# In[92]:


def importance_features(dataset):
    '''This function fits a Gradient Boosting Regressor to the dataset and then computes and plots feature 
    importances using permutation importance and the feature_importances_ attribute of the regressor. 
    The top 30 features by permutation importance and by the regressor's feature importances are plotted. 
    The function returns lists of feature names based on permutation importance and the regressor's 
    feature importances. This aids in identifying attributes that have the most influence
    on the target variable.'''
    
   
    gbr21=GradientBoostingRegressor(n_estimators=80)

    df_train=dataset.drop('CO2 uptake (mmol/g)',axis=1)
    df_label=dataset['CO2 uptake (mmol/g)']

    gbr=gbr21.fit(df_train, df_label)


    names = df_train.columns

    perm_importance = permutation_importance(gbr, df_train, df_label)
    per_sorted_idx = perm_importance.importances_mean.argsort()
        
    
    plt.figure(figsize=(8,6),dpi=200)
    plt.bar(names[per_sorted_idx[-30:]], perm_importance.importances_mean[per_sorted_idx[-30:]])
    plt.xticks(rotation = 60, horizontalalignment='right', fontsize= 12, fontname = "Times New Roman")
    plt.ylabel("Permutation Importance")
    plt.figure(num=None, figsize=(10,8), dpi=200, facecolor='w', edgecolor='k')
    
    
    features_BWDPS_46=names[per_sorted_idx][-30:]
    

    imp_sort_index = pd.Series(gbr.feature_importances_, index= df_train.columns)


    gbr.feature_importances_.round(2)

    imp_sorted_index=names[imp_sort_index.argsort()]
    imp_sort_index.nlargest(30).plot(kind='bar')
    
    return features_BWDPS_46,imp_sorted_index
     


# In[93]:


features_BWDPS_46,imp_sorted_index=importance_features(BWDPS_46)


# In[94]:


importance_features(BWDPS_38)
# ## mutual information


# In[95]:


# Utility functions from Tutorial
def make_mi_scores(x, y):
    '''This function computes Mutual Information (MI) scores between features in the input DataFrame x and 
    the target variable y. It converts categorical features to integer encodings and calculates MI scores
    using mutual_info_regression from scikit-learn. The function returns a Pandas Series containing MI 
    scores sorted in descending order.'''
    
    x = x.copy()
    for colname in x.select_dtypes(["object", "category"]):
        x[colname], _ = x[colname].factorize()
    # All discrete features should now have integer dtypes
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in x.dtypes]
    mi_scores = mutual_info_regression(x, y, discrete_features=discrete_features, random_state=0)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=x.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores


def plot_mi_scores(scores):
    '''This function plots the MI scores calculated by the make_mi_scores function. However, there is an 
    issue with the provided code. To fix it, the line plt.bar(scores) should be replaced with
    scores.plot(kind='bar'). This will create a bar plot showing the MI scores for each feature.'''
    scores = scores.sort_values(ascending=True)
#     width = np.arange(len(scores))
#     ticks = list(scores.index)
    plt.bar(scores)
    #plt.yticks(width, ticks)
    plt.title("Mutual Information Scores")


# In[96]:


# Set Matplotlib defaults
plt.style.use("seaborn-whitegrid")
plt.rc("figure", autolayout=True)
plt.rc(
    "axes",
    labelweight="bold",
    labelsize="large",
    titleweight="bold",
    titlesize=14,
    titlepad=10,
)

features1 = ["Pressure (bar)", "O (%)", "Micropore Volume (cm3/g)"]
features2 = ['Total Pore Volume(cm3/g)','Surface Area (m2/g)','C (%)']
sns.relplot( x="value", y="CO2 uptake (mmol/g)", col="variable",
            data=BWDPS_46.melt(id_vars="CO2 uptake (mmol/g)", value_vars=features1), facet_kws=dict(sharex=False),);
sns.relplot( x="value", y="CO2 uptake (mmol/g)", col="variable",
            data=BWDPS_46.melt(id_vars="CO2 uptake (mmol/g)", value_vars=features2), facet_kws=dict(sharex=False),);


# In[97]:


x = BWDPS_46.copy()
y = x.pop('CO2 uptake (mmol/g)')

mi_scores = make_mi_scores(x, y)
mi_scores[:10]


# In[98]:


#plt.plot(mi_scores[:10])
ser = pd.DataFrame(mi_scores)

mu_features=ser.index
mu_features
dsm=BWDPS_46[mu_features[:30]]
dsm['CO2 uptake (mmol/g)']=BWDPS_46['CO2 uptake (mmol/g)']
x_mu=dsm
x_mu


# In[99]:


#plt.figure(figsize=(20,16),dpi=150)
g=sns.catplot(x="Pressure (bar)", y="CO2 uptake (mmol/g)", data=BWDPS_46, kind="boxen");
g.fig.set_size_inches(8,6)


# In[100]:


#plt.figure(figsize=(20,16),dpi=150)
g=sns.catplot(x="Temp (°C)", y="CO2 uptake (mmol/g)", data=BWDPS_46, kind="strip");
g.fig.set_size_inches(8,6)


# In[101]:


#plt.figure(figsize=(20,16),dpi=150)
g=sns.catplot(x="C (%)", y="CO2 uptake (mmol/g)", data=BWDPS_46, kind="boxen");
g.fig.set_size_inches(8,6)


# In[102]:


feature = "Pressure (bar)"

sns.lmplot(
    x=feature, y="CO2 uptake (mmol/g)", hue="Temp (°C)", col="Temp (°C)",
    data=BWDPS_46, scatter_kws={"edgecolor": 'w'}, col_wrap=3, height=4,
);


# In[103]:


feature = "Temp (°C)"

sns.lmplot(
    x=feature, y="CO2 uptake (mmol/g)", hue="Pressure (bar)", col="Pressure (bar)",
    data=BWDPS_46, scatter_kws={"edgecolor": 'w'}, col_wrap=3, height=4,
);


# ## Outliers checking


# In[104]:


plt.figure(figsize=(8,6),dpi=200);

ax=plt.subplot(4,3,1);
sns.boxplot(y=ds0['Surface Area (m2/g)']);

ax=plt.subplot(4,3,2);
sns.boxplot(y=ds0['Total Pore Volume(cm3/g)']);

ax=plt.subplot(4,3,3)
sns.boxplot(y=ds0['Micropore Volume (cm3/g)']);

ax=plt.subplot(4,3,4);
sns.boxplot(y=ds0['Temp (°C)']);

ax=plt.subplot(4,3,5);
sns.boxplot(y=ds0['C (%)']);

ax=plt.subplot(4,3,6);
sns.boxplot(y=ds0['H (%)']);

ax=plt.subplot(4,3,7);
sns.boxplot(y=ds0['N (%)']);

ax=plt.subplot(4,3,8);
sns.boxplot(y=ds0['O (%)']);


ax=plt.subplot(4,3,9);
sns.boxplot(y=ds0['Pressure (bar)'])



plt.subplots_adjust(wspace=0.8);
plt.subplots_adjust(hspace=0.4);
print(ds0.shape)

plt.show();


Q11 = ds0['Surface Area (m2/g)'].quantile(0.05)
Q13 = ds0['Surface Area (m2/g)'].quantile(0.95)
IQR1 = Q13 - Q11

Q21 = ds0['Total Pore Volume(cm3/g)'].quantile(0.05)
Q23 = ds0['Total Pore Volume(cm3/g)'].quantile(0.95)
IQR2 = Q23 - Q21

Q31 = ds0['Micropore Volume (cm3/g)'].quantile(0.05)
Q33 = ds0['Micropore Volume (cm3/g)'].quantile(0.95)
IQR3 = Q33 - Q31

Q41 = ds0['Pressure (bar)'].quantile(0.05)
Q43 = ds0['Pressure (bar)'].quantile(0.95)
IQR4 = Q43 - Q41


# In[105]:


new_df = ds0[
        #(ds0['Surface Area (m2/g)'] > Q11-IQR1 ) & (ds0['Surface Area (m2/g)'] < Q13+IQR1 )&  
         (ds0['Total Pore Volume(cm3/g)'] > Q21-IQR2) & (ds0['Total Pore Volume(cm3/g)'] < Q23+IQR2)&
         (ds0['Micropore Volume (cm3/g)'] > Q31 -IQR3) & (ds0['Micropore Volume (cm3/g)'] < Q33+IQR3)&
         (ds0['Pressure (bar)'] > Q41 -IQR4) & (ds0['Pressure (bar)'] < Q43+IQR4)]#&

print('shape of dataset after removing outliers',new_df.shape)


plt.figure(figsize=(10,6),dpi=100)

ax=plt.subplot(4,3,1)
sns.boxplot(y=new_df['Surface Area (m2/g)'])

ax=plt.subplot(4,3,2)
sns.boxplot(y=new_df['Total Pore Volume(cm3/g)'])

ax=plt.subplot(4,3,3)
sns.boxplot(y=new_df['Micropore Volume (cm3/g)'])

ax=plt.subplot(4,3,4)
sns.boxplot(y=new_df['Temp (°C)'])

ax=plt.subplot(4,3,5)
sns.boxplot(y=new_df['C (%)'])

ax=plt.subplot(4,3,6)
sns.boxplot(y=new_df['H (%)'])

ax=plt.subplot(4,3,7)
sns.boxplot(y=new_df['N (%)'])

ax=plt.subplot(4,3,8)
sns.boxplot(y=new_df['O (%)'])

ax=plt.subplot(4,3,9)
sns.boxplot(y=new_df['Pressure (bar)'])


plt.subplots_adjust(wspace=0.8)
plt.subplots_adjust(hspace=0.4)
print(new_df.shape)

plt.show()


# # dataset after adding newfeature and feature selection


# In[106]:


def split_datasets(dataset,size):
    print(dataset.shape)
    x=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']

    df_train,df_test,df_label,df_test_label=train_test_split(x,y,test_size=size, random_state=42)

    print('shape of train set is:      ',df_train.shape)
    print('shape of train label set is:',df_label.shape)
    print()
    print('shape of test set is:      ',df_test.shape)
    print('shape of test label set is:',df_test_label.shape)
    return df_train,df_test,df_label,df_test_label


# In[107]:


features_BWDPS_46,imp_sorted_index=importance_features(BWDPS_46)
print(len(features_BWDPS_46))
dff=BWDPS_46[features_BWDPS_46]
print(dff.shape)
dff['CO2 uptake (mmol/g)']=BWDPS_46['CO2 uptake (mmol/g)']

x3=dff.drop(['CO2 uptake (mmol/g)'],axis=1)
y3=BWDPS_46['CO2 uptake (mmol/g)']


# In[108]:


features_BWDPS_38,imp_sorted_index0=importance_features(BWDPS_38)
imp_sorted_index0
print(len(features_BWDPS_38))
dff0=BWDPS_38[features_BWDPS_38[-30:]]
print(dff0.shape)
dff0['CO2 uptake (mmol/g)']=BWDPS_38['CO2 uptake (mmol/g)']
x4=dff0.drop(['CO2 uptake (mmol/g)'],axis=1)
y4=BWDPS_38['CO2 uptake (mmol/g)']


# ## recrussive feature selection
# 


# In[109]:


#gbr=GradientBoostingRegressor(n_estimators=80)
gbr=GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1,
                          min_samples_split = 2, n_estimators = 300, subsample = 0.5)
def rfecv_feature(dataset,n,t):
    '''The rfecv_feature function performs feature selection using Recursive Feature Elimination with 
    Cross-Validation (RFECV) and evaluates the impact of different numbers of selected features (k-best)
    on the performance of Gradient Boosting Regressor and Random Forest Regressor models. It uses different
    k-best values, cross-validation, and box plots to visualize how the models' r2-scores change with 
    varying feature counts. The goal is to find the optimal number of features for each model.'''
    
    x=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    
    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    scaler_Min = scalers[n]#MinMaxScaler()
    
    x = scaler_Min.fit_transform(x)
    # X_test2= scaler_Min.fit_transform(X_test2)
    gbr=GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1,
                          min_samples_split = 2, n_estimators = 300, subsample = 0.5)
  

    df_trains,df_tests,df_labels,df_test_labels=train_test_split(x,y,test_size=.15, random_state=42)

    print('shape of train set is:      ',df_trains.shape)
    print('shape of train label set is:',df_labels.shape)
    print()
    print('shape of test set is:      ',df_tests.shape)
    print('shape of test label set is:',df_test_labels.shape)

    regressor_names=['gbr','rf']
    rf=RandomForestRegressor(random_state =42)
    k_best1 = [9,12,15,18,22,26,30,34]
    k_best2 = [9,12,15,18,22,26,30,34,38,40,42,45]
    k_best=[k_best1,k_best2]
    
    fig, axs = plt.subplots(1, 2, figsize=(12,5))
    cv = RepeatedKFold(n_splits=5, n_repeats=10, random_state=321)

    mean_score = {}
    for i, regressor in enumerate([gbr, rf]):
      scores = []
      for k in k_best[t]:
          sel = SelectKBest(score_func=f_regression, k=k)
          _X = sel.fit_transform(x, y.values.ravel())
          score = cross_val_score(regressor, _X, y, scoring="r2", cv=cv, n_jobs=-1)
          scores.append(score)
          mean_score[regressor_names[i]+'-'+str(k)] = np.mean(score)
      scores = pd.DataFrame(scores).T
      scores.boxplot(ax=axs[i], grid=False)
      axs[i].set_title(regressor_names[i])
      axs[i].set_ylabel('r2 score')
      axs[i].set_xlabel('K-best features')
      axs[i].set_xticklabels(k_best[0])

    plt.show()
    print("The mean r2-scores are:")
    for name, score in sorted(mean_score.items(), key=lambda item: item[1]):
      print(str(name)+" features:\t", score)


# In[110]:


#rfecv_feature(BWDPS_38,4,0)


# In[111]:


def rfecv_sel(dataset,n):
    '''This function performs Recursive Feature Elimination with Cross-Validation (RFECV) to select the 
    most important features for a Gradient Boosting Regressor. It scales the features using a specified scaler
    and then fits the RFECV estimator to the data to identify the important features. The function returns 
    the transformed feature matrix with the selected features, the corresponding target variable, and a 
    DataFrame indicating which columns are kept based on RFECV. The goal is to reduce the number of 
    features while maintaining or improving model performance.'''
    
    x=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    xx=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    
    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    scaler_Min = scalers[n]  #MinMaxScaler()
    
    x = scaler_Min.fit_transform(x)
    gbr=GradientBoostingRegressor(learning_rate= 0.05, max_depth = 4, min_samples_leaf = 1,
                          min_samples_split = 2, random_state=42, n_estimators = 300, subsample = 0.5)
  
    rfecv = RFECV(estimator=gbr, step=1, scoring='neg_mean_squared_error')

    # Fit recursive feature eliminator 
    rfecv.fit(x, y)

    X_new = rfecv.transform(x)
    print("Num Features Before:", x.shape[1])
    print("Num Features After:", X_new.shape[1])
    
    #print(x.columns.shape)
    print(rfecv.support_.shape)
    features_kept = pd.DataFrame({'columns': xx.columns,'Kept': rfecv.support_})
    print(features_kept)
    
    last_columns=features_kept['columns'][features_kept['Kept']==True]
    print(last_columns)
    
    X_new_df = xx.iloc[:, rfecv.support_]
    print(X_new_df.shape)
    
    X_new_df['CO2 uptake (mmol/g)']=dataset['CO2 uptake (mmol/g)']
    
    yr=X_new_df['CO2 uptake (mmol/g)']
    xr=X_new_df.drop(['CO2 uptake (mmol/g)'],axis=1)
    print(rfecv.n_features_)
    print(rfecv.get_support(indices=True))
  
    return xr,yr,X_new_df


# In[112]:


#xrs01,yrs01,X_new_dfs01=rfecv_sel(BWDPS_38,1)


# In[113]:


#X_new_dfs01


# In[114]:


#xrs04,yrs04,X_new_dfs04=rfecv_sel(BWDPS_38,4)


# In[115]:


#xrs1,yrs1,X_new_dfs1=rfecv_sel(BWDPS_46,1)


# In[116]:


#X_new_dfs1


# In[117]:


#xrs4,yrs4,X_new_dfs4=rfecv_sel(BWDPS_46,4)


# In[118]:


#X_new_dfs4


# In[119]:


#some new datasets
BWDPS_38_shuffled = shuffle(BWDPS_38)

BWDPS_46_shuffled = shuffle(BWDPS_46)

df0_shuffled = shuffle(df0)

df_shuffled = shuffle(df)

dff_shuffled = shuffle(dff)

dff0_shuffled = shuffle(dff0)

# X_new_dfs01_shuffled = shuffle(X_new_dfs01)

# X_new_dfs04_shuffled = shuffle(X_new_dfs04)

# X_new_dfs1_shuffled = shuffle(X_new_dfs1)

# X_new_dfs4_shuffled = shuffle(X_new_dfs4)


# # Comparison of performance of different models with different scalers


# In[120]:


def com_per_models(dataset):
    '''The com_per_models function compares the performance of different models using different feature scaling
    techniques. It takes a dataset as input, where one of the columns is the target variable
    "CO2 uptake (mmol/g)". The function uses three different models: Linear Regression, Random Forest Regressor,
    and Gradient Boosting Regressor. For each model, it compares the performance using different 
    feature scaling methods: raw data, MinMaxScaler, MaxAbsScaler, RobustScaler, StandardScaler, 
    and QuantileTransformer. 
    The function performs cross-validation with repeated k-fold (5-fold, 10 repeats) and calculates 
    the r-squared scores for each combination of model and scaling technique. The results are visualized 
    using boxplots, showing the distribution of r-squared scores for each combination. The purpose of this 
    function is to help compare how different models perform under different scaling techniques, which can
    give insights into which combination works best for the given dataset and problem.'''
    
    x = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]
    
    models=[LinearRegression(),RandomForestRegressor(random_state=42),gbr]
    models_names = ['Linear', 'RF','GBR']
    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]

    scalers_names = ['Row data', 'MinMax', 'MaxAbs', 'Robust', 'SS','Quantile']

    fig, axs = plt.subplots(figsize=(8,6),dpi=150)
    results = {}
    for j in range(len(models)):
        for k in range(len(scalers)):
            if scalers[k]:
                X_scaled = scalers[k].fit_transform(x)
            else:
                X_scaled = x
            
            cv = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)
            scores = cross_val_score(models[j], X_scaled, y, scoring='r2', cv=cv, n_jobs=1)
            results[f'{models_names[j]}-{scalers_names[k]}'] = scores

    df_res0 = pd.DataFrame(results).copy()
    df_res0.boxplot(rot=45)
    axs.set_ylabel("r$^2$ score")
    plt.xticks(ha='right')
    plt.show()
    return df_res0


# In[121]:


#df_res0=com_per_models(df_first)


# In[122]:


#df_res0=com_per_models(df_second)


# In[123]:


def skew_map(data):
    '''The skew_map function calculates and prints the skewness of each column in the provided dataset. 
    Skewness is a measure of the asymmetry of the distribution of values in a dataset. Positive skewness 
    indicates that the distribution is skewed to the right (tail is longer on the right side), while negative
    skewness indicates that the distribution is skewed to the left (tail is longer on the left side).'''
    for column in data.columns:
        print(column)
        df_check = data[column].map(lambda i: np.log(i) if i > 0 else 0) 
        print(df_check.skew())
        print(df_check.skew())


# In[124]:


skew_map(df_first)

# ## Scaler effect


# In[125]:


p=sns.displot(BWDPS, kind="kde")
p.fig.set_dpi(200)


# In[126]:


BWDPS_scaled = StandardScaler().fit_transform(BWDPS)

BWDPS_scaled = pd.DataFrame(BWDPS_scaled, columns=BWDPS.columns)

p_all = sns.displot(BWDPS_scaled, kind="kde", common_norm=False)

p_all.fig.set_dpi(200)

plt.xticks(rotation=0, ha='right')

plt.show()


# # results of MGBR on datasets

# ## modified GBR on first set of collected original dataset


# In[127]:


def best_par_gbr(data,size):
    '''The best_par_gbr function searches for the optimal hyperparameters of a Gradient Boosting Regressor model
    using a grid search approach. It takes a dataset and test set size, and then iterates through various 
    hyperparameter combinations (learning rate, n_estimators, and max_depth). For each combination, it trains
    a model, evaluates its performance, and records the accuracy scores. The results are returned as a 
    dictionary and a DataFrame.'''
    
    results={}
    df_train,df_test,df_label,df_test_label=split_datasets(data,size)

    for i in [0.5,0.1, 0.01, 0.001]:
        for j in [100, 250, 500, 750]:
            for k in [2, 4, 6]:
                
            
                gbr = GradientBoostingRegressor(learning_rate= i, max_depth = k, min_samples_leaf = 1,
                                  min_samples_split = 2, n_estimators = j,
                                  subsample = 0.5, random_state=42)
                #GradientBoostingRegressor(learning_rate=i, n_estimators=j)
                gbr = gbr.fit(df_train, df_label)
                print("predict output for GradientBoostingRegressor: learning_rate={}, n_estimators={},max_depth = {}".format(i, j,k))
                mse = mean_squared_error(df_test_label, gbr.predict(df_test))
                print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
                scores=gbr.score(df_test, df_test_label)
                print("Accuracy on training set: %.3f" % gbr.score(df_train, df_label))
                print("Accuracy on test set: %.3f" % scores)
                print("==============================================")
                results[f'{i}-{j}-{k}'] = scores

    df_scores = pd.DataFrame(results, index=[0]).copy()
    return results,df_scores


# In[128]:


def best_par_gbr2(dataset,fold,size):
    
    '''The best_par_gbr2 function is used to find the best hyperparameters for a Gradient Boosting Regressor 
    model using a grid search approach, while also performing cross-validation. It takes a dataset, the number
    of folds for cross-validation, and the test set size. It then iterates through various combinations of 
    hyperparameters (learning rate, n_estimators, max_depth), trains a model with each combination, and 
    evaluates its performance using cross-validation. The results are stored in a dictionary and a DataFrame, 
    containing the mean scores from cross-validation for each hyperparameter combination.'''
    results={}
    x=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    df_train,df_test,df_label,df_test_label=train_test_split(x,y,test_size=size, random_state=42)

    for i in [0.01, 0.05, 0.1]:
        for j in [300, 500, 700,750,800]:
            for k in [3, 4, 5, 6]:
                
            
                gbr = GradientBoostingRegressor(learning_rate= i, max_depth = k, min_samples_leaf = 1,
                                  min_samples_split = 2, n_estimators = j,
                                  subsample = 0.5, random_state=42)
                #GradientBoostingRegressor(learning_rate=i, n_estimators=j)
                gbr = gbr.fit(df_train, df_label)
                
                scores = cross_val_score(gbr, x, y , cv=fold, scoring='r2')
                
                
                print("predict output for GradientBoostingRegressor: learning_rate={}, n_estimators={},max_depth = {}".format(i, j,k))
                mse = mean_squared_error(df_test_label, gbr.predict(df_test))
                print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
                #scores=gbr.score(df_test, df_test_label)
                #pred2 = gbr.predict(df_test)
                #print("Accuracy on training set: %.3f" % pred2)
                print("mean on test set: %.3f" % scores.mean())
                print("std on test set: %.3f" % scores.std())

                print("==============================================")
                results[f'{i}-{j}-{k}'] = scores.mean()


    df_scores = pd.DataFrame(results, index=[0]).copy()

    return results,df_scores


# In[129]:


#results,df_scores=best_par_gbr2(dff_shuffled,5,.15)


# In[130]:


# max(df_scores.loc[0])
# df_scores['0.1-750-6']
# maxValueIndexObj = df_scores.idxmax(axis=1)
# df_scores[maxValueIndexObj]


# ## Functions for compare


# In[131]:


dff2=dff
dff2=dff2.assign(MP= BWDPS_46['Micropore(cm3/g)/Pressure'],
                 TO=BWDPS_46['Total(cm3)/O' ] ,
                 TN= BWDPS_46['Total(cm3)/N (%)' ],
                 OT= BWDPS_46['O/Temp' ],
                 CN= BWDPS_46[ 'C/N (%)'], 
                 MH= BWDPS_46[ 'Micropore(cm3/g)/H (%)'], 
                 MO= BWDPS_46['Micropore(cm3/g)/O' ] ,
                 SH= BWDPS_46['Surface2/H (%)' ] ,
                 CH= BWDPS_46[ 'C/H (%)'] ,
                 MN= BWDPS_46[ 'Micropore(cm3/g)/N (%)'] ,
                 TPV= BWDPS_46['Total Pore Volume(cm3/g)' ])#,'22'=Total(cm3)/O])
dff2.shape

dff2_shuffled = shuffle(dff2)


dff02=dff0
dff02=dff02.assign(MP= BWDPS_38['Micropore(cm3/g)/Pressure'],
                 TO=BWDPS_38['Total(cm3)/O' ] ,
                 TN= BWDPS_38['Total(cm3)/N (%)' ],
#                  ff04= BWDPS_38['O/Temp' ],
                 CN= BWDPS_38[ 'C/N (%)'], 
                 MH= BWDPS_38[ 'Micropore(cm3/g)/H (%)'], 
                 MO= BWDPS_38['Micropore(cm3/g)/O' ] ,
                 SH= BWDPS_38['Surface2/H (%)' ] ,
                 CH= BWDPS_38[ 'C/H (%)'] ,
                 MN= BWDPS_38[ 'Micropore(cm3/g)/N (%)'] ,
                 TPV= BWDPS_38['Total Pore Volume(cm3/g)' ])#,'22'=Total(cm3)/O])
dff02.shape

dff02_shuffled = shuffle(dff02)


# In[132]:


def generate_short_names(names, length=3):
    """
    Generate short names for features.

    :param names: List of feature names
    :param length: Length of short names
    :return: List of short names
    """
    short_names = [name[:length] for name in names]
    return short_names


# In[134]:


def loss_GBR_ML(data, size):
    '''The loss_GBR_ML function trains a Gradient Boosting Regressor model on a given dataset. It then evaluates
    the model's performance using cross-validated R2 scores, plots the training and test set loss curves, and 
    visualizes feature importance using a bar plot.'''
    
    X = data.drop('CO2 uptake (mmol/g)',axis=1) # assuming 'target' is the column you want to predict
    y = data['CO2 uptake (mmol/g)']
    gbr_params = {'learning_rate': 0.1, 'max_depth': 4, 'min_samples_leaf': 1,
                  'min_samples_split': 2, 'n_estimators': 750, 'subsample': 0.5}

    df_train, df_test, df_label, df_test_label = train_test_split(X,y,test_size=.15, random_state=42)
    sc = StandardScaler()
    X_train_std = sc.fit_transform(df_train)
    X_test_std = sc.transform(df_test)

    gbr = GradientBoostingRegressor(**gbr_params)
    cv_scores = cross_val_score(gbr, X_train_std, df_label, cv=5, scoring='r2')
    mean_cv_score = np.mean(cv_scores)
    std_cv_score = np.std(cv_scores)

    print("Mean cross-validated R2 score: %.2f" %( mean_cv_score*100))
    print("Standard deviation of cross-validated R2 scores: %.3f" % (std_cv_score*100))

    gbr.fit(X_train_std, df_label)

    train_score = np.zeros((gbr_params['n_estimators'],), dtype=np.float64)
    test_score = np.zeros((gbr_params['n_estimators'],), dtype=np.float64)
    train_score = gbr.train_score_

    y_test = df_test_label
    for i, y_pred in enumerate(gbr.staged_predict(X_test_std)):
        test_score[i] = gbr.loss_(y_test, y_pred)



    # Plot Deviance (Loss)
    fig = plt.figure(figsize=(8, 6), dpi=300)
    plt.subplot(1, 1, 1)
    #plt.title('Deviance')
    plt.plot(np.arange(gbr_params['n_estimators']) + 1, train_score, 'b-', label='Train Set')
    plt.plot(np.arange(gbr_params['n_estimators']) + 1, test_score, 'r-', label='Test Set')
    plt.legend(loc='upper right')
    plt.xlabel('Boosting Iterations', fontsize=16)
    plt.ylabel('Loss', fontsize=16)
    fig.tight_layout()
    plt.show()

    # Plot Feature Importance
    bhp = pd.DataFrame(df_train, columns=df_train.columns)
    feature_importance = gbr.feature_importances_
    sorted_idx = np.argsort(feature_importance)[-10:]
    pos = np.arange(sorted_idx.shape[0]) + .5
    fig = plt.figure(figsize=(8, 6), dpi=300)
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, bhp.columns[sorted_idx], fontsize=16)
    plt.title('Feature Importance (MDI)')
    fig.tight_layout()
    plt.show()


# In[135]:


loss_GBR_ML(BWDPS,.15)


# In[136]:


loss_GBR_ML(BWDPS_shuffled,.15)


# In[137]:


loss_GBR_ML(BWDPS_46_shuffled,.15)


# In[138]:


loss_GBR_ML(BWDPS_38_shuffled,.15)


# In[139]:


dff2['Micropore Volume (cm3/g)']=BWDPS_46['Micropore Volume (cm3/g)']
dff2_shuffled = shuffle(dff2)


# In[140]:


def N_par_gbr(dataset,fold,size,n):
    ''' this function find effect of changes in Nitrogen features on co2 adsorption '''
    results0={}
    results20={}

    for i in range(1, n):#[.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.2,1.3,1.4,1.5]:
        
        

        dataset_shuffled=shuffle(dataset)
     
        #dataset_shuffled['Pressure (bar)']= dataset['Pressure (bar)']+i/10
        #dataset_shuffled.loc[:,['N (%)']]= dataset_shuffled.loc[:,['N (%)']]+round(i / 3, 1)
        dataset_shuffled.loc[:,['N (%)']]= round(i / 10, 2)

        print(dataset_shuffled['N (%)'].head(2))
        x=dataset_shuffled.drop(['CO2 uptake (mmol/g)'],axis=1)
        y=dataset_shuffled['CO2 uptake (mmol/g)']
        df_train,df_test,df_label,df_test_label=train_test_split(x,y,test_size=size, random_state=42)


        gbr = GradientBoostingRegressor(learning_rate= .1, max_depth = 5, min_samples_leaf = 1,
                          min_samples_split = 2, n_estimators = 300,
                          subsample = 0.5, random_state=42)
        #GradientBoostingRegressor(learning_rate=i, n_estimators=j)
        gbr = gbr.fit(df_train, df_label)

        scores0 = cross_val_score(gbr, x, y , cv=fold, scoring='r2')
        print(scores0)

        print("predict output for GradientBoostingRegressor: presuure = {}".format(i))
        mse = mean_squared_error(df_test_label, gbr.predict(df_test))
        print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
        #scores=gbr.score(df_test, df_test_label)
        #pred2 = gbr.predict(df_test)
        #print("Accuracy on training set: %.3f" % pred2)
        print("mean on test set: %.3f" % scores0.mean())
        print("std on test set: %.3f" % scores0.std())

        print("==============================================")
        results0[f'{i}'] = scores0.mean()
        results20[f'{i}'] = scores0.std()


    df_scores0 = pd.DataFrame(results0, index=[0]).copy()
    df_scores20 = pd.DataFrame(results20, index=[0]).copy()


    return results0,results20,df_scores0,df_scores20


# In[141]:


# N_par_gbr(dff2,7,.15,10)


# In[142]:


def pressure_par_gbr(dataset,fold,size,n):
    
    ''' this function find effect of changes in Presuure features on co2 adsorption '''
    
    results0={}
    results20={}

    for i in range(1, n):#[.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.2,1.3,1.4,1.5]:
        
        

        dataset_shuffled=shuffle(dataset)
     
        #dataset_shuffled['Pressure (bar)']= dataset['Pressure (bar)']+i/10
        dataset_shuffled.loc[:,['Temp (°C)']]= dataset_shuffled.loc[:,['Temp (°C)']]+round(i / 3, 1)
        print(dataset_shuffled['Temp (°C)'].head(2))
        x=dataset_shuffled.drop(['CO2 uptake (mmol/g)'],axis=1)
        y=dataset_shuffled['CO2 uptake (mmol/g)']
        df_train,df_test,df_label,df_test_label=train_test_split(x,y,test_size=size, random_state=42)


        gbr = GradientBoostingRegressor(learning_rate= .1, max_depth = 5, min_samples_leaf = 1,
                          min_samples_split = 2, n_estimators = 300,
                          subsample = 0.5, random_state=42)
        #GradientBoostingRegressor(learning_rate=i, n_estimators=j)
        gbr = gbr.fit(df_train, df_label)

        scores0 = cross_val_score(gbr, x, y , cv=fold, scoring='r2')
        print(scores0)

        print("predict output for GradientBoostingRegressor: presuure = {}".format(i))
        mse = mean_squared_error(df_test_label, gbr.predict(df_test))
        print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
        #scores=gbr.score(df_test, df_test_label)
        #pred2 = gbr.predict(df_test)
        #print("Accuracy on training set: %.3f" % pred2)
        print("mean on test set: %.3f" % scores0.mean())
        print("std on test set: %.3f" % scores0.std())

        print("==============================================")
        results0[f'{i}'] = scores0.mean()
        results20[f'{i}'] = scores0.std()


    df_scores0 = pd.DataFrame(results0, index=[0]).copy()
    df_scores20 = pd.DataFrame(results20, index=[0]).copy()


    return results0,results20,df_scores0,df_scores20


# In[143]:


def pressure_par_gbr_added(dataset,fold,size,n):
    results={}
    results2={}
    
    for i in range(1, n):#[.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.2,1.3,1.4,1.5]:
        
                
        
        dataset_shuffled=shuffle(dataset)
        dataset_shuffled.loc[:,['Pressure (bar)']]= dataset_shuffled.loc[:,['Pressure (bar)']]+round(i / 30, 1)
        #dataset_shuffled['Pressure (bar)']=dataset['Pressure (bar)']+i/10
        print(dataset_shuffled['Pressure (bar)'].head(2))

        x=dataset_shuffled.drop(['CO2 uptake (mmol/g)'],axis=1)
        y=dataset_shuffled['CO2 uptake (mmol/g)']
        df_train,df_test,df_label,df_test_label=train_test_split(x,y,test_size=size, random_state=42)


        gbr = GradientBoostingRegressor(learning_rate= .1, max_depth = 5, min_samples_leaf = 1,
                          min_samples_split = 2, n_estimators = 300,
                          subsample = 0.5, random_state=42)
        #GradientBoostingRegressor(learning_rate=i, n_estimators=j)
        gbr = gbr.fit(df_train, df_label)

        scores = cross_val_score(gbr, x, y , cv=fold, scoring='r2')
        print(scores)

        print("predict output for GradientBoostingRegressor: presuure = {}".format(i))
        mse = mean_squared_error(df_test_label, gbr.predict(df_test))
        print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
        #scores=gbr.score(df_test, df_test_label)
        #pred2 = gbr.predict(df_test)
        #print("Accuracy on training set: %.3f" % pred2)
        print("mean on test set: %.3f" % scores.mean())
        print("std on test set: %.3f" % scores.std())

        print("==============================================")
        results[f'{i}'] = scores.mean()
        results2[f'{i}'] = scores.std()


    df_scores = pd.DataFrame(results, index=[0]).copy()
    df_scores2 = pd.DataFrame(results2, index=[0]).copy()


    return results,results2,df_scores,df_scores2


# In[144]:


def pressure_par_gbr2(dataset,fold,size):
    ''' this function find effect of changes in 3 pressure, temperature and MV features on co2 adsorption '''

    results={}
    results2={}
    resultsp={}
    resultst={}
    resultsm={}
    for i in range(10, 20, 2):#[.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.2,1.3,1.4,1.5]:
        for j in range(4, 32, 4):
            for k in range(1, 3, 1):
                
                dff2_shuffled=shuffle(dataset)

                dff2_shuffled['Pressure (bar)']=dff2_shuffled['Pressure (bar)']+i/10 
                dff2_shuffled['Temp (°C)']=dff2_shuffled['Temp (°C)']+j 
                dff2_shuffled['Micropore Volume (cm3/g)']=dff2_shuffled['Micropore Volume (cm3/g)']+k/10 

                x=dff2_shuffled.drop(['CO2 uptake (mmol/g)'],axis=1)
                y=dff2_shuffled['CO2 uptake (mmol/g)']
                df_train,df_test,df_label,df_test_label=train_test_split(x,y,test_size=size, random_state=42)


                gbr = GradientBoostingRegressor(learning_rate= .1, max_depth = 5, min_samples_leaf = 1,
                                  min_samples_split = 2, n_estimators = 300,
                                  subsample = 0.5, random_state=42)
                #GradientBoostingRegressor(learning_rate=i, n_estimators=j)
                gbr = gbr.fit(df_train, df_label)

                scores = cross_val_score(gbr, x, y , cv=fold, scoring='r2')
                print(scores)

                print("predict output for GradientBoostingRegressor: presuure = {}, Temp = {},  TPV = {} ".format(i,j,k))
                mse = mean_squared_error(df_test_label, gbr.predict(df_test))
                print("The mean squared error (MSE) on test set: {:.4f}".format(mse))
                #scores=gbr.score(df_test, df_test_label)
                #pred2 = gbr.predict(df_test)
                #print("Accuracy on training set: %.3f" % pred2)
                print("mean on test set: %.3f" % scores.mean())
                print("std on test set: %.3f" % scores.std())

                print("==============================================")
                
                resultsp[f'{i}'] = scores.mean()
                resultst[f'{j}'] = scores.mean()
                resultsm[f'{k}'] = scores.mean()

                results[f'{i}-{j}-{k}'] = scores.mean()
                results2[f'{i}-{j}-{k}'] = scores.std()


    df_scores = pd.DataFrame(results, index=[0]).copy()
    df_scores2 = pd.DataFrame(results2, index=[0]).copy()


    return results,results2,df_scores,df_scores2,resultsp,resultst,resultsm


# In[145]:


def evaluate_model(dataset, model,cv,split):
    '''The evaluate_model function evaluates a given regression model using cross-validation. It takes the 
    dataset, model, number of splits for cross-validation, and a splitting method (split) as input. 
    The function performs cross-validation, computes R2 scores for each fold, and returns the mean R2 score, 
    standard deviation of the scores, and the dictionary keys for different metrics calculated during the 
    cross-validation. Note that there seems to be a small issue in the function where it tries to call the 
    absolute function, which doesn't seem to be defined in the code. It should be corrected to something like 
    np.absolute or the intended function you want to use to calculate the absolute value of the scores.'''
    
    XX=dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]
    sc = StandardScaler()
    X= sc.fit_transform(XX)
    #define model evaluation method
    cv = RepeatedKFold(n_splits=split, n_repeats=1, random_state=1234)
    # evaluate model
    scores = cross_val_score(model, X, y, scoring='r2', cv=cv, n_jobs=-1)
    scores1 = cross_validate( model, X, y, scoring='r2')
    # force scores to be positive
    print('Mean MAE: %.3f (%.3f)' % (mean(scores)*100, std(scores)*100))
    print(scores)
    print()
    print(scores.mean())
    print()
    print(scores.std())
    print(sorted(scores1.keys()))
    return absolute(scores),scores1.keys()
    
 


# In[146]:


# plot the dataset and the model's line of best fit
def plot_best_fit(dataset, model):
    '''This function fits a regression model to a dataset and then displays a scatter plot of the dataset 
    along with the predicted line of best fit from the model. It helps visualize the relationship between the 
    features and the target variable as well as the model's fit to the data.'''
    
    # fut the model on all data
    XX=dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]
    sc = StandardScaler()
    X= sc.fit_transform(XX)
    model.fit(X, y)
    # plot the dataset
    
    plt.scatter(dataset['Surface Area (m2/g)'].values,dataset["CO2 uptake (mmol/g)"].values)
    # plot the line of best fit
    #yaxis = model.predict(xaxis.reshape((len(xaxis), 1)))
   # plt.plot(xaxis, yaxis, color='r')
    # show the plot
    plt.title(type(model).__name__)
    plt.show()



# In[148]:


from keras import backend as K
from tensorflow.keras.layers import BatchNormalization
from keras.layers import Dropout


def R_squared(y, y_pred):
    
    '''The R_squared function calculates the coefficient of determination (R-squared) between the predicted 
    values y_pred and the actual target values y. The R-squared value indicates how well the predicted values
    match the actual values and represents the proportion of the variance in the dependent variable that is 
    explained by the independent variables.'''
    
    residual = tf.reduce_sum(tf.square(tf.subtract(y, y_pred)))
    total = tf.reduce_sum(tf.square(tf.subtract(y, tf.reduce_mean(y))))
    r2 = tf.subtract(1.0, tf.divide(residual, total))
    return r2
#y=y_test8
#R_squared(y_test, test_preds)


# In[149]:



def first_deep(data,size,lr,batch,epoch):

    # Features (Input)
    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]
    
    x = (x-x.min())/(x.max()-x.min())
    # Label (Output)

    y = (y-y.min())/(y.max()-y.min())
    # Splitting data into train and test dataset
    x_train , x_test , y_train , y_test = train_test_split(x,y, test_size=size,
    random_state = 0)
    # Defining R2 score
    def det_coeff(y_true, y_pred):
        SS_res = K.sum(K.square(y_true - y_pred))
        SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
        return K.ones_like(SS_tot) - (SS_res / SS_tot)
    # Tuned learning rate
    learning_rate=lr
    regression1 = Sequential()
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    = 'relu', input_dim = x_train.shape[1]))
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    ='tanh' ))
    regression1.add(Dense(units= 1, kernel_initializer = 'glorot_uniform', activation
    = 'relu'))
    opt=Adam(learning_rate)
    regression1.compile(optimizer =opt , loss = 'mse',metrics=['mae'])
    # Fit the model
    regression1.fit(x_train, y_train, batch_size = batch, epochs = epoch)

    # Predict the result for train and test dataset
    y_pred_train = regression1.predict(x_train)
    y_pred_test = regression1.predict(x_test)
    # R2 results for each model
    R2_train_set= r2_score(y_train , y_pred_train)
    R2_test_set= r2_score(y_test , y_pred_test)
    # Print R2 results for each model
    print( 'R2 for train set is : ', R2_train_set )
    print( 'R2 for test set is : ', R2_test_set )
    
    return R2_train_set,R2_test_set,x_train , x_test , y_train , y_test,y_pred_train,y_pred_test


# In[150]:


#first_deep(BWDPS,.15,0.001,16,100)


# In[151]:


def first_deep2(data,size,lr,batch,epoch):

    # Features (Input)
    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]
    
    x = (x-x.min())/(x.max()-x.min())
    # Label (Output)

    y = (y-y.min())/(y.max()-y.min())
    # Splitting data into train and test dataset
    x_train , x_test , y_train , y_test = train_test_split(x,y, test_size=size,
    random_state = 0)
    # Defining R2 score
    def det_coeff(y_true, y_pred):
        SS_res = K.sum(K.square(y_true - y_pred))
        SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
        return K.ones_like(SS_tot) - (SS_res / SS_tot)
    # Tuned learning rate
    learning_rate=lr
    regression1 = Sequential()
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    = 'relu', input_dim = x_train.shape[1]))
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    ='tanh' ))
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    ='tanh' ))
    regression1.add(Dense(units= 1, kernel_initializer = 'glorot_uniform', activation
    = 'relu'))
    opt=Adam(learning_rate)
    regression1.compile(optimizer =opt , loss = 'mse')#, metrics =[det_coeff])
    # Fit the model
    regression1.fit(x_train, y_train, batch_size = batch, epochs = epoch)

    # Predict the result for train and test dataset
    y_pred_train = regression1.predict(x_train)
    y_pred_test = regression1.predict(x_test)
    # R2 results for each model
    R2_train_set= r2_score(y_train , y_pred_train)
    R2_test_set= r2_score(y_test , y_pred_test)
    # Print R2 results for each model
    print( 'R2 for train set is : ', R2_train_set )
    print( 'R2 for test set is : ', R2_test_set )
    
    return R2_train_set,R2_test_set,x_train , x_test , y_train , y_test,y_pred_train,y_pred_test


# In[152]:


def first_deep3(data,size,lr,batch,epoch):

    # Features (Input)
    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]
    
    x = (x-x.min())/(x.max()-x.min())
    # Label (Output)

    y = (y-y.min())/(y.max()-y.min())
    # Splitting data into train and test dataset
    x_train , x_test , y_train , y_test = train_test_split(x,y, test_size=size,
    random_state = 0)
    # Defining R2 score
    def det_coeff(y_true, y_pred):
        SS_res = K.sum(K.square(y_true - y_pred))
        SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
        return K.ones_like(SS_tot) - (SS_res / SS_tot)
    # Tuned learning rate
    learning_rate=lr
    regression1 = Sequential()
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    = 'relu', input_dim = x_train.shape[1]))
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    ='tanh' ))
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    ='tanh' ))
    regression1.add(Dense(units=x_train.shape[1] , kernel_initializer = 'glorot_uniform', activation
    ='tanh' ))
    regression1.add(Dense(units= 1, kernel_initializer = 'glorot_uniform', activation
    = 'relu'))
    opt=Adam(learning_rate)
    regression1.compile(optimizer =opt , loss = 'mse', metrics ='mae')
    # Fit the model
    regression1.fit(x_train, y_train, batch_size = batch, epochs = epoch)

    # Predict the result for train and test dataset
    y_pred_train = regression1.predict(x_train)
    y_pred_test = regression1.predict(x_test)
    # R2 results for each model
    R2_train_set= r2_score(y_train , y_pred_train)
    R2_test_set= r2_score(y_test , y_pred_test)
    # Print R2 results for each model
    print( 'R2 for train set is : ', R2_train_set )
    print( 'R2 for test set is : ', R2_test_set )
    
    return R2_train_set,R2_test_set,x_train , x_test , y_train , y_test,y_pred_train,y_pred_test


# In[153]:


def deep_train1(dataset,k,size,lr,batch):
        
    
    x = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)
   
    
    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]
    
    scaler_Min =scalers[k]
    
    print('dataset scaled by:      ',scalers[k])
    print()
    
    if k==0:
        x_train=x_train
        x_test=x_test
    else:
        x_train = scaler_Min.fit_transform(x_train)
        x_test = scaler_Min.fit_transform(x_test)
    
    print('shape of train set is:      ',x_train.shape)
    print('shape of train label set is:',y_train.shape)
    print()
    print('shape of test set is:      ',x_test.shape)
    print('shape of test label set is:',y_test.shape)

    neural_regressor = models.Sequential([
        keras.layers.Dense(x_train.shape[1],  activation="relu", input_shape=(x_train.shape[1],)),
        keras.layers.Dense(x_train.shape[1], activation="relu"),
        keras.layers.Dense(x_train.shape[1], activation="relu"),
        keras.layers.Dense(x_train.shape[1], activation="relu"), 
        keras.layers.Dense(1)])


    neural_regressor.summary()
    #keras2ascii(neural_regressor)
    

    optimizer = keras.optimizers.Adam(learning_rate=lr)
  
    scikeras_regressor = KerasRegressor(model=neural_regressor, optimizer=optimizer,
                                    loss=keras.losses.mean_squared_error,
                                        epochs=200, verbose=0)
     
    history=scikeras_regressor.fit(x_train, y_train,batch_size=batch,validation_data=(x_test,y_test))# validation_split=size);
    
    test_preds = scikeras_regressor.predict(x_test)
    train_preds = scikeras_regressor.predict(x_train)
    
    from sklearn.metrics import mean_squared_error

    print("Train MSE : {:.4f}".format(mean_squared_error(y_train, train_preds)))
    print("Test  MSE : {:.4f}".format(mean_squared_error(y_test, test_preds)))

    test_scoree=scikeras_regressor.score(x_test, y_test)
    print("\nTrain R^2 : {:.2f}".format(scikeras_regressor.score(x_train, y_train)*100))
    print("Test  R^2 : {:.2f}".format(scikeras_regressor.score(x_test, y_test)*100))
    
    # "Loss"
    plt.figure(figsize=(8,6),dpi=100);
        
    plt.plot(history.history_['loss'],label = 'val_loss',linewidth=1);
    plt.plot(history.history_['val_loss'],label = 'val_loss',linewidth=1);

    
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
        
       ###################
    #pp_tr = scikeras_regressor.predict(x_train)
    
    plt.figure(figsize=(6,4),dpi=150)

    
    #y_predicted=scikeras_regressor.predict(x_test)
    g = sns.JointGrid(y_test, test_preds)
    
    sns.scatterplot(x=y_train, y=train_preds, s=100, color='red', ax=g.ax_joint)
    #sns.regplot(x=y_train, y=pp_tr, color='green', ax=g.ax_joint)

    
    sns.scatterplot(x=y_test, y=test_preds, s=100, color='blue', ax=g.ax_joint)
    sns.regplot(x=y_test, y=test_preds, color='blue',ax=g.ax_joint)
    #sns.lineplot(x=y_test, y=y_predicted, ax=g.ax_joint)
    plt.ylim(0, 7.5)
    plt.xlim(0, 7.5)

    g.set_axis_labels("Actual CO2 uptake (mmol/g)",
                      "Predicted CO2 uptake (mmol/g)", fontsize =22, fontname = 'Times New Roman')
    sns.histplot(x=y_train,ax=g.ax_marg_x, color ='red')
    sns.histplot(x=y_test, ax=g.ax_marg_x, color ='blue')
    g.ax_marg_x.legend(["Train", "Test"])
    plt.locator_params(tight=None, nbins=4)
    return x_train, x_test, y_train, y_test, train_preds, test_preds,test_scoree
    


# In[154]:


deep_train1(BWDPS_shuffled,4,0.15,.00015,16)
# ## MLP deep models


# In[155]:


def mlp1(data,size,lr,batch):
    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)


    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]

    scaler_Min =scalers[4]




    x_train = scaler_Min.fit_transform(x_train)
    x_test = scaler_Min.fit_transform(x_test)

    print('shape of train set is:      ',x_train.shape)
    print('shape of train label set is:',y_train.shape)
    print()
    print('shape of test set is:      ',x_test.shape)
    print('shape of test label set is:',y_test.shape)


    trainX=x_train
    trainy=y_train

    testX=x_test
    testy=y_test

    # reshape 1d arrays to 2d arrays
    trainy = trainy.values.reshape(len(trainy),1)
    testy = testy.values.reshape(len(testy),1 )
    # created scaler
    scaler = StandardScaler()
    # fit scaler on training dataset
    scaler.fit(trainy)
    # transform training dataset
    trainy = scaler.transform(trainy)
    # transform test dataset
    testy = scaler.transform(testy)
    # define model
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model = Sequential()
    model.add(Dense(trainX.shape[1], input_dim=trainX.shape[1], activation='relu'))
    model.add(Dense(trainX.shape[1], input_dim=trainX.shape[1], activation='relu'))
    model.add(Dense(1, activation='linear'))
    # compile model
    model.compile(loss='mean_squared_error', optimizer=optimizer)#SGD(lr=0.01, momentum=0.5))
    # fit model
    history = model.fit(trainX, trainy, validation_data=(testX, testy),batch_size=batch, epochs=100, verbose=0)
    # evaluate the model
    train_mse = model.evaluate(trainX, trainy, verbose=0)
    test_mse = model.evaluate(testX, testy, verbose=0)
    print('Train: %.3f, Test: %.3f' % (train_mse, test_mse))

    train_preds = model.predict(trainX)
    test_preds = model.predict(testX)
    print('R_squared_train= ', R_squared(trainy, train_preds))

    print('R_squared_test= ', R_squared(testy, test_preds))

    # plot loss during training
    plt.title('Loss / Mean Squared Error')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()


# In[156]:


#mlp1(BWDPS,.15,0.0001,4)


# In[157]:


mlp1(BWDPS,.15,0.0001,4)


# In[160]:


#mlp1(BWDPS_shuffled,.15,0.0001,4)


# In[161]:


mlp1(BWDPS_shuffled,.15,0.0001,4)


# In[164]:


mlp1(BWDPS_38_shuffled,.15,0.0001,4)


# In[167]:


mlp1(BWDPS_46_shuffled,.15,0.0001,4)


# In[168]:


def mlp2(data,size,lr,batch):
    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)


    scalers = [None, MinMaxScaler(), MaxAbsScaler(), RobustScaler(),StandardScaler(),
               QuantileTransformer(n_quantiles=5, random_state=42, output_distribution='normal')]

    scaler_Min =scalers[4]




    x_train = scaler_Min.fit_transform(x_train)
    x_test = scaler_Min.fit_transform(x_test)

    print('shape of train set is:      ',x_train.shape)
    print('shape of train label set is:',y_train.shape)
    print()
    print('shape of test set is:      ',x_test.shape)
    print('shape of test label set is:',y_test.shape)


    trainX=x_train
    trainy=y_train

    testX=x_test
    testy=y_test

    # reshape 1d arrays to 2d arrays
    trainy = trainy.values.reshape(len(trainy),1)
    testy = testy.values.reshape(len(testy),1 )
    # created scaler
    scaler = StandardScaler()
    # fit scaler on training dataset
    scaler.fit(trainy)
    # transform training dataset
    trainy = scaler.transform(trainy)
    # transform test dataset
    testy = scaler.transform(testy)
    # define model
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model = Sequential()
    model.add(Dense(trainX.shape[1], input_dim=trainX.shape[1], activation='relu'))
    model.add(Dense(trainX.shape[1], input_dim=trainX.shape[1], activation='relu'))

    model.add(Dense(trainX.shape[1]//2, input_dim=trainX.shape[1], activation='relu'))
    model.add(Dense(1, activation='linear'))
    # compile model
    model.compile(loss='mean_squared_error', optimizer=optimizer)#SGD(lr=0.01, momentum=0.5))
    # fit model
    history = model.fit(trainX, trainy, validation_data=(testX, testy),batch_size=batch, epochs=100, verbose=0)
    # evaluate the model
    train_mse = model.evaluate(trainX, trainy, verbose=0)
    test_mse = model.evaluate(testX, testy, verbose=0)
    print('Train: %.3f, Test: %.3f' % (train_mse, test_mse))

    train_preds = model.predict(trainX)
    test_preds = model.predict(testX)
    print('R_squared_train= ', R_squared(trainy, train_preds))

    print('R_squared_test= ', R_squared(testy, test_preds))

    # plot loss during training
    plt.title('Loss / Mean Squared Error')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()


# In[173]:


mlp2(BWDPS_shuffled,.15,0.0001,4)


# In[176]:


mlp2(BWDPS_38_shuffled,.15,0.0001,4)


# In[179]:


mlp2(BWDPS_46_shuffled,.15,0.0001,4)


# ## BWDPS_46 models


# In[180]:


from sklearn.preprocessing import StandardScaler

def BWDPS_46_1(dataset, size, lr, batch, epoch):
    
    x = dataset.drop("CO2 uptake (mmol/g)", axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    
    x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

    optimizer = keras.optimizers.Adam(learning_rate=lr)
    
    regressor = Sequential()
    regressor.add(BWDPS_46(units=x_train.shape[1], return_sequences=True, input_shape=(x_train.shape[1], 1)))
    regressor.add(Dropout(0.1))
    regressor.add(BatchNormalization())
    regressor.add(BWDPS_46(units=x_train.shape[1], return_sequences=True))
    regressor.add(Dropout(0.1))
    regressor.add(BatchNormalization())
    regressor.add(BWDPS_46(units=x_train.shape[1], return_sequences=True))
    regressor.add(Dropout(0.1))
    regressor.add(BatchNormalization())
    regressor.add(BWDPS_46(units=x_train.shape[1]))
    regressor.add(Dropout(0.1))
    regressor.add(Dense(units=1, activation='relu'))
    regressor.compile(optimizer=optimizer, loss='mean_squared_error')
     
    hist = regressor.fit(x_train, y_train, epochs=epoch, batch_size=batch, validation_data=(x_test, y_test),verbose=0)
    regressor.summary()  
    
    test_preds = regressor.predict(x_test)
    train_preds = regressor.predict(x_train)
    train_preds = train_preds.reshape(train_preds.shape[0],)
    test_preds = test_preds.reshape(test_preds.shape[0],)

    print("Train MSE : {:.4f}".format(mean_squared_error(y_train, train_preds)))
    print("Test  MSE : {:.4f}".format(mean_squared_error(y_test, test_preds)))
    print("R-score-train : {:.4f}".format(R_squared(y_train, train_preds)))
    print("R-score-test : {:.4f}".format(R_squared(y_test, test_preds)))
    
    plt.figure(figsize=(6,4), dpi=100)
    plt.plot(hist.history["loss"], label="Training Loss")
    plt.plot(hist.history["val_loss"], label="Validation Loss")
    plt.legend()
    plt.show()

    return R_squared(y_train, train_preds), R_squared(y_test, test_preds)



# In[181]:


#LSTM_1(BWDPS_38_shuffled,.15,.001,16,40)


# In[182]:


def conv_lstm(data,size,lr,batch,epoch):
    ''' convolutiona_lstm'''


    x = data.drop("CO2 uptake (mmol/g)",axis=1)
    y = data["CO2 uptake (mmol/g)"]

    x = (x-x.min())/(x.max()-x.min())
        # Label (Output)

    y = (y-y.min())/(y.max()-y.min())


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)

   
    x_train.shape[1]




    print(x_train.shape)
    print(y_train.shape)



    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv1D(filters=x_train.shape[1],
                               kernel_size=5,
                               padding="same",
                               activation="relu",
                               input_shape=(x_train.shape[1],1)),
         tf.keras.layers.MaxPooling1D(pool_size=1),
        tf.keras.layers.Conv1D(filters=x_train.shape[1],
                               kernel_size=5,
                               padding="same",
                               activation="relu"),
        tf.keras.layers.MaxPooling1D(pool_size=1),
        tf.keras.layers.LSTM(x_train.shape[1], return_sequences=True),
        tf.keras.layers.LSTM(x_train.shape[1], return_sequences=False),
        tf.keras.layers.Dense(1),
    ])
    optimizer1 = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  optimizer=optimizer1,
                  metrics=['mae'])
    model.summary()


    hist = model.fit(x_train, y_train,validation_data=(x_test,y_test), batch_size=batch, epochs=epoch)

    #resuilts model
    test_preds = model.predict(x_test)
    train_preds = model.predict(x_train)

    train_preds=train_preds.reshape(train_preds.shape[0],)
    test_preds=test_preds.reshape(test_preds.shape[0],)

    print( y_train.shape)

    print( y_test.shape)
    print( test_preds.shape)


    print( test_preds.shape)


    test_preds=np.squeeze(np.asarray(test_preds))
    train_preds=np.squeeze(np.asarray(train_preds))

    print("Train MSE : {:.4f}".format(mean_squared_error(y_train, train_preds)))
    print("Test  MSE : {:.4f}".format(mean_squared_error(y_test, test_preds)))
    

    print("R-score-train : {:.4f}".format(R_squared(y_train, train_preds)))
    print("R-score-test : {:.4f}".format(R_squared(y_test, test_preds)))
    
    plt.plot(figsize=(6,4),dpi=100)
    plt.plot(hist.history["loss"], label="Training Loss")
    plt.plot(hist.history["val_loss"], label="Validation Loss")
    plt.legend()


# In[183]:


#conv_lstm(BWDPS,.15,.0001,4,40)


# In[184]:


#for BWDPS lstm


train_df=[0.7573,0.7656,0.7180,0.7434,0.7490,0.7536,0.6946]
train_df=np.array(train_df)
print(train_df.mean())
print(train_df.std())

print()
test_df=[0.7380,0.7583,0.7227,0.7221,0.7393,.7461,0.7388]
test_df=np.array(test_df)
print(test_df.mean())
print(test_df.std())


# In[185]:


def plot_history(hist):

  train_loss = hist.history['loss']
  val_loss = hist.history['val_loss']

  train_acc = hist.history['mae']
  val_acc = hist.history['val_mae']

  plt.figure()

  plt.plot
  plt.plot(np.arange(1,len(train_loss)+1), train_loss)
  plt.plot(np.arange(1,len(train_loss)+1), val_loss)
  plt.legend(['train','validation'])
  plt.grid()
  plt.xlabel('epoch')
  plt.ylabel('loss')
    
  plt.figure()

  plt.plot
  plt.plot(np.arange(1,len(train_acc)+1), train_acc)
  plt.plot(np.arange(1,len(val_acc)+1), val_acc)
  plt.legend(['train','validation'])
  plt.grid()
  plt.xlabel('epoch')
  plt.ylabel('loss')  
    


# ## Convolutional deep models


# In[186]:


def deep_conv12(dataset,size,lr,batch):
    

    xx = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    x = xx.to_numpy()
    print(type(x))
    scaler_Min =StandardScaler()#MinMaxScaler()
    x = scaler_Min.fit_transform(xx)

    print(x.shape)

    x = x.reshape(x.shape[0], x.shape[1], 1)
    print(x.shape)

    xtrain, xtest, ytrain, ytest=train_test_split(x, y, test_size=size, random_state=42)
    optimizer = keras.optimizers.Adam(learning_rate=lr)

    model = Sequential()
    model.add(Conv1D(x.shape[1], 1, activation="relu", input_shape=(x.shape[1],1)))
    model.add(Flatten())
    model.add(Dense(x.shape[1], activation="relu"))
    model.add(Dense(1))
    model.compile(loss="mse", optimizer=optimizer)#"adam")
    model.summary()
    history=model.fit(xtrain, ytrain, batch_size=batch,epochs=120, verbose=0, validation_split=size)

    ypred = model.predict(xtest)
    print(model.evaluate(xtrain, ytrain))
    print("MSE: %.4f" % mean_squared_error(ytest, ypred))
    score=r2_score(ytest, ypred)
    print("r2: %.4f" % r2_score(ytest, ypred))

    print(history.history.keys())
    # "Loss"
    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'val_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()
    
    plt.figure(figsize=(8,6),dpi=100);

    x_ax = range(len(ypred))
    plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
    plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()
    return score


# In[187]:


deep_conv12(BWDPS_shuffled,.15,.0001,4)


# In[189]:


def deep_conv2(dataset, test_size, lr, batch_size):
    '''The deep_conv2 function performs deep learning regression using Convolutional Neural Networks (CNNs)
    on structured data. This function applies Conv1D layers to a structured dataset for regression. 
    It scales the data using StandardScaler, reshapes it for CNN compatibility, and then splits it into 
    training and test sets. The function constructs a neural network with Conv1D and Dense layers, compiles it
    , and trains it on the training data. It evaluates the model's performance on both the test and 
    training sets, calculates metrics like Mean Squared Error (MSE) and R-squared, and visualizes loss 
    and predicted vs. original values. The function returns the R-squared score on the test set, 
    R-squared score on the training set, and the standard deviation of predictions on the test set.'''
    
    X=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = (y - y.mean()) / y.std()


    # Reshape the features into a 3D tensor for Conv1D layer
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_scaled, test_size=test_size, random_state=42)

    # Create the neural network model
    model = Sequential()
    model.add(Conv1D(X_reshaped.shape[1], 1, activation="relu", input_shape=(X_reshaped.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(X_reshaped.shape[1], activation="relu"))
    model.add(Dense(1))
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss="mse", optimizer=optimizer)

    # Fit the model to the training data
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=120, verbose=0, validation_split=test_size)

    #history = model.fit(xtrain, ytrain, batch_size=batch, epochs=120, verbose=0, validation_split=size)
    xtest=X_test
    ytest=y_test
    xtrain=X_train
    ytrain=y_train
    ypred = model.predict(xtest)
    print("MSE_test: %.4f" % mean_squared_error(ytest, ypred))
    score = r2_score(ytest, ypred)
    print("r2_test: %.4f" % score)

    ypredtr = model.predict(xtrain)
    print("MSE_train: %.4f" % mean_squared_error(ytrain, ypredtr))
    scoretr = r2_score(ytrain, ypredtr)
    print("r2_train: %.4f" % scoretr)

    
    ytest =np.array(ytest)
    ypred = np.array(ypred)
    std = np.std(ytest - ypred)
    print("Standard deviation of predictions on test set: %.4f" % std)

    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'val_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()
    
    plt.figure(figsize=(8,6),dpi=100);

    x_ax = range(len(ypred))
    plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
    plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()

    return score, scoretr, std


# In[191]:


deep_conv2(BWDPS,.15,0.0001,4)


# In[196]:


deep_conv2(BWDPS_shuffled,.15,0.0001,4)


# In[199]:


deep_conv2(BWDPS_38_shuffled,.15,0.0001,4)


# In[ ]:






# In[200]:




#deep_conv2(BWDPS_38_shuffled,.15,0.0001,4)


# In[202]:


deep_conv2(BWDPS_46_shuffled,.15,0.0001,4)


# In[203]:


#deep_conv2(BWDPS_46_shuffled,.15,0.0001,4)


# In[206]:


def deep_conv22(dataset,i,j,k):
    

    xx = dataset.drop("CO2 uptake (mmol/g)",axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    x = xx.to_numpy()
    print(type(x))
    scaler_Min =StandardScaler()#MinMaxScaler()
    x = scaler_Min.fit_transform(xx)

    print(x.shape)

    x = x.reshape(x.shape[0], x.shape[1], 1)
    print(x.shape)

    xtrain, xtest, ytrain, ytest=train_test_split(x, y, test_size=i, random_state=42)
    optimizer = keras.optimizers.Adam(learning_rate=j)

    model = Sequential()
    model.add(Conv1D(x.shape[1], 1, activation="relu", input_shape=(x.shape[1],1)))
    model.add(Flatten())
    model.add(Dense(x.shape[1], activation="relu"))
    model.add(Flatten())
    model.add(Dense(x.shape[1], activation="relu"))
    model.add(Dense(1))
    model.compile(loss="mse", optimizer=optimizer)#"adam")
    model.summary()
    history=model.fit(xtrain, ytrain, batch_size=k,epochs=120, verbose=0, validation_split=i)

    
       
    ypred_train = model.predict(xtrain)

    train_score = r2_score(ytrain, ypred_train)
    print("r2 for train set: %.4f" % train_score)

    print("Train MSE: %.4f" % mean_squared_error(ytrain, ypred_train))
    
    ypred = model.predict(xtest)
    print(model.evaluate(xtrain, ytrain))
    print("Test MSE: %.4f" % mean_squared_error(ytest, ypred))
    score=r2_score(ytest, ypred)
    print("Test r2: %.4f" % r2_score(ytest, ypred))

    print(history.history.keys())
    # "Loss"
    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'val_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()
    
    plt.figure(figsize=(8,6),dpi=100);

    x_ax = range(len(ypred))
    plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
    plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()
    return score


# In[208]:


#deep_conv22(BWDPS_38_shuffled,.15,0.0001,4)


# In[209]:


def deep_conv23(dataset, test_size, lr, batch_size):
    X = dataset.drop("CO2 uptake (mmol/g)", axis=1)
    y = dataset["CO2 uptake (mmol/g)"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)
    y_scaler = StandardScaler()
    y_scaled = y_scaler.fit_transform(y.values.reshape(-1, 1)).flatten()

    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_scaled, test_size=test_size, random_state=42)

    optimizer = Adam(learning_rate=lr)

    model = Sequential()
    model.add(Conv1D(X_reshaped.shape[1], 1, activation="relu", input_shape=(X_reshaped.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(X_reshaped.shape[1], activation="relu"))
    model.add(Dense(1))
    model.compile(loss="mse", optimizer=optimizer)
    model.summary()

    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=120, verbose=0, validation_split=test_size)

    ypred = model.predict(X_test)
    mse_test = mean_squared_error(y_test, ypred)
    r2_test = r2_score(y_test, ypred)
    print("MSE_test: %.4f" % mse_test)
    print("r2_test: %.4f" % r2_test)

    plt.figure(figsize=(8, 6), dpi=100)
    plt.plot(history.history['loss'], label='train_loss', linewidth=1)
    plt.plot(history.history['val_loss'], label='val_loss', linewidth=1)
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()

    plt.figure(figsize=(8, 6), dpi=100)
    x_ax = range(len(ypred))
    plt.scatter(x_ax, y_test, s=5, color="blue", label="original")
    plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()

    return r2_test


# In[210]:


#deep_conv23(BWDPS_46_shuffled,.15,0.0001,4)


# In[211]:


def deep_conv24(dataset, test_size, lr, batch_size):
    
    X=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = (y - y.mean()) / y.std()


    # Reshape the features into a 3D tensor for Conv1D layer
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_scaled, test_size=test_size, random_state=42)

    # Create the neural network model
    model = Sequential()
    model.add(Conv1D(X_reshaped.shape[1], 1, activation="relu", input_shape=(X_reshaped.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(X_reshaped.shape[1], activation="relu"))
    model.add(Dense(1))
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss="mse", optimizer=optimizer)

    # Fit the model to the training data
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=120, verbose=0, validation_split=test_size)

    #history = model.fit(xtrain, ytrain, batch_size=batch, epochs=120, verbose=0, validation_split=size)
    xtest=X_test
    ytest=y_test
    xtrain=X_train
    ytrain=y_train
    ypred = model.predict(xtest)
    print("MSE_test: %.4f" % mean_squared_error(ytest, ypred))
    score = r2_score(ytest, ypred)
    print("r2_test: %.4f" % score)

    ypredtr = model.predict(xtrain)
    print("MSE_train: %.4f" % mean_squared_error(ytrain, ypredtr))
    scoretr = r2_score(ytrain, ypredtr)
    print("r2_train: %.4f" % scoretr)

    
    ytest =np.array(ytest)
    ypred = np.array(ypred)
    std = np.std(ytest - ypred)
    print("Standard deviation of predictions on test set: %.4f" % std)

    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'val_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()
    
    plt.figure(figsize=(8,6),dpi=100);

    x_ax = range(len(ypred))
    plt.scatter(x_ax, ytest, s=5, color="blue", label="original")
    plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()

    return score, scoretr, std


# In[212]:


#deep_conv24(BWDPS_46_shuffled,.15,0.0001,4)


# In[213]:


deep_conv2(BWDPS_38_shuffled,.15,0.0001,4)


# In[214]:


def deep_conv2_oplot(dataset, test_size, lr, batch_size):
    
    X=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = (y - y.mean()) / y.std()


    # Reshape the features into a 3D tensor for Conv1D layer
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_scaled, test_size=test_size, random_state=42)

    # Create the neural network model
    model = Sequential()
    model.add(Conv1D(X_reshaped.shape[1], 1, activation="relu", input_shape=(X_reshaped.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(X_reshaped.shape[1], activation="relu"))
    model.add(Dense(1))
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss="mse", optimizer=optimizer)

    # Fit the model to the training data
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=120, verbose=0, validation_split=test_size)

    ypred = model.predict(X_test)
    ypred = np.squeeze(ypred)  # Remove unnecessary dimension
    ypred_rescaled = ypred * y.std() + y.mean()  # Rescale predictions
    ytest_rescaled = y_test * y.std() + y.mean() # Rescale original target values
    
    print("MSE_test: %.4f" % mean_squared_error(ytest_rescaled, ypred_rescaled))
    score = r2_score(ytest_rescaled, ypred_rescaled)
    print("r2_test: %.4f" % score)

    ypredtr = model.predict(X_train)
    ypredtr = np.squeeze(ypredtr)  # Remove unnecessary dimension
    ypredtr_rescaled = ypredtr * y.std() + y.mean() # Rescale predictions
    ytrain_rescaled = y_train * y.std() + y.mean() # Rescale original target values
    
    print("MSE_train: %.4f" % mean_squared_error(ytrain_rescaled, ypredtr_rescaled))
    scoretr = r2_score(ytrain_rescaled, ypredtr_rescaled)
    print("r2_train: %.4f" % scoretr)
    
    std = np.std(ytest_rescaled - ypred_rescaled)
    print("Standard deviation of predictions on test set: %.4f" % std)

    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'train_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()

    plt.figure(figsize=(8,6),dpi=100);

    x_ax = range(len(ypred_rescaled))
    plt.scatter(x_ax, ytest_rescaled, s=5, color="blue", label="original")
    plt.scatter(x_ax, ypred_rescaled, s=5, color="red", label="predicted")

    #plt.plot(x_ax, ypred_rescaled, lw=0.8, color="red", label="predicted")
    plt.legend()
    plt.show()

    return score, scoretr, std


# In[215]:


#deep_conv2_oplot(BWDPS_38_shuffled,.15,0.0001,4)


# In[216]:


def deep_conv2_oplot_mse(dataset, test_size, lr, batch_size):
    
    X=dataset.drop(['CO2 uptake (mmol/g)'],axis=1)
    y=dataset['CO2 uptake (mmol/g)']
    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = (y - y.mean()) / y.std()


    # Reshape the features into a 3D tensor for Conv1D layer
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y_scaled, test_size=test_size, random_state=42)

    # Create the neural network model
    model = Sequential()
    model.add(Conv1D(X_reshaped.shape[1], 1, activation="relu", input_shape=(X_reshaped.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(X_reshaped.shape[1], activation="relu"))
    model.add(Dense(1))
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model.compile(loss="mse", optimizer=optimizer)

    # Fit the model to the training data
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=120, verbose=0, validation_split=test_size)

    ypred = model.predict(X_test)
    ypred = np.squeeze(ypred)  # Remove unnecessary dimension
    ypred_rescaled = ypred * y.std() + y.mean()  # Rescale predictions
    ytest_rescaled = y_test * y.std() + y.mean() # Rescale original target values
    
    mse_test = mean_squared_error(ytest_rescaled, ypred_rescaled) # calculate MSE for test set
    print("MSE_test: %.4f" % mse_test)
    score = r2_score(ytest_rescaled, ypred_rescaled)
    print("r2_test: %.4f" % score)

    ypredtr = model.predict(X_train)
    ypredtr = np.squeeze(ypredtr)  # Remove unnecessary dimension
    ypredtr_rescaled = ypredtr * y.std() + y.mean() # Rescale predictions
    ytrain_rescaled = y_train * y.std() + y.mean() # Rescale original target values
    
    print("MSE_train: %.4f" % mean_squared_error(ytrain_rescaled, ypredtr_rescaled))
    scoretr = r2_score(ytrain_rescaled, ypredtr_rescaled)
    print("r2_train: %.4f" % scoretr)
    
    std = np.std(ytest_rescaled - ypred_rescaled)
    print("Standard deviation of predictions on test set: %.4f" % std)

    plt.figure(figsize=(8,6),dpi=100);
    plt.plot(history.history['loss'],label = 'train_loss',linewidth=1);
    plt.plot(history.history['val_loss'],label = 'val_loss',linewidth=1);
    plt.title('model loss');
    plt.ylabel('loss');
    plt.xlabel('epoch');
    plt.legend(['train', 'validation'], loc='upper right');
    plt.show()

    plt.figure(figsize=(8,6),dpi=200)
    x_ax = range(len(ypred_rescaled))
    plt.scatter(x_ax, ytest_rescaled, s=5, color="blue", label="original")
    plt.scatter(x_ax, ypred_rescaled, s=5, color="red", label="predicted")

    # Add text box with MSE value for test set
    plt.text(0.88, 0.85, "MSE_test: %.2f" % mse_test, transform=plt.gca().transAxes, fontsize=10,
            verticalalignment='top')

    plt.legend()
    plt.show()

    return score, scoretr, std


# In[217]:



deep_conv2_oplot_mse(BWDPS_38_shuffled,.15,0.0001,4)
deep_conv2_oplot_mse(BWDPS_38_shuffled,.15,0.0001,4)

