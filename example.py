
# Module imports
import pytest
import requests
import time
import cloudscraper
from bs4 import BeautifulSoup

# Example variables to display
url = 'https://domain.com'
url_login = '/auth/login/'
params = {
    'grant_type': 'password',
    'id_username':'username', 
    'id_password':'12345678',
}

# 
def test_sessions():

    # Creating Session
    session = requests.session()

    # Session Headers 
    session.headers = {
        'Accept-Language': 'en-en',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Content-Type': 'text/html; charset=utf-8',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': url, 
        'Referer': '/auth/login/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/80.0.3987.160 Chrome/80.0.3987.163 Safari/537.36',
        
    }

    # Setting browser options
    browser={
        'browser': 'chrome', 
        'platform': 'windows',
        'mobile': False
    }

    # Creating CloudScraper object with Session
    scraper = cloudscraper.create_scraper(delay=10, sess=session, browser=browser, allow_brotli=False, debug=True)

    # Opening Auth Login Page for get csrftoken
    client_login = scraper.get(url + url_login)

    # Creating BeautifulSoup object from client response
    soup = BeautifulSoup(client_login.content, features='html.parser')

    # Find csrfmiddlewaretoken with Soup and Add to params
    csrfmiddlewaretoken = soup.find('input', attrs = {'name':'csrfmiddlewaretoken'})['value']

    # Set additional params from cookies and request
    # Another way to get the csrftoken
    # session.cookies['csrftoken'] 
    params['csrfmiddlewaretoken'] = csrfmiddlewaretoken
    params['csrftoken'] = client_login.cookies['csrftoken']
    params['affkey'] = client_login.cookies['affkey']
    params['sbr'] = client_login.cookies['sbr']
    params['__cf_bm'] = client_login.cookies['__cf_bm']

    # Set additional params from data
    # session.headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in client_login.cookies])
    session.headers['Authorization'] = "Bearer " + client_login.cookies['csrftoken']
    
    # LogIn Request
    response = scraper.post(url=url, params=params, cookies=client_login.cookies)
    print(response.status_code)
    print(session.cookies.get_dict())

    print('Opening Profile User Page...')
    res = session.get(url + '/profile')
    print(res.status_code)
    print(res.text)    
    

def main():

    test_sessions()
    print('Control + C para salir...')
    time.sleep(10)


if __name__ == '__main__':
    
  main()


  