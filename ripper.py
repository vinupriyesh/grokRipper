from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import os



grok_url = input("Enter grok url : ")
download_path = input("Enter download directory : ")

parsed_uri = urlparse(grok_url)
hostname = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
print(hostname)

def get_all_links(url):
    links = []
    files = []
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data,features="html.parser")
    for tr in soup.find_all("tr"):
        current_link = None
        for td in tr.find_all("td"):
            for a in td.find_all('a'):
                if(a.get('href') != '..' and type(td.get("class"))!= list):
                    current_link = url+a.get('href')
            if type(td.get("class"))==list:                
                if td.get("class")[0] == "q":            
                    for a in td.find_all('a'):
                        if a.get('title') == "Download":
                            files.append(a.get('href'))
                            current_link = None
        if(current_link):
            links.append(current_link)  
    return files,links

def download_files(files):
    for f in files:    
        print("Downloading : "+f)
        r = requests.get(hostname+f, stream=True)
        os.makedirs(os.path.dirname(download_path+f), exist_ok=True)
        with open(download_path+f, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: 
                    f.write(chunk)
    
def rip(links):
    for url in links:
        print("Ripping URL "+url)
        files, new_links = get_all_links(url)
        download_files(files)
        rip(new_links)    


urls = []
urls.append(grok_url)
rip(urls)
print("Completed")

