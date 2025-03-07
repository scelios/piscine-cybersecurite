import argparse
import urllib.request
import requests
from bs4 import BeautifulSoup 
from bs4 import XMLParsedAsHTMLWarning
import warnings
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import os

def fetch_url(url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def download_file(url, path= "./data/"):
    # create the folder if it doesn't exist
    filename = ""
    if not os.path.exists(path):
        os.makedirs(path)
    response = fetch_url(url)
    if not response:
        return
    # get the filename from the content-disposition header
    if "content-disposition" in response.headers:
        content_disposition = response.headers["content-disposition"]
        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[1]
    if not filename:
        filename = url.split("/")[-1]
    # check if the file already exists
    if os.path.exists(f"{path}{filename}"):
        return
    # save the file in the specified path
    with open(f"{path}{filename}", "wb") as file:
        file.write(response.content)


def get_links_and_images(url, path= "./data/", level=0, all_links=[]):
    if level < 0:
        return
    else:
        print(f" {level} Etching {url}")
        level -= 1
    response = fetch_url(url)
    if not response:
        return
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
    soup = BeautifulSoup(response.content, 'lxml')
    #get all links if one of the specified tags
    tags_with_urls = ['a', 'link', 'script', 'iframe', 'meta']
    links = []
    for tag in tags_with_urls:
        if tag == 'meta':
            links.extend([urljoin(url, meta['content']) for meta in soup.find_all(tag, content=True) if 'http' in meta['content']])
        else:
            links.extend([urljoin(url, tag_element['href']) for tag_element in soup.find_all(tag, href=True)])
            links.extend([urljoin(url, tag_element['src']) for tag_element in soup.find_all(tag, src=True)])
    links = list(set(links))

    # get images if is of the specified format
    images = [urljoin(url, img['src']) for img in soup.find_all('img', src=True) if img['src'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
    
    # remove links already visited
    for link in links:
        if link not in all_links:
            all_links.append(link)
            get_links_and_images(link, path, level, all_links)
    for image in images:
        download_file(image, path)
    # print(images)
    

def main():
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('-r', action='store_true', help='A boolean flag')
    parser.add_argument('-l', type=int, nargs='?', default=None, help='A positional argument')
    parser.add_argument('-p', type=str, nargs='?', default=None, help='A positional argument')
    parser.add_argument('url', type=str, help='A positional argument')

    args = parser.parse_args()

    # Stocker les arguments dans une variable
    if (args.r is True and args.l is None):
        args.l = 5
    arguments = {
        'r': args.r,
        'l': args.l if args.l is not None else 0,
        'p': args.p if args.p is not None else "./data/",
        'url': args.url
    }
    if (arguments['l'] < 0):
        print("Error: The level must be a positive number")
        return
    if (arguments['l'] > 5):
        print("Error: The level must be less than 5")
        return
    if (arguments['p'][-1] != "/"):
        arguments['p'] += "/"
    # print(arguments)
    # download_file(arguments['url'], arguments['p'])
    get_links_and_images(arguments['url'], arguments['p'], arguments['l'], [])
    


if __name__ == "__main__":
    main()