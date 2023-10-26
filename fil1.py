import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium


director = '宁浩'

# Define the base URL for movie search
base_url = f'https://movie.douban.com/subject_search?search_text={director}&cat=1002&start='

# CSV file to store the data
file_name = f'./{director}.csv'

# Function to extract movie data and save it to a CSV file
def download_movies(director, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as out:
        csv_writer = csv.writer(out, dialect='excel')
        flags = set()
        start = 0

        while start < 10000:  # Maximum of 10,000 movies
            request_url = base_url + str(start)
            response = requests.get(request_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            movie_items = soup.find_all('div', class_='item-root')
            for movie_item in movie_items:
                title = movie_item.find('a', class_='title-text').text.strip()
                meta = movie_item.find('div', class_='meta abstract_2').text.strip()
                names = meta.split('/')
                if names[0].strip() == director and title not in flags:
                    flags.add(title)
                    names[0] = title
                    csv_writer.writerow(names)
            
            num_items = len(movie_items)
            if num_items > 1:
                start += 15
            else:
                break

    print('Finished')

# Download and save movie data
download_movies(director, file_name)

# Load the movie dataset
data = pd.read_csv(file_name, encoding='utf-8-sig')

# Data Exploration
print(data.info())
print('-' * 30)
print(data.head())

# Data Preprocessing
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Data Visualization
plt.figure(figsize=(8, 6))
sns.countplot(data['Movie'], label="Movie Count")
plt.title(f'Movies Directed by {director}')
plt.xlabel('Movie')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

# Plotting Frequent Itemsets
fig = px.bar(data['Actor'].value_counts().reset_index(), x='Actor', y='index', orientation='h')
fig.update_layout(title=f'Frequent Actors in Movies Directed by {director}')
fig.show()

# Creating a Map
m = folium.Map(location=[0, 0], zoom_start=1)
folium.Marker(location=[0, 0], tooltip=f'{director} Movies').add_to(m)
m.save(f'{director}_movies_map.html')
