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
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver import ChromeOptions as ChromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#options = ChromeOptions()
options = FirefoxOptions()

#allows firefox to run without showing a graphical interface.
options.add_argument("--headless")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver= webdriver.Chrome(service=Service(GeckoDriverManager().install()),options=options)
#For the cookies to work, you need to initially be ON the domain you're adding cookies for.
#Doing something else will result in an error.
driver.get("https://www.linkedin.com")
formatted_cookies={}
with open('www.linkedin.com.cookies.json') as f:
    linkedincookies = json.load(f)
for i in linkedincookies:
    driver.add_cookie(i)
#Go to your linkedIn About section and click Edit. Then copy the URL generated and paste it here.
driver.get(<LINKEDIN ABOUT EDIT PAGE HERE>)
driver.implicitly_wait(5)
#password_locator = driver.locate_with(By.TAG_NAME, "input").below({By.ID: "email"})
#these sections might be individual to the user, not completely sure, just use the inspect element to find the buttons, then right-click and go "copy XPATH" for this to work
textarea = driver.find_element(By.XPATH, '//*[@id="multiline-text-form-component-profileEditFormElement-SUMMARY-profile-ACoAACrMZ6EBNDja1YhNynYMasB0eX8VQ4LWTzc-summary"]')
#Select all and delete old blurb
textarea.send_keys(Keys.CONTROL, 'a')
textarea.send_keys(Keys.BACKSPACE)
textarea.send_keys(combined_string)
driver.implicitly_wait(1)
driver.find_element(By.XPATH, '//*[@id="ember90"]').click()
driver.implicitly_wait(5)
driver.quit()
