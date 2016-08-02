#!/usr/bin/env python
""" That's script allows downloading competition data from kaggle. Prior to this
you should accept kaggle rules for downloading data on download page """

import shutil
import requests
import concurrent
import os
import bs4

def load_url(link_field, folder_path, buf_size):
    name = link_field.attrs['name']
    file_name = os.path.join(folder_path, name)
    file_url = url_main + link_field.attrs['href']

    with open(file_name, 'wb') as f:
        response = s.get(file_url, stream=True)
        shutil.copyfileobj(response.raw, f)                 # save response to file

    return "downloading {} is completed".format(name)
    
# challenge_name = 'grupo-bimbo-inventory-demand'
# challenge_name = 'talkingdata-mobile-user-demographics'
challenge_name = 'predicting-red-hat-business-value'
url_main = 'https://www.kaggle.com'
download_url = 'https://www.kaggle.com/c/{}/data'.format(challenge_name)
login_url = 'https://www.kaggle.com/account/login'

# enter your kaggle username and password
login_data = {'UserName':'', 
              'Password':''}

s = requests.session()
if login_data['UserName'] and login_data['Password']:
    s.post(login_url, data=login_data)
else:
    raise Exception("Enter your username and password")

r = s.get(download_url)
soup = bs4.BeautifulSoup(r.text, 'lxml')
download_table = soup.find('table', id='data-files')
file_urls = download_table.findAll('a')

buf_size = 1024*1024
# change to your folder path
folder_path = os.path.abspath('ml/{}/input'.format(challenge_name))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, folder_path, buf_size): url for url in file_urls}
    for future in concurrent.futures.as_completed(future_to_url):
        # print success result
        print(future.result())


# With multiprocessing module

# from multiprocessing.pool import ThreadPool as Pool
# pool = Pool(10)
# pool.starmap(load_url, (file_urls, folder_path, buf_size))


# With simple for loop

# for link_field in file_urls:
#     load_url(link_field, folder_path, buf_size)
