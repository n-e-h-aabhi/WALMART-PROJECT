#!/usr/bin/env python
# coding: utf-8

# # WALMART PROJECT
Use statistical analysis, EDA, outlier analysis, and handle the missing values to come up with various
insights that can give them a clear perspective on the following:
a. If the weekly sales are affected by the unemployment rate, if yes - which stores
are suffering the most?
b. If the weekly sales show a seasonal trend, when and what could be the reason?
c. Does temperature affect the weekly sales in any manner?
d. How is the Consumer Price index affecting the weekly sales of various stores?
e. Top performing stores according to the historical data.
f. The worst performing store, and how significant is the difference between the
highest and lowest performing stores.
2. Use predictive modeling techniques to forecast the sales for each store for the next 12 weeks.
# In[1]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


# In[2]:


df=pd.read_csv(r"C:\Users\Dell\Downloads\Walmart DataSet.csv")
df


# In[3]:


df.shape


# In[4]:


df.info()


# In[5]:


df.isnull().sum()


# In[6]:


df.head()


# In[7]:


df.tail()


# In[8]:


df.duplicated().sum()


# In[9]:


for col in df.columns:
    if (df[col].dtype!=object):
        plt.boxplot(df[col])
        plt.xlabel(col)
        plt.show()


# In[10]:


out_col=["Weekly_Sales","Unemployment"]


# In[11]:


for col in out_col:
    q1=df[col].quantile(0.25)
    q3=df[col].quantile(0.75)
    iqr=q3-q1
    ul=q3+1.5*iqr
    ll=q1-1.5*iqr
    df=df[(df[col]>=ll)& (df[col]<=ul)]


# In[12]:


for col in df.columns:
    if (df[col].dtype!=object):
        plt.boxplot(df[col])
        plt.xlabel(col)
        plt.show()


# In[13]:


df.describe()


# In[14]:


sns.pairplot(df)
plt.show()


# In[15]:


# To find the correlation between weekly sales and unemployment
df.corr()


# In[16]:


sns.heatmap(df.corr())


# INFERENCE:As the correlation between weekly_sales and unemployment is -0.073227.Unemployment increases weekly sales decreases.

# In[17]:


#a.If the weekly sales are affected by the unemployment rate, if yes - which stores are suffering the most?
correlation_per_store = df.groupby('Store')[['Weekly_Sales', 'Unemployment']].corr().iloc[0::2, -1]
correlation_per_store 
stores_suffering = correlation_per_store.groupby('Store').min().idxmin()

print("Stores suffering the most due to unemployment rate:")
print(stores_suffering)

# Scatter plot of CPI vs Weekly Sales for each store
sns.scatterplot(data=df, x='Unemployment', y='Weekly_Sales', hue='Store')
plt.title('Unemployment vs Weekly Sales for each store')
plt.xlabel('Unemployment')
plt.ylabel('Weekly Sales')
plt.show()


# In[18]:


#b.If the weekly sales show a seasonal trend, when and what could be the reason?


# In[19]:


#c. Does temperature affect the weekly sales in any manner?
correlation = df['Temperature'].corr(df['Weekly_Sales'])
print("Correlation coefficient between temperature and weekly sales:", correlation)


# INFERENCE:As the correlation between weekly_sales and temperature is -0.040918.
#     There is little to no correlation between temperature and weekly sales.

# In[20]:


#d. How is the Consumer Price index affecting the weekly sales of various stores?
# Calculate the correlation coefficient between CPI and weekly sales for each store
correlation_by_store = df.groupby('Store')[['CPI', 'Weekly_Sales']].corr().iloc[0::2,-1]
print("Correlation coefficient between CPI and weekly sales for each store:")
print(correlation_by_store)

# Scatter plot of CPI vs Weekly Sales for each store
sns.scatterplot(data=df, x='CPI', y='Weekly_Sales', hue='Store')
plt.title('CPI vs Weekly Sales for each store')
plt.xlabel('CPI')
plt.ylabel('Weekly Sales')
plt.show()


# In[21]:


#eTop performing stores according to the historical data.
# Calculate total sales for each store
total_sales_by_store = df.groupby('Store')['Weekly_Sales'].sum()

# Sort stores based on total sales in descending order
top_store = total_sales_by_store.sort_values(ascending=False)

# Print the top performing stores
print("Top 10 performing stores based on total sales:")
top_store.head(10)


# In[22]:


#f.The worst performing store, and how significant is the difference between the highest and lowest performing stores.

# Sort stores based on total sales in ascending order
worst_score = total_sales_by_store.sort_values()

# Print the top performing stores
print("Top  performing stores based on total sales:")
worst_score.head(5)


# In[23]:


# Calculate the difference between the highest and lowest performing stores
highest_sales = total_sales_by_store.max()
lowest_sales = total_sales_by_store.min()
difference = highest_sales - lowest_sales

# Print the significance of the difference
print("Difference between highest and lowest performing stores:", difference)


# # FORECASTING

# In[24]:


get_ipython().system('pip install prophet')


# In[25]:


from prophet import Prophet


# In[26]:


df


# In[27]:


df.info()


# In[28]:


df['Date'] = pd.to_datetime(df['Date'])


# In[26]:


# Loop over each store
for store_id, store_data in df.groupby('Store'):
    print("Forecasting sales for Store", store_id)
    
    # Prepare the data for Prophet
    sales_data = store_data[['Date', 'Weekly_Sales']]
    sales_data.columns = ['ds', 'y']  # Rename columns for Prophet
    
    # Create and fit Prophet model
    model = Prophet(interval_width=0.95)
    model.fit(sales_data)
    
    # Make future dataframe for the next 12 weeks
    future = model.make_future_dataframe(periods=12, freq='W')
    
    # Make predictions
    forecast = model.predict(future)
    
    # Print or store the forecasted values
    forecasted_sales = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
    print("Forecasted sales for the next 12 weeks:")
    print(forecasted_sales[['ds', 'yhat']])
    
    confirmed_plot=model.plot(forecast)


# In[29]:


from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(df['Weekly_Sales'],period=12)
decomposition.plot()


# In[ ]:




