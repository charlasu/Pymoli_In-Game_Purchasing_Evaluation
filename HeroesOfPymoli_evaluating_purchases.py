
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[158]:


# Dependencies and Setup
import pandas as pd
import numpy as np
import random

# Raw data file
raw_data = "Resources/purchase_data.csv"

# Read csv file and store into pandas data frame
game_purchases_df = pd.read_csv(raw_data, encoding="utf-8")

col_name =game_purchases_df.columns[1]
game_purchases_df=game_purchases_df.rename(columns = {col_name:"Players"})

#View dataframe
game_purchases_df.head()


# ## Player Count

# * Display the total number of players
# 

# In[159]:


#Calculate the number of unique players
unique_players = len(game_purchases_df["Players"].unique())

#Rename "Players" column
player_table = pd.DataFrame({"Total Unique Players": [unique_players]})

#View dataframe
player_table


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# * Create a summary data frame to hold the results
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display the summary data frame
# 

# In[160]:


#Use basic calculations for each element
purchased_items = len(game_purchases_df["Item Name"].unique())
average_price = game_purchases_df["Price"].mean()
total_purchases = game_purchases_df["Item Name"].count()
total_revenue = game_purchases_df["Price"].sum()

#Put elements into a dataframe
purchasing_table = pd.DataFrame({"Total Unique Items": [purchased_items],
                              "Avg. Purchase Price": [average_price],
                              "Total Purchases": [total_purchases],
                              "Total Revenue": [total_revenue]})

# Make the data pretty
purchasing_table["Avg. Purchase Price"] = purchasing_table["Avg. Purchase Price"].map("${:,.2f}".format)
purchasing_table["Total Revenue"] = purchasing_table["Total Revenue"].map("${:,.2f}".format)
purchasing_table = purchasing_table.loc[:, ["Total Unique Items", "Avg. Purchase Price", "Total Purchases", "Total Revenue"]]

#View dataframe
purchasing_table


# ## Gender Demographics

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# * Create a summary data frame to hold the results
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display the summary data frame

# In[171]:


#Create a groupby to break out info by gender
gender_groupby = game_purchases_df.groupby("Gender")

#Calculate the total number of players and the percentage of players by gender
gender_playercount = gender_groupby["Gender"].count()

total_gender = gender_playercount["Female"] + gender_playercount["Male"] + gender_playercount["Other / Non-Disclosed"] 

gender_percentage = round(gender_playercount / total_gender * 100, 2)
  
#Put elements into a dataframe
gender_table = pd.DataFrame({"# of Players": gender_playercount,
                             "% of Players": gender_percentage})

# Make the data pretty
gender_table["% of Players"] = gender_table["% of Players"].map("{:,.2f}%".format)

#View dataframe
gender_table.reset_index()


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, etc. by gender
# 
# * Create a summary data frame to hold the results
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display the summary data frame

# In[162]:


#Calculate elements by gender
#_p_ stands for "purchases"
gender_p_count = game_purchases_df.groupby(["Gender"]).count()["Price"].rename("# of Purchases")
gender_p_avg = game_purchases_df.groupby(["Gender"]).mean()["Price"].rename("Avg. Purchase Price")
gender_p_total = game_purchases_df.groupby(["Gender"]).sum()["Price"].rename("Total Purchases")


# Convert groupby elements into a DataFrame
gender_p_analysis = pd.DataFrame({"# of Purchases": gender_p_count, "Avg. Purchase Price": gender_p_avg, "Total Purchases": gender_p_total})

# Make the data pretty
gender_p_analysis["# of Purchase Count"] = gender_p_analysis["# of Purchases"].map("{:,}".format)
gender_p_analysis["Avg. Purchase Price"] = gender_p_analysis["Avg. Purchase Price"].map("${:,.2f}".format)
gender_p_analysis["Total Purchases"] = gender_p_analysis["Total Purchases"].map("${:,.2f}".format)
#gender_p_analysis["Total (Normalized)"] = gender_p_analysis["Total (Normalized)"].map("${:,.2f}".format)
gender_p_analysis = gender_p_analysis.loc[:, ["# of Purchases", "Avg. Purchase Price", "Total Purchases"]]

#View dataframe
gender_p_analysis


# ## Age Demographics

# * Establish bins for ages
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# * Calculate the numbers and percentages by age group
# 
# * Create a summary data frame to hold the results
# 
# * Optional: round the percentage column to two decimal points
# 
# * Display Age Demographics Table
# 

# In[163]:


# Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_labels = ["<10", "10–14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]


# In[164]:


#Add the binned data as a new column in the dataframe
game_purchases_df["Player Ages"] = pd.cut(game_purchases_df["Age"], age_bins, labels=group_labels)

print(game_purchases_df.head(2))


# In[165]:


#Create a groupby to break out info by age
age_groupby = game_purchases_df.groupby("Player Ages")

#Calculate the total number of players and the percentage of players by age
age_playercount = age_groupby["Player Ages"].count()

total_ages = age_playercount["<10"] + age_playercount["10–14"] + age_playercount["15-19"] + age_playercount["20-24"] + age_playercount["25-29"] + age_playercount["30-34"] + age_playercount["35-39"] + age_playercount["40+"] 

age_percentage_all = round(age_playercount / total_ages * 100, 2)

#Calculate the percentage of unique players
unique_players = len(game_purchases_df["Players"].unique())

age_percentage_unique = round(age_playercount / unique_players * 100, 2)

  
#Put elements into a dataframe
age_table = pd.DataFrame({"# of Players": age_playercount, 
                          "Total Players (all SNs)": age_percentage_all,
                         "Total Players (unique)": age_percentage_unique})

# Make the data pretty
age_table["Total Players (all SNs)"] = age_table["Total Players (all SNs)"].map("{:,.2f}%".format)
age_table["Total Players (unique)"] = age_table["Total Players (unique)"].map("{:,.2f}%".format)

#View dataframe
age_table.reset_index()

#DEAR READER: The Total Players (all SNs) shows age percentages that align to full count of the Num. of Players columnn; 
#however, the Total Players (unique) shows the age percentages that align to the total player count listed at the top of the notebook.


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, etc. in the table below
# 
# * Create a summary data frame to hold the results
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display the summary data frame

# In[166]:


#Create a groupby to break out info by age
age_groupby = game_purchases_df.groupby("Player Ages")


#Calculate elements by age
#_p_ stands for "purchases"
age_p_count = game_purchases_df.groupby(["Player Ages"]).count()["Price"].rename("# of Purchases")
age_p_avg = game_purchases_df.groupby(["Player Ages"]).mean()["Price"].rename("Avg. Purchase Price")
age_p_total = game_purchases_df.groupby(["Player Ages"]).sum()["Price"].rename("Total Purchases")


# Convert groupby elements into a DataFrame
age_p_analysis = pd.DataFrame({"# of Purchases": age_p_count, "Avg. Purchase Price": age_p_avg, "Total Purchases": age_p_total})

# Make the data pretty
age_p_analysis["# of Purchases Count"] = age_p_analysis["# of Purchases"].map("{:,}".format)
age_p_analysis["Avg. Purchase Price"] = age_p_analysis["Avg. Purchase Price"].map("${:,.2f}".format)
age_p_analysis["Total Purchases"] = age_p_analysis["Total Purchases"].map("${:,.2f}".format)
#age_p_analysis["Normalized Totals"] = age_p_analysis["Normalized Totals"].map("${:,.2f}".format)
age_p_analysis = age_p_analysis.loc[:, ["# of Purchases", "Avg. Purchase Price", "Total Purchases"]]

#View dataframe
age_p_analysis


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# * Create a summary data frame to hold the results
# 
# * Sort the total purchase value column in descending order
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display a preview of the summary data frame
# 
# 

# In[167]:


#Create a groupby to break out info by those players who spend the most money
BigSpenders_p_groupby = game_purchases_df.groupby(["Players"])

#Calculate elements by top spenders (SN is the column name)
#_p_ stands for "purchases"
BigSpenders_p_count = BigSpenders_p_groupby["Item ID"].count()
BigSpenders_p_avg = BigSpenders_p_groupby["Price"].mean()
BigSpenders_p_total = BigSpenders_p_groupby["Price"].sum()

# Convert groupby elements into a DataFrame
BigSpenders_p_analysis = pd.DataFrame({"# of Purchases": BigSpenders_p_count,
                         "Avg. Purchase Price": BigSpenders_p_avg,
                         "Total Purchases": BigSpenders_p_total})

#Sort by Total Purchases
BigSpenders_p_analysis = BigSpenders_p_analysis.sort_values("Total Purchases", ascending=False) 

# Make the data pretty
BigSpenders_p_analysis["Avg. Purchase Price"] = BigSpenders_p_analysis["Avg. Purchase Price"].map("${:.2f}".format)
BigSpenders_p_analysis["Total Purchases"] = BigSpenders_p_analysis["Total Purchases"].map("${:.2f}".format)
BigSpenders_p_analysis = BigSpenders_p_analysis[["# of Purchases", "Avg. Purchase Price", "Total Purchases"]]

#View dataframe
BigSpenders_p_analysis.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# * Create a summary data frame to hold the results
# 
# * Sort the purchase count column in descending order
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display a preview of the summary data frame
# 

# In[168]:


#Create a dataframe of Item ID, Item Name, and Item Price
popular_df = game_purchases_df[["Item ID", "Item Name", "Price"]]
popular_df.head()


# In[169]:


#Create a groupby to break out info by most popular items purchased
most_pop_p_groupby = game_purchases_df.groupby(["Item ID"])

#Calculate items
#_p_ stands for "purchases"
item_ID = most_pop_p_groupby["Item ID"].unique().str[0]
item_name = most_pop_p_groupby["Item Name"].unique().str[0]
pop_p_count = most_pop_p_groupby["Item ID"].count()
item_price = most_pop_p_groupby["Price"].unique().str[0]
revenue_total = most_pop_p_groupby["Price"].sum()


# Convert groupby elements into a new DataFrame
most_pop_p_analysis = pd.DataFrame({"Item ID": item_ID,
                                "Item Name": item_name,
                                "# of Purchases": pop_p_count, 
                                "Item Price": item_price,
                               "Total Purchase Value": revenue_total})

# Make the data pretty
#most_pop_p_analysis["Item Price"] = most_pop_p_analysis["Item Price].map("${:.2f}.format)—THIS CAUSES ERROR, BUT I CAN'T SEE DIFFERENCE
most_pop_p_analysis["Item Price"] = most_pop_p_analysis["Item Price"].map("${:.2f}".format)
most_pop_p_analysis["Total Purchase Value"] = most_pop_p_analysis["Total Purchase Value"].map("${:.2f}".format)


#View dataframe and sort data frame from highest value down
most_pop_p_analysis.sort_values("# of Purchases", ascending=False).head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# * Optional: give the displayed data cleaner formatting
# 
# * Display a preview of the data frame
# 

# In[170]:


#Create new dataframe and sort on multiple columns
most_profit_p_analysis = most_pop_p_analysis.sort_values(["# of Purchases","Total Purchase Value"], ascending=False)

#View dataframe
most_profit_p_analysis.head()

