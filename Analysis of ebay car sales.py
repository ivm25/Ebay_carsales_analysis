#!/usr/bin/env python
# coding: utf-8

# # Analysing ebay car sales

# ### Table of Contents
# ***
# 1 [DEFINE](#definition)
# 
# 1.1 [BUSINESS PROBLEM](#problem)
# 
# 2 [DISCOVER](#discover)
# 
# 2.1 [Loading](#loadthefile)
# 
# 2.2 [Exploring the data](#etl)
# 

# ### 1 DEFINE
# <a id="#definition"></a>
# 
# *Scope of the project:
# 
# *Assumptions and outlines:

# ### 1.1 BUSINESS PROBLEM
# <a id="problem"></a>
# 
# *Cleaning and analysing the cleaned used car listings scraped data for a classifieds section of the German ebay website.*
# 
# *Coming out with clear insights as to which brands have the highest mileage/highest price*
# 
# 
# 
# **Source of the data: https://data.world/data-society/used-cars-data**
# 
# 
# 
# 

# ### 2 DISCOVER
# <a id="#discover"></a>
# 

# ### 2.1 LOADING
# <a id="#loadthefile"></a>

# In[1]:


import pandas as pd
import numpy as np
import dtale

autos = pd.read_csv('autos.csv', encoding = 'Windows-1252')
autos


# In[2]:


autos.info()


# In[3]:


autos.head()


# *Key Observations*
# ***
# 
# 1. There are null values for the columns:(vehicleType,gearbox,model,fuelType,notRepairedDamage)
# 
# 2. There are ints and object type columns in our dataset, which might need to be altered, depending upon the analysis.
# 
# 3. The first few rows also show that there are multiple date columns, out of which the first one shows the date of crawling, one shows the last seen timings and a column that shows the creation of listing.
# 
# 4. In addition, there are columns with German and English strings, whih might need to be replaced or combined, depending upon our analysis.
# 
# 5. A few columns are in camelcase and a few are in snakecase, which complicates the analysis a little bit.

# ### 2.2 Exploring the data
# <a id="#etl"></a>

# In[4]:


autos_copy=autos.columns.copy()

# Create a function to clean the column names.
# The function takes in a string and replaces it with the desired or choice name, coverts the string to lower case


def clean_column_names(s):
    s=s.replace("yearOfRegistration","registration_year")
    s=s.replace("monthOfRegistration","registration_month")
    s=s.replace("notRepairedDamage","unrepaired_damage")
    s=s.replace("dateCreated","ad_created")
    s=s.lower()
    return s



names = []
# Looping through the function and updating the names list
for name in autos_copy:
    name = clean_column_names(name)
    names.append(name)
autos.columns = names  


# In[5]:


#Inspect the new/modified column names
autos.columns


# **Some of the column names still need to be converted from camelcase to snakecase**

# In[6]:


#Inspecting the data
autos.head()


# **Made changes to column names to more human readable names, which will make the analysis easier as move forward into the project**

# In[7]:


#Having a detailed look at all the columns of the data
autos.describe(include = 'all')


# **There are a few columns that just have one or two values and are possible candidates for removal later on, for example**:
# 
# 1. Offertype
# 2. Seller
# 
# 
# **Price and Kilometer columns are text types and should be converted to numeric type, as well as the "registration_year" column which is not in the correct date format yet.**

# In[8]:


# Converting the Kilometer and price column to numeric types

autos["kilometer"] = pd.to_numeric(autos["kilometer"])


autos["price"] = pd.to_numeric(autos["price"])


#Insecting the shape of price column
autos["price"].unique().shape

#Inspecting the shape of Kilometer column
autos["kilometer"].unique().shape


# **To further make the analysis robust, we will sort the values of price and kilometer columns after having an estimate of the unique values**

# In[9]:


autos["price"].value_counts(ascending = False).sort_index(ascending = True).head()


autos["kilometer"].value_counts(ascending = True).head()


# In[10]:


print(autos["ad_created"].value_counts(normalize=True, dropna=False).sort_index())


print(autos["datecrawled"].value_counts(normalize=True, dropna=False).sort_index())


print(autos["lastseen"].value_counts(normalize=True, dropna=False).sort_index())


# In[11]:


autos["registration_year"].describe()


# **The registration year cannot be 1000 (min value) and also cant be 9999 (max value)**. Therefore, will pick a more reasonable range of years for the analysis. 
# 
# Will count all the listings of cars within 1900 and 2016 and see if that starts to make more sense.

# In[12]:


autos[autos["registration_year"].between(1900,2016)].describe()


# In[13]:


#Filter out rows outside of the extreme points identified, i.e. 1900, 2016.
autos = autos[autos["registration_year"].between(1900,2016)]


# In[14]:


#Inspecting the data statistics after removal of above identified rows
autos.describe()


# In[15]:


#Inpscting the "registration_year" column in more detail, specifically getting the value_counts and estimating the most common year.

autos["registration_year"].value_counts(normalize = True)


# In[16]:


dtale.show(autos)


# **Write a summary of the above steps, as in the removal of outliers and the calculation of value counts for the registration year.**

# **The next section of analysis could essentially focus on the estimation of mean price and mileage across brands**
# 
# - We will group (Aggregate the data) across the most common brands, create dictionaries for each of the variables and save the values
# 
# 

# In[17]:


count_of_brands = autos["brand"].value_counts(normalize=True)


#Restricting the above analysis to the top 5% of the brands, would be a reasonable assumption here


most_common_brands = count_of_brands[count_of_brands>0.05].index


# In[18]:


try:
    print(most_common_brands)
except:
    print("Exception occurred") 


# In[19]:


aggregation_over_brands = {}

for b in most_common_brands:
    new_brands = autos[autos["brand"]==b]
    mean_price = new_brands["price"].mean()
    aggregation_over_brands[b]=int(mean_price)
    
    
aggregation_over_brands


# **Explain your results here**

# In[20]:


mean_mileage_dict = {}

for b in most_common_brands:
    new_brands = autos[autos["brand"]==b]
    mean_mileage = new_brands["kilometer"].mean()
    mean_mileage_dict[b] = mean_mileage
    
mean_mileage_dict


# **Convert the dictionary output to a series and then a pandas datframe for simple, clear explanations**

# In[21]:


mean_price_s=pd.Series(aggregation_over_brands)


print(mean_price_s)
df_price=pd.DataFrame(mean_price_s, columns = ['mean_price'])
df_price


# In[22]:


mean_mileage_s = pd.Series(mean_mileage_dict)
print(mean_mileage_s)

df_mileage = pd.DataFrame(mean_mileage_s, columns = ['mileage'])
df_mileage


# In[ ]:





# #### Data cleaning next steps:
# 
# ***
# 
# 1. Identify categorical data that uses german words, translate them and map the values to their english counterparts
# Convert the dates to be uniform numeric data, so "2016-03-21" becomes the integer 20160321.
# 
# 2. See if there are particular keywords in the name column that you can extract as new columns
# 
# #### Analysis next steps:
# 1. Find the most common brand/model combinations.
# 
# 2. Split the odometer_km into groups, and use aggregation to see if average prices follows any patterns based on the mileage.
# How much cheaper are cars with damage than their non-damaged counterparts?
