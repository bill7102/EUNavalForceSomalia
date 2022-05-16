# Suitable to be run in Juypiter Notebooks

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Create URL to scrape,
url = "https://eunavfor.eu/key-facts-and-figures?items_per_page=100&from=&to=&page="
start=0
data = []
while True:
    try:
        # Creeate a request to the URL with the page number
        urlWithPage = url + str(start)
        # Get the response from the URL
        r = requests.get(urlWithPage.format(urlWithPage))
        # Create a BeautifulSoup object from the response
        soup = BeautifulSoup(r.content, 'html.parser')
        # Find the table.   THe ID had to be determined by looking at the HTML.  The table is in this div.
        div = soup.find('div', attrs={'id': 'block-views-block-key-facts-block-incident-location'})
        # Find the table body
        table_body = div.find('tbody')
        # Find all the rows in the table body
        rows = table_body.find_all('tr')
        # Loop through each row
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            # Append the data to the data list
            data.append([ele for ele in cols])
        # Change to the next page
        start += 1    
    # If the page is not found, stop the loop.   This is the end of the data   
    except Exception as e:
        #print(e)
        break
# Create a dataframe from the data list
df = pd.DataFrame(data)
# Add the column names to the dataframe, could not manually obtain them from HTML accurately
df.columns = ['View on Map','Date','Vessel Type','Vessel','Flag','Event','Crew']
# Save the dataframe to a csv file
df.to_csv('data.csv', header='View on Map,Date,Vessel Type,Vessel,Flag,Event,Crew', index=False)

df['View on Map'].str.split(",", expand=True)
df