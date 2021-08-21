from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from dotenv import dotenv_values

# load env
env = dotenv_values(".env")

def instagram_login():
    browser = webdriver.Chrome()
    url = 'https://www.instagram.com/'

    # go to url
    browser.get(url)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'username')))

    # find username and password location
    username_input = browser.find_elements_by_name('username')[0]
    password_input = browser.find_elements_by_name('password')[0]

    # set username and password
    username_input.send_keys(env['instagram_username'])
    password_input.send_keys(env['instagram_password'])

    # login
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
    login_click = browser.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')[0]
    login_click.click()

    # wait for first window
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))

    return browser

def get_headers():
    # login instagram
    browser = instagram_login()

    # get cookie
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    mid = browser.get_cookie('mid')
    sessionid = browser.get_cookie('sessionid')

    # close browser
    browser.close()

    return {
        'user-agent': user_agent,
        'cookie': 'mid=%s;sessionid=%s;'%(mid['value'], sessionid['value'])
    }

if __name__ == '__main__':
    # get ig headers
    headers = get_headers()

    tag_name = env['tag_name']
    api_url  = 'https://www.instagram.com/explore/tags/%s/?__a=1'%tag_name

    # request get with header
    result = requests.get(api_url, headers = headers)

    print(result.status_code)