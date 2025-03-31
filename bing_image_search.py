import requests
import os
import pandas as pd

# Your Bing Search API key
API_KEY = 'YOUR_BING_SEARCH_API_KEY'

def search_images(query):
    # API endpoint
    url = f'https://api.bing.microsoft.com/v7.0/images/search?q={query}&count=10'

    # Headers
    headers = {
        'Ocp-Apim-Subscription-Key': "d48cb7ab215a44e798466cb621ae0d99"
    }

    # Make the request
    response = requests.get(url, headers=headers)
    results = response.json()

    # Create a directory to save images
    if not os.path.exists('bing_images'):
        os.makedirs('bing_images')

    # Download and save images
    for idx, item in enumerate(results['value']):
        img_url = item['contentUrl']
        img_data = requests.get(img_url).content
        with open(f'bing_images/image_{idx}.jpg', 'wb') as handler:
            handler.write(img_data)

    print(f"Images have been downloaded and saved in the 'bing_images' directory.")

# Main function to run the script
if __name__ == '__main__':
    # Read the input from the CSV file
    csv_path = r'C:\Users\Aswin\OneDrive\Documents\Learning\projectFASHBuddy\last_rows_combined_output.csv'
    df = pd.read_csv(csv_path, header=None)
    
    # Assuming the fashion style description is in the first column of the last row
    search_query = df.iloc[-1, 0]
    
    search_images(search_query)
