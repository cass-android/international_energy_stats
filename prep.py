import pandas as pd
from numpy import inf
import re

# IMPORT DATA 
# Detailed energy dataset - includes TJ conversions and Flow Categories:
df = pd.read_csv('~/code/intenergy/all_energy_statistics_2019_V2.csv')

# Population totals
pop = pd.read_csv('~/code/intenergy/population.csv', header = 4).drop(
    columns=['Country Code','Indicator Name','Indicator Code']
)
pop = pd.DataFrame(pop.set_index('Country Name').unstack())
pop = pop.reset_index()
pop['Year'] = pop['level_0'].fillna(0).astype(int)
pop['Population'] = pop[0].fillna(0).astype(int)
pop = pop.drop(columns=['level_0',0])
pop = pop.rename({'Country Name': 'Country or Area'}, axis=1)

# GDP totals
gdp = pd.read_csv('~/code/intenergy/gdp_usd.csv', header = 4).drop(
    columns=['Country Code','Indicator Name','Indicator Code']
)
gdp = pd.DataFrame(gdp.set_index('Country Name').unstack())
gdp = gdp.reset_index()
gdp['Year'] = gdp['level_0'].fillna(0).astype(int)
gdp['GDP_USD'] = gdp[0].fillna(0).astype(int)
gdp = gdp.drop(columns=['level_0',0])
gdp = gdp.rename({'Country Name': 'Country or Area'}, axis=1)

# SUMMARY TABLES:
# totals final consumption
totals_con = pd.DataFrame(
    df[
        (df['Flow_Category']=='Final consumption')
        ].groupby(by=['Country or Area', 'Year'])['Quantity_TJ'].sum()
        )
totals_con = totals_con.reset_index(level=['Country or Area', 'Year'])

# totals imports
totals_imp = pd.DataFrame(
    df[
        (df['Flow_Category']=='Imports')
        ].groupby(by=['Country or Area', 'Year'])['Quantity_TJ'].sum()
        )
totals_imp = totals_imp.reset_index(level=['Country or Area', 'Year'])

# totals exports
totals_exp = pd.DataFrame(
    df[
        (df['Flow_Category']=='Exports')
        ].groupby(by=['Country or Area', 'Year'])['Quantity_TJ'].sum()
        )
totals_exp = totals_exp.reset_index(level=['Country or Area', 'Year'])

# MERGED TABLES:
totals_con = totals_con.merge(
                  pop, 
                  how='left', 
                  on=['Year','Country or Area'], 
)

totals_con = totals_con.merge(
                  gdp, 
                  how='left', 
                  on=['Year','Country or Area'], 
)
totals_imp = totals_imp.merge(
                  pop, 
                  how='left', 
                  on=['Year','Country or Area'], 
)

totals_imp = totals_imp.merge(
                  gdp, 
                  how='left', 
                  on=['Year','Country or Area'], 
)
totals_exp = totals_exp.merge(
                  pop, 
                  how='left', 
                  on=['Year','Country or Area'], 
)

totals_exp = totals_exp.merge(
                  gdp, 
                  how='left', 
                  on=['Year','Country or Area'], 
)

# Add columns for TJ/capita, TJ/GDP
totals_con['TJ_per_capita'] = totals_con['Quantity_TJ'] / totals_con['Population']
totals_con['TJ_per_USD_GDP'] = totals_con['Quantity_TJ'] / totals_con['GDP_USD']
totals_con['TJ_per_capita'] = totals_con['TJ_per_capita'].replace(to_replace= inf, value=0)
totals_con['TJ_per_USD_GDP'] = totals_con['TJ_per_USD_GDP'].replace(to_replace= inf, value=0)

totals_imp['TJ_per_capita'] = totals_imp['Quantity_TJ'] / totals_imp['Population']
totals_imp['TJ_per_USD_GDP'] = totals_imp['Quantity_TJ'] / totals_imp['GDP_USD']
totals_imp['TJ_per_capita'] = totals_imp['TJ_per_capita'].replace(to_replace= inf, value=0)
totals_imp['TJ_per_USD_GDP'] = totals_imp['TJ_per_USD_GDP'].replace(to_replace= inf, value=0)

totals_exp['TJ_per_capita'] = totals_exp['Quantity_TJ'] / totals_exp['Population']
totals_exp['TJ_per_USD_GDP'] = totals_exp['Quantity_TJ'] / totals_exp['GDP_USD']
totals_exp['TJ_per_capita'] = totals_exp['TJ_per_capita'].replace(to_replace= inf, value=0)
totals_exp['TJ_per_USD_GDP'] = totals_exp['TJ_per_USD_GDP'].replace(to_replace= inf, value=0)

