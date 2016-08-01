import shutil
import requests
import concurrent
import bs4

def load_url(link_field, buf_size):
    name = link_field.attrs['name']
    file_url = url_main + link_field.attrs['href']

    with open(name, 'wb') as f:
        response = s.get(file_url, stream=True)
        # save response to file
        shutil.copyfileobj(response.raw, f, length=buf_size) 

    return "downloading {} is completed".format(name)
    
# challenge_name = 'grupo-bimbo-inventory-demand'
challenge_name = 'talkingdata-mobile-user-demographics'
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

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, buf_size): url for url in file_urls}
    for future in concurrent.futures.as_completed(future_to_url):
        # print success result
        print(future.result())


# With multiprocessing module

# from multiprocessing.pool import ThreadPool as Pool
# pool = Pool(10)
# pool.map(load_url, file_urls)


# With simple for loop

# for link_field in file_urls:
#     load_url(link_field)
