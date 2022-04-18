import requests
import json

#Use the "Export cookie JSON file for Puppeteer" Chrome extension to generate these files.
#A JSON file will be generated containing all the cookies for the website you are currently on.
with open('leetcode.com.cookies.json') as f:
	leetcookies = json.load(f)
formatted_cookies={}

for i in leetcookies:
    formatted_cookies[i['name']]=i['value']
#print(formatted_cookies)
#This is the LeetCode API, if you are currently logged in.
Url = "https://leetcode.com/api/problems/algorithms/"
request_reply = requests.get( Url, cookies=formatted_cookies)
data = request_reply.json()

#The default string is whatever blurb is currently in your LinkedIn about section that you want to stay there
default_string = "I am interested in applying statistical inferences to large datasets, currently working on AWS certificates.😃\n\n"

#This blurb is generated using the LeetCode JSON
leetcode_string = f'🔥🔥I\'ve Solved {data["num_solved"]} LeetCode problems, {data["ac_easy"]} Easy, {data["ac_medium"]} Medium and {data["ac_hard"]} Hard. This string is updated programmatically using Python and Selenium.🔥🔥'
combined_string = default_string+leetcode_string

print(combined_string)

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
driver= webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("https://www.linkedin.com")
with open('www.linkedin.com.cookies.json') as f:
    linkedincookies = json.load(f)
for i in linkedincookies:
    driver.add_cookie(i)
driver.get("https://www.linkedin.com/in/paul-jones-969577180/edit/forms/summary/new/?profileFormEntryPoint=PROFILE_SECTION&trackingId=l85%2BWyFQRMW17ic3JgyfWQ%3D%3D")

textarea = WebDriverWait(driver,5).until(lambda d: d.find_element(By.XPATH, '//*[@id="multiline-text-form-component-profileEditFormElement-SUMMARY-profile-ACoAACrMZ6EBNDja1YhNynYMasB0eX8VQ4LWTzc-summary"]'))
textarea.send_keys(Keys.CONTROL, 'a')
textarea.send_keys(combined_string)
driver.find_element(By.XPATH, '//*[@id="ember90"]').click()
driver.quit()
