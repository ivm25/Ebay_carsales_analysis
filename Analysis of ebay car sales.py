#!/usr/bin/env python
# coding: utf-8

# ### Analysing ebay car sales

# *Business Problem: Cleaning and analysing the cleaned used car listings scraped data for a classifieds section of the German ebay website.*
# 
# *Source of the data: https://data.world/data-society/used-cars-data*
# 
# 

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


autos = pd.read_csv('autos.csv', encoding = 'Windows-1252')


# In[3]:


autos


# In[4]:


autos.info()


# In[5]:


autos.head()


# *Key Observations*
# 
# 1. There are null values for the columns:(vehicleType,gearbox,model,fuelType,notRepairedDamage)
# 
# 2. There are ints and object type columns in our dataset, which might need to be altered, depending upon the analysis.
# 
# 3. The first few rows also show that there are multiple date columns, out of which the first one shows the date of crawling, one shows the last seen timings and a column that shows the creation of listing.
# 
# 4. In addition, there are columns with German and English strings, whih might need to be replaced or combined, depending upon our analysis.
# 
# 5. A few columns are in camelca and a few are in snakecase, which complicates the analysis a little bit.

# In[6]:


autos_copy=autos.columns.copy()


# In[7]:


def clean_column_names(s):
    s=s.replace("yearOfRegistration","registration_year")
    s=s.replace("monthOfRegistration","registration_month")
    s=s.replace("notRepairedDamage","unrepaired_damage")
    s=s.replace("dateCreated","ad_created")
    s=s.lower()
    return s

names = []

for name in autos_copy:
    name = clean_column_names(name)
    names.append(name)
autos.columns = names  


# In[8]:


autos.columns


# **Some of the column names still need to be converted from camelcase to snakecase**

# In[9]:


autos.head()


# **Made changes to column names to more human readable names, which will make the analysis easier as move forward into the project**

# In[10]:


autos.describe(include = 'all')


# **There are a few columns that just have one or two values and are possible candidates for removal later on, for example**:
# 
# 1. Offertype
# 2. Seller
# 
# 
# **Price and Odometer columns are text types and will need exploration later on, as well as the "registration_year" column which is not in the correct date format yet.

# In[11]:


autos["price"] = autos["price"].str.replace("$","")
autos["price"] = autos["price"].str.replace(",","")
autos["odometer"] = autos["odometer"].str.replace("km","")
autos["odometer"] = autos["odometer"].str.replace(",","")
    


# In[12]:


autos.head()


# In[13]:


autos["odometer"] = pd.to_numeric(autos["odometer"])
autos["price"] = pd.to_numeric(autos["price"])


# In[14]:


autos=autos.rename(columns = {"odometer":"odometer_km"})


# In[15]:


autos["price"].unique().shape


# In[16]:


autos["odometer_km"].unique().shape


# In[17]:


autos["price"].describe()


# In[18]:


autos["odometer_km"].describe()


# In[19]:


autos["price"].value_counts(ascending = False).sort_index(ascending = True).head()


# In[20]:


autos["odometer_km"].value_counts(ascending = True).head()


# In[21]:


autos["ad_created"].value_counts(normalize=True, dropna=False).sort_index()


# In[22]:


autos["datecrawled"].value_counts(normalize=True, dropna=False).sort_index()


# In[23]:


autos["lastseen"].value_counts(normalize=True, dropna=False).sort_index()


# **Use this cell to explain the findings from the above data exploration**

# In[24]:


autos["registration_year"].describe()


# **The registration year cannot be 1000 (min value) and also cant be 9999 (max value)**. Therefore, will pick a more reasonable range of years for the analysis. 
# 
# Will count all the listings of cas within 1900 and 2016 and see if that starts to make more sense.

# In[25]:


autos[autos["registration_year"].between(1900,2016)].describe()


# In[26]:


autos = autos[autos["registration_year"].between(1900,2016)]


# In[27]:


autos.describe()


# In[28]:


autos["registration_year"].value_counts(normalize = True)


# **Write a summary of the above steps, as in the removal of outliers and the calculation of value counts for the registration year.**

# In[29]:


count_of_brands = autos["brand"].value_counts(normalize=True)


# *Restricting the above analysis to the top 5% of the brands, would be a reasonable assumption here*

# In[30]:


most_common_brands = count_of_brands[count_of_brands>0.05].index


# In[31]:


most_common_brands


# In[32]:


aggregation_over_brands = {}

for b in most_common_brands:
    new_brands = autos[autos["brand"]==b]
    mean_price = new_brands["price"].mean()
    aggregation_over_brands[b]=int(mean_price)


# In[33]:


aggregation_over_brands


# **Explain your results here**

# In[38]:


mean_mileage_dict = {}

for b in most_common_brands:
    new_brands = autos[autos["brand"]==b]
    mean_mileage = new_brands["odometer_km"].mean()
    mean_mileage_dict[b] = mean_mileage


# In[39]:


mean_mileage_dict


# In[40]:


mean_price_s=pd.Series(aggregation_over_brands)


# In[42]:


print(mean_price_s)
df_price=pd.DataFrame(mean_price_s, columns = ['mean_price'])
df_price


# In[43]:


mean_mileage_s = pd.Series(mean_mileage_dict)
print(mean_mileage_s)


# In[44]:


df_mileage = pd.DataFrame(mean_mileage_s, columns = ['mileage'])
df_mileage

