from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime
# set the path for the Chrome driver executable file
driver_path = "path/to/chromedriver"

# create a Chrome driver instance
driver = webdriver.Chrome(executable_path=driver_path)


def website_open():
    driver.get("https://1xbet.cm/live/football/147087-egypt-premier-league")
    driver.implicitly_wait(10)
    driver.find_element(
        By.XPATH, "/html/body/div[6]/div/div[3]/button[1]").click()
    time.sleep(10)
    driver.find_element(
        By.XPATH, '//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a').click()

    time.sleep(10)
    

def event_goingOn():
    zeit = driver.find_element(
        By.XPATH, '//*[@id="games_content"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[2]/span[1]').text
    hours, minutes = map(int, zeit.split(':'))
    time_in_seconds = (hours * 60 * 60) + (minutes * 60)
    print("Time in seconds:", time_in_seconds)
    





website_open()
