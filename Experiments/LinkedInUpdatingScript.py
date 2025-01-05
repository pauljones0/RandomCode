import requests
import json

with open('leetcode.com.cookies.json') as f:
	leetcookies = json.load(f)
formatted_cookies={}

for i in leetcookies:
    formatted_cookies[i['name']]=i['value']
Url = "https://leetcode.com/api/problems/algorithms/"
request_reply = requests.get( Url, cookies=formatted_cookies)
data = request_reply.json()

new_string = f'I\'ve Solved {data["num_solved"]} LeetCode problems, {data["ac_easy"]} Easy, {data["ac_medium"]} Medium and {data["ac_hard"]} Hard. This string is updated programmatically using Python and Selenium.'

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver= webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=options)
driver.get("https://www.linkedin.com")
with open('www.linkedin.com.cookies.json') as f:
    linkedincookies = json.load(f)
for i in linkedincookies:
    driver.add_cookie(i)
    
    
driver.get(EDIT_ABOUT)

textarea = WebDriverWait(driver,5).until(lambda d: d.find_element(By.XPATH, EDIT_XPATH))

action = webdriver.ActionChains(driver)
action.send_keys_to_element(textarea, Keys.ARROW_LEFT, Keys.ARROW_LEFT).key_down(Keys.SHIFT).send_keys(Keys.HOME,Keys.ARROW_UP,Keys.ARROW_RIGHT,Keys.ARROW_RIGHT).key_up(Keys.SHIFT).send_keys(new_string).perform()
driver.find_element(By.XPATH, '//*[@id="ember90"]').click()
driver.quit()

action = webdriver.ActionChains(driver)
action.send_keys_to_element(textarea, Keys.ARROW_LEFT, Keys.ARROW_LEFT).key_down(Keys.SHIFT).send_keys(Keys.HOME,Keys.ARROW_UP,Keys.ARROW_RIGHT,Keys.ARROW_RIGHT).key_up(Keys.SHIFT).send_keys(new_string).perform()
driver.find_element(By.XPATH, '//*[@id="ember90"]').click()
driver.quit()
