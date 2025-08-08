import requests
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
from IPython.display import display, clear_output

# -----------------
# CONFIG
# -----------------
API_KEY = '5e1c6b888af8a8ba38566511c032baa4'
EXCEL_FILE = r"C:\Users\Hp\Desktop\Honours\air_quality_data.xlsx"
SAVE_DIR = r"C:\Users\Hp\Desktop\Honours\Air_Quality_ML"

cities = {
    'Mumbai': (19.0760, 72.8777),
    'Delhi': (28.7041, 77.1025),
    'Bengaluru': (12.9716, 77.5946),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639)
}

aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
aqi_colors = {1: "green", 2: "skyblue", 3: "yellow", 4: "orange", 5: "red"}

# -----------------
# FETCH AQI
# -----------------
def fetch_aqi(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()["list"][0]["main"]["aqi"]
        except KeyError:
            return None
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# -----------------
# MAIN ONE-TIME FETCH
# -----------------
timestamp = datetime.datetime.now()
data = []

for city, coords in cities.items():
    aqi = fetch_aqi(*coords)
    if aqi is not None:
        if aqi >= 4:
            print(f"⚠️ ALERT: {city} has {aqi_levels[aqi]} air quality!")
        data.append({
            'Timestamp': timestamp,
            'City': city,
            'AQI Level': aqi,
            'Category': aqi_levels[aqi]
        })

df_new = pd.DataFrame(data)

# Append to file
try:
    old_df = pd.read_excel(EXCEL_FILE)
    df_all = pd.concat([old_df, df_new], ignore_index=True)
except FileNotFoundError:
    df_all = df_new

df_all.to_excel(EXCEL_FILE, index=False)

clear_output(wait=True)
print(f"Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
display(df_new)

# -----------------
# LIVE BAR CHART
# -----------------
plt.figure(figsize=(8, 5))
plt.bar(df_new['City'], df_new['AQI Level'],
        color=[aqi_colors[x] for x in df_new['AQI Level']])
plt.title(f'Live AQI Levels - {timestamp.strftime("%Y-%m-%d %H:%M:%S")}')
plt.xlabel('Cities')
plt.ylabel('AQI Level (1=Good to 5=Very Poor)')
plt.ylim(0, 6)
plt.grid(axis='y')
for i, (city, level, cat) in enumerate(zip(df_new['City'], df_new['AQI Level'], df_new['Category'])):
    plt.text(i, level + 0.1, cat, ha='center')
plt.show()

# -----------------
# TREND CHART
# -----------------
plt.figure(figsize=(10, 6))
for city in cities:
    city_data = df_all[df_all['City'] == city]
    if not city_data.empty:
        plt.plot(city_data['Timestamp'], city_data['AQI Level'], label=city, marker='o')
plt.title('AQI Trend Analysis Over Time')
plt.xlabel('Timestamp')
plt.ylabel('AQI Level')
plt.ylim(0, 6)
plt.grid(True)
plt.legend()
plt.show()

# -----------------
# HISTOGRAM
# -----------------
plt.figure(figsize=(8, 5))
plt.hist(df_all['AQI Level'], bins=[0.5,1.5,2.5,3.5,4.5,5.5],
         edgecolor='black', rwidth=0.8, color='lightblue')
plt.xticks([1, 2, 3, 4, 5], list(aqi_levels.values()))
plt.title('Distribution of AQI Levels')
plt.xlabel('AQI Category')
plt.ylabel('Frequency')
plt.grid(axis='y')
plt.show()

# -----------------
# PIE CHART
# -----------------
category_counts = df_all['Category'].value_counts().sort_index()
plt.figure(figsize=(6, 6))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Proportion of AQI Categories')
plt.show()
