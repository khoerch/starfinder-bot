import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs

"""
The scraping of data from 'https://www.aonsrd.com/' is done with the website owner's permission. Note that the intent of this work is to store text data from the website locally so that it can be embedded for use by our Question/Answer bot. Beware of making too many requests simultaneously or too quickly. 

For questions or clarifications, always best to contact the website owners directly. 

'https://www.aonsrd.com/ContactUs.aspx'
"""

# URL of the main site to scrape
main_url = 'https://www.aonsrd.com/'
filename = '../data/urls/starfinder.txt'

# Set of already checked URLs to avoid duplicates
checked_urls = set()

def extract_params(url):
    """Extracts all possible paths, queries, and params from a URL."""
    parsed_url = urlparse(url)
    paths = parsed_url.path.strip('/').split('/')
    queries = parse_qs(parsed_url.query)
    params = set()
    for path in paths:
        params.add(path)
        for query, values in queries.items():
            params.add('{}={}'.format(query, values[0]))
    return params

def check_links(url):
    """Recursively checks all links on a given URL with the same domain."""
    global checked_urls
    # Make a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all the links on the page
    links = soup.find_all('a')
    # Check each link on the page and append urls to txt file
    with open(filename, 'a') as f:
        for link in links:
            href = link.get('href')
            if href and not href.startswith('mailto:'):
                # Construct the absolute URL for the link
                abs_url = urljoin(url, href)
                # Parse the absolute URL to check if it belongs to the same domain
                parsed_url = urlparse(abs_url)
                if parsed_url.netloc == urlparse(main_url).netloc:
                    # Check if the absolute URL has already been checked to avoid duplicates
                    if abs_url not in checked_urls:
                        # Add the absolute URL to the set of checked URLs and append to file
                        checked_urls.add(abs_url)
                        f.write(abs_url + '\n')
                        # Print the absolute URL
                        print(abs_url)
                        # Recursively check all links on the absolute URL
                        check_links(abs_url)

# Check all links on the main site
check_links(main_url)

print('')
print('---')
print('Finished!!')
