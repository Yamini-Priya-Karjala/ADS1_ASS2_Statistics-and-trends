# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:56:07 2023

@author: yaminiperi
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:45:44 2023

@author: yaminiperi
"""

# Import necessary libraries
import wbdata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define a function to fetch and clean data
def fetch_clean_data():
    """
    Retrieves climate change-related data from the World Bank API, cleans it up, and saves it to a CSV file.
    
    Returns:
        A Pandas dataframe containing the cleaned-up data.
    """
    # Define the indicator codes for the data we want to retrieve
    indicators = {
        'EN.ATM.CO2E.KT': 'CO2 emissions (kt)',
        'EG.USE.ELEC.KH.PC': 'Electric power consumption (kWh per capita)',
        'NY.GDP.MKTP.CD': 'GDP (current US$)',
        'SP.POP.GROW': 'Population growth (annual %)'
    }

    # Retrieve the data from the World Bank API
    data = wbdata.get_dataframe(indicators, convert_date=True)

    # Clean up the dataframe
    data = data.reset_index()
    data = data.rename(columns={'country': 'Country', 'date': 'Year'})
    
    #Transpose the data
    data_T = data.transpose()

    # Save the data to a CSV file
    data.to_csv(filename, index=False)

    return data,data_T

# Define the filename for the CSV file
filename = 'worldbank_climate_change_data.csv'

# Retrieve and clean the data
data = fetch_clean_data()

# Load data from CSV file
df = pd.read_csv(filename)

# Select only 11 countries
countries = ['United States', 'Turkiye', 'China', 'India', 'Russia', 'United Kingdom', 'Bangladesh', 'Germany', 'Austria', 'Saudi Arabia', 'Canada']
df = df[df['Country'].isin(countries)]

# Define list of indicators to be used in correlation analysis
indicators=['Year', 'CO2 emissions (kt)', 'Electric power consumption (kWh per capita)', 'GDP (current US$)', 'Population growth (annual %)']

# Convert the Year column to a datetime format
df['Year'] = pd.to_datetime(df['Year'])

# Create a line plot of GDP over time for all countries
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x='Year', y='GDP (current US$)', hue='Country')

# Set the x-axis label and title
plt.xlabel('Year')
plt.title('GDP over Time')

# Show the plot
plt.show()

# Group the data by country and year, and compute the mean of the CO2 emissions for each group
grouped = df.groupby(['Country', pd.Grouper(key='Year', freq='1Y')])['CO2 emissions (kt)'].mean().reset_index()

# Resample the data to 10-year intervals and compute the mean for each interval
grouped = grouped.set_index('Year').groupby('Country').resample('10Y').mean().reset_index()

# Create a bar plot of CO2 emissions by country for 10-year intervals
plt.figure(figsize=(10,6))
sns.barplot(data=grouped, x='Country', y='CO2 emissions (kt)', hue='Year')

# Set the plot title and axis labels
plt.title('CO2 Emissions by Country for 10-years average (kt)')
plt.xlabel('Country')
plt.ylabel('CO2 Emissions (kt)')

# Get the current legend
handles, labels = plt.gca().get_legend_handles_labels()

# Create a new legend with only the year component of each label
new_labels = [label.split('T')[0] for label in labels]

# Update the legend
plt.legend(handles, new_labels)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.show()

#Sort the data by CO2 emissions and print summary statistics
print('CO2 Emissions (kt):')
print(df.sort_values(by='CO2 emissions (kt)', ascending=False))
print()


# Plot data for all countries
df_countries = df[::-1]

"""
#Create a new figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(20,12))

#Plot population growth on the first subplot
axs[0].plot(df_countries['Year'], df_countries['Population growth (annual %)'])
axs[0].set_title('Population growth')
axs[0].set_ylabel('Population growth (annual %)')

#Plot electric power consumption on the second subplot
axs[1].plot(df_countries['Year'], df_countries['Electric power consumption (kWh per capita)'])
axs[1].set_title('Electric power consumption')
axs[1].set_ylabel('Electric power consumption (kWh per capita)')

# Set the x-axis label
plt.xlabel('Year')

# Add country labels to the legend
plt.legend(df_countries['Country'], loc='upper left')

# Show the plot
plt.show()

"""



#Create a scatter plot of CO2 emissions versus electric power consumption for all countries
plt.scatter(df_countries['Electric power consumption (kWh per capita)'], df_countries['Population growth (annual %)'], c=df_countries['GDP (current US$)'], cmap='coolwarm', alpha=0.8, label='Countries')
plt.xlabel('Electric power consumption (kWh per capita)')
plt.ylabel('Population growth (annual %)')
plt.legend()
plt.show()


#Select only the data for India
df_India = df[df['Country'] == 'India']
df_india_subset = df_India[['CO2 emissions (kt)', 'Electric power consumption (kWh per capita)']]
correlation_matrix = df_india_subset.corr()

#Print the correlation matrix
print(correlation_matrix)

# Calculate and display correlation coefficients for India
corr_matrix = df_India.corr()
sns.heatmap(corr_matrix, cmap='YlGnBu', annot=True)
plt.title('India')
plt.show()



# Print summary statistics
print(df.describe())

# Print information about the DataFrame
print(df.info())

# calculate and print the correlation matrix for all the indicators:
corr_matrix = df[indicators].corr()
print(corr_matrix)

#Calculate and print the correlation coefficients between CO2 emissions and electric power consumption for each country
corr_by_country = df.groupby('Country')[['CO2 emissions (kt)', 'Electric power consumption (kWh per capita)']].corr().iloc[0::2,-1]
print(corr_by_country)

#Calculate the correlation coefficients between all the indicators for each country and create a heatmap to visualize them
corr_by_country = df.groupby('Country')[indicators].corr()
sns.heatmap(df[indicators].corr(), annot=True, cmap='coolwarm')
plt.title("All Countries")

#show the plot
plt.show()