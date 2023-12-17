# Selenium

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import keyboard
import os
import time


# DRIVER
class Driver:
    # Initialize
    def __init__(self):
        PATH = "C:\chromedriver.exe"
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(PATH)
        print(f"\n--- Starting WebDriver with Selenium {selenium.__version__} ---")

    # Stay open for number of seconds
    def stayOpen(self, seconds, countdown):
        print("\n--- DONE ---")
        while seconds > 0:
            if countdown:
                print(f"{seconds}")
            seconds -= 1
            time.sleep(1)
        print("\nClosing Webdriver...")
        self.driver.quit()
        quit()

    # Navigate to specified URL
    def navTo(self, url, wait):
        print(f"\nNavigating to {url}")
        self.driver.get(url)
        time.sleep(wait)

    # Refresh page & wait for number of seconds
    def refresh(self, wait):
        print("\nRefreshing page")
        self.driver.refresh()
        time.sleep(wait)

    # Go back one page & wait for number of seconds
    def back(self, wait):
        print("\nGoing back one page")
        self.driver.back()
        time.sleep(wait)

    # Returns current URL
    def getUrl(self):
        return self.driver.current_url

    # Enter keywords
    def indeedEnterKeywords(self, keywords, wait):
        print(f'\nEntering keywords: "{keywords}"')
        keywordBox = self.driver.find_element(By.ID, "text-input-what")
        keywordBox.send_keys(keywords)
        time.sleep(wait)

    # Enter location
    def indeedEnterLocation(self, location, wait):
        print(f'\nEntering location: "{location}"')
        locationBox = self.driver.find_element(By.ID, "text-input-where")
        locationBox.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        locationBox.send_keys(location)
        time.sleep(wait)

    # Click search
    def indeedClickSearch(self, wait):
        print("\nClicking search button")
        searchButton = self.driver.find_element(
            By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton"
        )
        searchButton.click()
        time.sleep(wait)

    # Get jobs on page
    def indeedGetJobs(self, wait):
        urls = []

        print("\nLooking for jobs")
        jobs = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
        print(f"\n--- Found {len(jobs)} jobs ---")

        for job in jobs:
            link = job.find_element(By.TAG_NAME, "a")
            url = link.get_attribute("href")
            urls.append(url)
            print("\n" + link.text)
            print(url)

        time.sleep(wait)
        return urls


# MAIN
if __name__ == "__main__":
    # Search Indeed
    def searchIndeed():
        driver.navTo("https://www.indeed.com/", 3)
        driver.indeedEnterKeywords("Entry level Python", 3)
        driver.indeedEnterLocation("75081", 3)
        driver.indeedClickSearch(3)
        indeedJobLinks = driver.indeedGetJobs(3)
        driver.stayOpen(900, False)

    driver = Driver()
    searchIndeed()
