# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:40:31 2023

@author: yaminiperi
"""


import wbdata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_clean_data(filename):
    

    # Define the indicator codes for the data we want to fetch
    indicators = {
        'EN.ATM.CO2E.KT': 'CO2 emissions (kt)',
        'EG.USE.ELEC.KH.PC': 'Electric power consumption (kWh per capita)',
        'NY.GDP.MKTP.CD': 'GDP (current US$)',
        'SP.POP.GROW': 'Population growth (annual %)'
    }

    # fetch the data from the World Bank API
    data = wbdata.get_dataframe(indicators, convert_date=True)

    # Clean up the dataframe
    data = data.reset_index()
    data = data.rename(columns={'country': 'Countries', 'date': 'Year'})
    

    # Save the data to a CSV file
    data.to_csv(filename, index=False)

    return data

# Specify the name of the CSV file to save the data to
filename = 'worldbank_climate_change_data.csv'


# fetch and clean the data
data = fetch_clean_data(filename)

# Load data from CSV file
df = pd.read_csv(filename)


countries = ['United States', 'China', 'India', 'Russia', 'United Kingdom']
df = df[df['Countries'].isin(countries)]

# Define list of indicators to be used in correlation analysis
indicators=['Year', 'CO2 emissions (kt)', 'Electric power consumption (kWh per capita)', 'GDP (current US$)']

# Sort by CO2 emissions and print summary statistics
print('CO2 Emissions (kt):')
print(df.sort_values(by='CO2 emissions (kt)', ascending=False))
print()

# Plot data for China
df_china = df[df['Countries'] == 'China'][::-1]

fig, axs = plt.subplots(3, 1, figsize=(30, 40))
axs[0].plot(df_china['Year'], df_china['CO2 emissions (kt)'])
axs[0].set_title('CO2 emissions')
axs[1].plot(df_china['Year'], df_china['Electric power consumption (kWh per capita)'])
axs[1].set_title('Electric power consumption')
axs[2].plot(df_china['Year'], df_china['GDP (current US$)'])
axs[2].set_title('GDP')
plt.show()

plt.scatter(df_china['GDP (current US$)'], df_china['CO2 emissions (kt)'])
plt.xlabel('GDP')
plt.ylabel('CO2 emissions')
plt.title('CO2 emissions vs GDP')
plt.show()


# Calculate and display correlation coefficients for each country
corr_matrix = df_china.corr()
sns.heatmap(df[indicators].corr(), annot=True, cmap='coolwarm')


df['Year']

# Convert the Year column to a datetime format
df['Year'] = pd.to_datetime(df['Year'])


# Group the data by country and year, and compute the mean of the CO2 emissions for each group
grouped = df.groupby(['Countries', pd.Grouper(key='Year', freq='1Y')])['CO2 emissions (kt)'].mean().reset_index()


# Resample the data to 5-year intervals and compute the mean for each interval
grouped = grouped.set_index('Year').groupby('Countries').resample('5Y').mean().reset_index()

# Create a new figure with the desired size
plt.figure(figsize=(10,6))

# Use Seaborn's barplot function to create the bar plot
sns.barplot(data=grouped, x='Countries', y='CO2 emissions (kt)', hue='Year')

# Set the plot title and axis labels
plt.title('5-Year Average of CO2 Emissions by Country')
plt.xlabel('Year')
plt.ylabel('CO2 Emissions (kt)')

# Plot data for 
df_united_states = df[df['Countries']=='United States']

df['Countries']

plt.figure(figsize=(10,6))

sns.lineplot(data=df, x='Year', y='GDP (current US$)', hue='Countries')

# Set the x-axis label and title
plt.xlabel('Year')
plt.title('GDP over Time')

# Show the plot
plt.show()