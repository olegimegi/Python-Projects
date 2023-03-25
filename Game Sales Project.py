#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv(r"C:\Users\Olegi Megi\Desktop\Data Analyst\Projects\Game Sales\vgsales.csv")
df.head()


# In[3]:


df.tail()


# In[4]:


df.info()


# In[5]:


df.describe()


# In[6]:


# check for duplicates 
df.duplicated().value_counts()


# In[7]:


# drop year 2017 and 2020
drop_row = df[df["Year"] > 2016].index
df = df.drop(drop_row)


# In[8]:


df.isna().sum()


# In[9]:


df.hist()


# # What  genre has been produced the most

# In[10]:


df["Genre"].value_counts()


# In[11]:


plt.figure(figsize=(15, 10))

sns.countplot(x=df["Genre"], order=df["Genre"].value_counts().index, data=df)

plt.title("Genre by Production", fontsize=18)
plt.xlabel("Genre")
plt.xticks(fontsize=14, rotation=65)
plt.ylabel("")
plt.yticks(fontsize=14)

plt.show()


# # Which Genre has the most Global Sales

# In[12]:


# group data 
df_global_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
df_global_sales = df_global_sales.reset_index()
print(df_global_sales)

fig = plt.figure(figsize=(10,5))

# create plot
plot = sns.barplot(x=df_global_sales["Genre"], y=df_global_sales["Global_Sales"], data=df_global_sales, color="grey")

#customize plot
plt.title("Genre by Global Sales")
plt.xticks(rotation=65)

# make the top three games blue
for i in range(3):
    plot.patches[i].set_facecolor("blue")

# show the plot    
plt.show


# # Which year had the most releases?

# In[13]:


df["Year"].value_counts()


# In[14]:


fig = plt.figure(figsize=(10,5))

sns.countplot(x=df["Year"], order=df["Year"].value_counts().index, data=df)

plt.title("Years by Releases")
plt.ylabel("Realeses")
plt.xlabel("")
plt.xticks(rotation=65)


# In[15]:


fig = plt.figure(figsize=(16,8))

style = "fivethirtyeight"

with plt.style.context(style):
    sns.countplot(x="Year", hue="Genre", order=df.Year.value_counts().iloc[:5].index, data=df)

plt.title("Games releaesed in the top 5 years", fontsize=16)
plt.ylabel("")
plt.xlabel("")
plt.xticks(fontsize=14)

plt.show()


# # Which Year has the most Global Sales

# In[16]:


df_global_sales_by_year = df.groupby("Year")["Global_Sales"].sum().sort_values(ascending=False)
df_global_sales_by_year = df_global_sales_by_year.reset_index()
print(df_global_sales_by_year)


# In[17]:


fig = plt.figure(figsize=(16,8))

sns.barplot(x=df_global_sales_by_year.Year, y=df_global_sales_by_year.Global_Sales, data=df_global_sales_by_year)

plt.xticks(fontsize=12, rotation=90)


# # Which genre game has the most global sales by year?

# In[18]:


year_genre_sales = df.groupby(['Year', 'Genre'])['Global_Sales'].sum()

# find the index of the maximum sales for each year
idx = year_genre_sales.groupby(level=0).idxmax()

# extract the rows with the maximum sales for each year
year_genre_sales_max = year_genre_sales.loc[idx]

# reset the index to turn the multi-index into columns
year_genre_sales_max = year_genre_sales_max.reset_index()

# print the result
print(year_genre_sales_max)


# In[19]:


fig = plt.figure(figsize=(16,8))

plot = sns.barplot(x=year_genre_sales_max.Year, y=year_genre_sales_max.Global_Sales, data=year_genre_sales_max)

index=0
genre=year_genre_sales_max["Genre"]

for value in year_genre_sales_max["Global_Sales"]:
    plot.text(index, value + 1, str(genre[index] + " = " + str(round(value, 2))), color="black", fontsize=14,
             rotation=90, ha="center")
    index +=1

plt.xticks(fontsize=14, rotation=90)


# # Which game has the most releases in a year?

# In[20]:


# group the data by year and genre and count the number of games in each group
year_genre_count = df.groupby(['Year', 'Genre']).size().reset_index(name='count')


year_max_genre = year_genre_count.groupby(['Year', 'Genre'])['count'].sum().reset_index()

# extract the rows with the maximum sales for each year
idx = year_max_genre.groupby('Year')['count'].transform(max) == year_max_genre['count']

# reset the index and remove duplicates to turn the multi-index into columns
year_max_genre = year_max_genre[idx].drop_duplicates(subset=["Year"]).reset_index(drop=True)

print(year_max_genre)


# In[21]:


fig = plt.figure(figsize=(16,8))

plot = sns.barplot(x=year_max_genre["Year"], y=year_max_genre["count"], data=year_max_genre)

index = 0
genre = year_max_genre["Genre"]


for value in year_max_genre['count'].values:
    plot.text(index, value + 2, str(genre[index] + " == " +str(value)), 
              color='#000', size=14, rotation= 90, ha="center") 
    index+=1
    
plt.xticks(fontsize=14, rotation=90)


# # Which Platform has the highest sales 

# In[22]:


sales_by_platform = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False)
sales_by_platform = sales_by_platform.reset_index()
print(sales_by_platform)

fig = plt.figure(figsize=(10,5))

sns.barplot(x=sales_by_platform.Platform, y=sales_by_platform.Global_Sales, data=sales_by_platform)

plt.title("Global Sales by Platform", fontsize=16)
plt.xticks(rotation=90, fontsize=14)
plt.grid(axis="y")


# # Which game has the greatest Global Sales

# In[23]:


sales_by_game = df.groupby("Name")["Global_Sales"].sum().sort_values(ascending=False).head(20)
sales_by_game = sales_by_game.reset_index()
print(sales_by_game)


# In[24]:


fig = plt.figure(figsize=(16,9))

sns.barplot(x=sales_by_game.Name, y=sales_by_game.Global_Sales, data=sales_by_game)

plt.xticks(rotation=90, fontsize=14)


# # Sales comparison by genre

# In[25]:


# grouping the sales by genre
sales_by_genre = df.groupby("Genre")[["Global_Sales", "EU_Sales","JP_Sales", "NA_Sales", "Other_Sales"]].sum()
print(sales_by_genre)


# In[26]:


fig = plt.figure(figsize=(16,8))

sns.heatmap(data=sales_by_genre, annot=True, fmt=".2f")

plt.title("Video Game Sales by Genre", fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)


# # Which Publisher have the most releases

# In[27]:


df["Publisher"].value_counts().head(20)


# In[28]:


fig = plt.figure(figsize=(16,8))

sns.countplot(x=df["Publisher"], order=df["Publisher"].value_counts().head(20).index, data=df)

plt.title("Releases by Publisher")
plt.xlabel("")
plt.xticks(rotation=90, fontsize=14)
plt.ylabel("")
plt.yticks(fontsize=14)

plt.show()


# # Global Sales by Publisher

# In[29]:


sales_by_publisher = df.groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False).head(20)
sales_by_publisher = sales_by_publisher.reset_index()
print(sales_by_publisher)


# In[30]:


fig = plt.figure(figsize=(16,8))

sns.barplot(x="Publisher", y="Global_Sales", data=sales_by_publisher)

plt.title("Global Sales by Publisher", fontsize=18, y=1.05) # adjust the hightof the titel  with y 
plt.xlabel("")
plt.xticks(rotation=90, fontsize=14)
plt.ylabel("")
plt.yticks(fontsize=14)


# # Most Releases per year by Publisher

# In[31]:


publisher_release_year = df.groupby(["Publisher", "Year"]).size().reset_index(name="count").sort_values(by="count", ascending=False)
publisher_release_year = publisher_release_year.reset_index()
print(publisher_release_year)


# In[39]:


# get the max value of each year
publisher_release_year = publisher_release_year.loc[publisher_release_year.groupby("Year")["count"].idxmax()]

# drop duplicates baesd on year
publisher_release_year = publisher_release_year.drop_duplicates(subset=["Year"], keep="last")
publisher_release_year  = publisher_release_year.reset_index()
print(publisher_release_year)


# In[45]:


publisher_release_year = publisher_release_year.drop(["level_0", "index"], axis=1)


# In[46]:


print(publisher_release_year)


# In[52]:


fig = plt.figure(figsize=(16,8))

plot = sns.barplot(x="Year", y="count", data=publisher_release_year)

index = 0 
publisher = publisher_release_year["Publisher"]

for value in publisher_release_year['count'].values:
    plot.text(index, value + 2, str(publisher[index] + " -- " +str(value)), 
              color='black', size=14, rotation= 90, ha="center") 
    index+=1

    

plt.title("Most releases by Publisher each year")
plt.xticks(rotation=90, fontsize=14)
plt.ylabel("")
plt.yticks(fontsize=14)


# In[ ]:




