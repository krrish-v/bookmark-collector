import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd

'''
For utilizing this script, I had to use https://github.com/RodrigoTomeES/html-bookmark-to-csv to convert html file into CSV.
Here, I read that file, get the response along with metadata and write it into another CSV file.
That CSV file can be used to test embed cohere model and perform semantic search capability 
'''

def get_title(html):
    """Scrape page title."""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    return title


def get_description(html):
    """Scrape page description."""
    description = None
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get('content')
    elif html.find("meta", property="og:description"):
        description = html.find("meta", property="og:description").get('content')
    elif html.find("meta", property="twitter:description"):
        description = html.find("meta", property="twitter:description").get('content')
    elif html.find("p"):
        description = html.find("p").contents
    return description


def get_site_name(html, url):
    """Scrape site name."""
    if html.find("meta", property="og:site_name"):
        site_name = html.find("meta", property="og:site_name").get('content')
    elif html.find("meta", property='twitter:title'):
        site_name = html.find("meta", property="twitter:title").get('content')
    else:
        site_name = url.split('//')[1]
        return site_name.split('/')[0].rsplit('.')[1].capitalize()
    return site_name


csv_file = pd.read_csv('bookmarks_8_20_22.csv')
urlList = csv_file['url'].tolist()

url_meta_list = []
for url in urlList:
    if not url.startswith("http"):
        continue
    """Scrape target URL for metadata."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    pp = pprint.PrettyPrinter(indent=4)
    try:
        r = requests.get(url, headers=headers)
        html = BeautifulSoup(r.content, 'html.parser')
        metadata = {
            'title': get_title(html),
            'description': get_description(html),
            'sitename': get_site_name(html, url),
            'url': url
            }
        pp.pprint(metadata)
        url_meta_list.append(metadata)
    except:
      continue

url_meta_dataframe = pd.DataFrame(url_meta_list)
print(url_meta_dataframe.head())

url_meta_dataframe.to_csv("url_with_metadata.csv", index=False)
