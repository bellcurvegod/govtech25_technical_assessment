import requests
import pandas as pd

# Initialize empty lists to store the data
r_id = []
r_name = []
country = []
country_code = []
city = []
user_rating_votes = []
user_agg_rating = []
cuisines = []
e_data = []

# Get the JSON data
restaurants_json = requests.get('https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json').json()

# Load the Excel file for country data
country_df = pd.read_excel('Country-Code.xlsx')
country_df.columns = ['country_code', 'country_name']  

# Convert the restaurant data into a DataFrame
restaurants_df = pd.DataFrame(restaurants_json)

# Explode restaurants column to handle lists inside the DataFrame
restaurants_list = restaurants_df['restaurants'].explode()

# Convert the exploded series back into a DataFrame
restaurants_list = pd.DataFrame(restaurants_list)

# Fill missing values with 'NA'
restaurants_list = restaurants_list.fillna('NA')

# Iterate over the rows to append restaurant data to appropriate arrays 
for index, row in restaurants_list.iterrows():
    rest_data = row['restaurants']
    
    # Check if 'restaurants' is a dictionary
    if isinstance(rest_data, dict) and 'restaurant' in rest_data:
        restaurant_info = rest_data['restaurant']
        id_dict = restaurant_info.get('R', {})
        res_id = id_dict.get('res_id', 'NA')
        r_id.append(res_id)

        r_name.append(restaurant_info.get('name', 'NA'))
        cuisines.append(restaurant_info.get('cuisines', 'NA'))
        
        user_rating = restaurant_info.get('user_rating', {})
        user_rating_votes.append(user_rating.get('votes', 'NA'))
        user_agg_rating.append(user_rating.get('aggregate_rating', 'NA'))
        
        location = restaurant_info.get('location', {})
        country_code.append(location.get('country_id', 'NA'))
        city.append(location.get('city', 'NA'))
        
    else:
        # If 'restaurant' data is missing, append 'NA'
        r_id.append('NA')
        r_name.append('NA')
        country_code.append('NA')
        user_agg_rating.append('NA')
        city.append('NA')
        user_rating_votes.append('NA')

# Create DataFrame to store restaurant details
details = [r_id, r_name, country_code, city, user_rating_votes, user_agg_rating, cuisines]
restaurant_details = pd.DataFrame(details).T  
restaurant_details.columns = ['r_id', 'r_name', 'country_code', 'city', 'user_rating_votes', 'user_agg_rating', 'cuisines']

# Merge the restaurant details with country data
restaurant_details = pd.merge(restaurant_details, country_df, on='country_code', how='left')
restaurant_details = restaurant_details.drop(columns=['country_code'])

# Write restaurant details to CSV file
restaurant_details.to_csv('restaurant_details.csv', index=False)