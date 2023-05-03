import json
import requests
from bs4 import BeautifulSoup

"""
The scraping of data from 'https://www.aonsrd.com/' is done with the website owner's permission. Note that the intent of this work is to store text data from the website locally so that it can be embedded for use by our Question/Answer bot. Beware of making too many requests simultaneously or too quickly. 

For questions or clarifications, always best to contact the website owners directly. 

'https://www.aonsrd.com/ContactUs.aspx'
"""

# URL of the webpage to fetch
urls = ['https://www.aonsrd.com/StellarRevelations.aspx?ItemName=Destructive Discharge']
# Folder where we store text content
folder = '../data/content/'

def parse_filename(url, file_type = '.json'):
  name = url.split('com/')[1]
  name = name.replace('.aspx', '').replace('?', '').replace('=', '').replace(' ', '')
  return name + file_type

for url in urls:
  # Make a GET request to the URL and get the HTML content
  response = requests.get(url)
  html_content = response.content

  # Parse the HTML content using BeautifulSoup and extract the readable text
  soup = BeautifulSoup(html_content, 'html.parser')
  readable_text = soup.get_text()

  # Define the filename and json data to be saved
  filename = parse_filename(url)
  data = {'url': url, 'text': readable_text}

  # Write the readable text to the txt file in the designated folder
  with open(folder + filename, 'w', encoding="utf-8") as f:
    json.dump(data, f)