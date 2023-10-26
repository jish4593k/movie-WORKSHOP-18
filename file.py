import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import plotly.express as px
import folium

# Set the director's name
director = '宁浩'

# Load the movie dataset
file_name = f'./{director}.csv'
data = pd.read_csv(file_name, encoding='utf-8-sig')

# Data Exploration
print(data.info())
print('-' * 30)
print(data.head())

# Data Preprocessing
# Remove leading and trailing spaces in actor names
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Data Visualization
plt.figure(figsize=(8, 6))
sns.countplot(data['Movie'], label="Movie Count")
plt.title(f'Movies Directed by {director}')
plt.xlabel('Movie')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

# Frequent Itemset Mining
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = data.groupby(['Movie', 'Actor'])['Actor'].count().unstack().fillna(0).applymap(encode_units)

frequent_itemsets = apriori(basket_sets, min_support=0.1, use_colnames=True)
print('Frequent Itemsets:')
print(frequent_itemsets)

# Association Rule Mining
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
print('Association Rules:')
print(rules)

# Plotting Frequent Itemsets
fig = px.bar(frequent_itemsets, x='support', y='itemsets')
fig.update_layout(title=f'Frequent Itemsets for Movies Directed by {director}')
fig.show()

# Creating a Map
m = folium.Map(location=[0, 0], zoom_start=1)
folium.Marker(location=[0, 0], tooltip=f'{director} Movies').add_to(m)
m.save(f'{director}_movies_map.html')
