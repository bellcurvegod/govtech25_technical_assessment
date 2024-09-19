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

e_id = []
p_url = []
e_title = []
e_start = []
e_end = []
events_r_id = []
events_r_name = []

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

# Fill missing values with NA
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

        # Check if restaurant has events
        events = restaurant_info.get('zomato_events', {})

        # Iterate over events and extract event data
        if isinstance(events, list) and len(events) > 0:
            for event in events:
                event_data = event.get('event', {})
                photos = event.get('photos', [])

                # Extract event details 
                event_id = event_data.get('event_id', 'NA')
                event_title = event_data.get('title', 'NA')
                event_start = event_data.get('start_date', 'NA')
                event_end = event_data.get('end_date', 'NA')

                # Extract photo URL
                if photos:
                    photos_url = photos[0]['photo'].get('url', 'NA')
                else:
                    photos_url = 'NA'

                # Append event details if event occurred in April 2019
                if '2019-04' in event_start or '2019-04' in event_end:
                    e_id.append(event_id)
                    events_r_id.append(res_id)
                    events_r_name.append(r_name)
                    p_url.append(photos_url)
                    e_title.append(event_title)
                    e_start.append(event_start)
                    e_end.append(event_end)

    else:
        # If restaurant data is missing append NA
        r_id.append('NA')
        r_name.append('NA')
        country_code.append('NA')
        user_agg_rating.append('NA')
        city.append('NA')
        user_rating_votes.append('NA')

# Create DataFrame to store restaurant details
details = [r_id, r_name, country_code, city, user_rating_votes, user_agg_rating, cuisines]
restaurant_details = pd.DataFrame(details).T  
restaurant_details.columns = ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'user_rating_votes', 'user_agg_rating', 'cuisines']

# Merge the restaurant details with country data
restaurant_details = pd.merge(restaurant_details, country_df, on='country_code', how='left')
restaurant_details = restaurant_details.drop(columns=['country_code'])

# Write restaurant details to CSV file
restaurant_details.to_csv('restaurant_details.csv', index=False)

# Create DataFrame for event details
events = [e_id, events_r_id, events_r_name, p_url, e_title, e_start, e_end]
events_df = pd.DataFrame(events).T
events_df.columns = ['event_id', 'restaurant_id', 'restaurant_name', 'photo_url', 'event_title', 'event_start_date', 'event_end_date']

# Write event details to CSV file
events_df.to_csv('restaurant_events.csv', index=False)

