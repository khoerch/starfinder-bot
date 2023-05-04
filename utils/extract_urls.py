import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs

"""
The scraping of data from 'https://www.aonsrd.com/' is done with the website owner's permission. Note that the intent of this work is to store text data from the website locally so that it can be embedded for use by our Question/Answer bot. Beware of making too many requests simultaneously or too quickly. 

For questions or clarifications, always best to contact the website owners directly. 

'https://www.aonsrd.com/ContactUs.aspx'
"""

main_url = 'https://www.aonsrd.com/'
filename = '../data/urls/starfinder.txt'

# Set of already checked URLs to avoid duplicates
checked_urls = set()
failed_urls = set()
with open(filename, 'r') as f:
    lines = f.read().splitlines()
    checked_urls.update(lines)

def check_links(url):
    """Recursively checks all links on a given URL within the same domain."""
    global checked_urls
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup and find all links
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    # Check each link on the page and append urls to file
    with open(filename, 'a') as f:
        for link in links:
            href = link.get('href')
            if href and not href.startswith('mailto:'):
                # Construct the absolute URL for the link
                abs_url = urljoin(url, href)
                # Parse the absolute URL to check if it belongs to the same domain
                parsed_url = urlparse(abs_url)
                if parsed_url.netloc == urlparse(main_url).netloc:
                    if abs_url not in checked_urls:
                        checked_urls.add(abs_url)
                        f.write(abs_url + '\n')
                        print(abs_url)
                        # Recursively try to check all links on the absolute URL
                        try:
                            check_links(abs_url)
                        except:
                            failed_urls.add(abs_url)


# Check all links on the main site
check_links(main_url)

print('')
print('---')
print(failed_urls)
print('Finished!!')
