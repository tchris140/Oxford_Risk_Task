# This script downloads the personality data from the GitHub repository and saves it to a CSV file.
import requests
import pandas as pd
import os

# Create csv_files directory if it doesn't exist
if not os.path.exists('csv_files'):
    os.makedirs('csv_files')

# URL for the personality CSV file
PERSONALITY_DATA_URL = "https://raw.githubusercontent.com/karwester/behavioural-finance-task/refs/heads/main/personality.csv"

# Download the file
response = requests.get(PERSONALITY_DATA_URL)
with open('csv_files/personality.csv', 'wb') as f:
    f.write(response.content)

print("Downloaded personality data to csv_files/personality.csv")

# This script downloads the assets data from the Supabase API and saves it to a CSV file.

import requests
import pandas as pd

SUPABASE_URL = "https://pvgaaikztozwlfhyrqlo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2Z2FhaWt6dG96d2xmaHlycWxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NDE2MjUsImV4cCI6MjA2MzQxNzYyNX0.iAqMXnJ_sJuBMtA6FPNCRcYnKw95YkJvY3OhCIZ77vI"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}
url = f"{SUPABASE_URL}/rest/v1/assets?select=*"

response = requests.get(url, headers=headers)
data = response.json()
df = pd.DataFrame(data)
df.to_csv('csv_files/assets.csv', index=False)
print("Downloaded assets data to csv_files/assets.csv")

print("Datasets downloaded successfully to csv_files directory!") 