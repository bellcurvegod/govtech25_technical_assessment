import requests
import pandas as pd

restaurants_json = requests.get('https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json')
country_df = pd.read_excel('Country-Code.xlsx')

print(country_df)