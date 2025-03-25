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
import signal
from urllib.parse import urlparse
import socket

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("The operation timed out")

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False

        socket.gethostbyname(parsed.netloc)
        return True
    except (socket.gaierror, ValueError):
        return False

def fetch_url(url, timeout=2, max_execution_time=2):

    if not is_valid_url(url):
        print(f"Invalid URL or domain cannot be resolved: {url}")
        return None

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(max_execution_time) 

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response
    except TimeoutException:
        print(f"Global timeout occurred while fetching {url}")
        return None
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    finally:
        signal.alarm(0) 

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
    parser = argparse.ArgumentParser(description='The spider program allow you to extract all the images from a website, recursively, by providing a url as a parameter.')
    parser.add_argument('-r', action='store_true', help='Recursively downloads the images in a URL received as a parameter')
    parser.add_argument('-l', type=int, nargs='?', default=None, help='Indicates the maximum depth level of the recursive download.\nIf not indicated, it will be 5')
    parser.add_argument('-p', type=str, nargs='?', default=None, help='indicates the path where the downloaded files will be saved.\nIf not specified, ./data/ will be used.')
    parser.add_argument('url', type=str, help='URL')

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
    if (arguments['l'] < 0 or arguments['l'] is None or not isinstance(arguments['l'], int)):
        print("Error: The level must be a positive number")
        return
    if (arguments['l'] > 5):
        print("Error: The level must be less than 5")
        return
    if (arguments['p'][-1] != "/"):
        arguments['p'] += "/"


    try:
        get_links_and_images(arguments['url'], arguments['p'], arguments['l'], [])
    except KeyboardInterrupt:
        print("The program was interrupted by the user")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return


if __name__ == "__main__":
    main()