# Selenium

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from ColorCodes import Colors as c
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
        print(f"+ \n--- Starting WebDriver with Selenium {selenium.__version__} ---")

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

        time.sleep(wait)
        return urls

    def indeedFilterJobs(self, links, wait):
        print("\n--- Searching for good jobs ---\n")
        for link in links:
            self.navTo(link, wait)

            # Print URL
            print(self.getUrl())

            # Get job title
            try:
                titleContainer = self.driver.find_element(
                    By.CLASS_NAME, "jobsearch-JobInfoHeader-title"
                )
                title = titleContainer.find_element(By.TAG_NAME, "span")
                print(title.text)
            except:
                print("No title provided")

            # Get job location
            try:
                location = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div',
                )
                print(location.text)
            except:
                print("No location provided")

            # Get salary info
            try:
                salaryArea = self.driver.find_element(By.ID, "salaryInfoAndJobType")
                salaryInfo = salaryArea.find_elements(By.TAG_NAME, "span")
                for info in salaryInfo:
                    if info.text[0] == "-":
                        print(info.text[2::])
                    else:
                        print(info.text)
            except:
                print("No salary provided")

            # Get job rating
            try:
                jobRating = self.driver.find_element(By.ID, "companyRatings")
                rating = jobRating.get_attribute("aria-label")
                print(rating)
            except:
                print("No rating provided")

            print(f"Jobs explored ({links.index(link) + 1}/{len(links)})\n")
        time.sleep(wait)


# MAIN
if __name__ == "__main__":
    # Search Indeed
    def searchIndeed(keywords, location, wait):
        driver.navTo("https://www.indeed.com/", wait)
        driver.indeedEnterKeywords(keywords, wait)
        driver.indeedEnterLocation(location, wait)
        driver.indeedClickSearch(wait)
        indeedLinks = driver.indeedGetJobs(wait)
        driver.indeedFilterJobs(indeedLinks, wait)

    driver = Driver()
    searchIndeed("Entry level Python", "75081", 2)
    driver.stayOpen(900, False)
