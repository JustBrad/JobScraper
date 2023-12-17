# Selenium

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ColorCodes import Colors as c
import keyboard
import os
import time
import random


# DRIVER
class Driver:
    # Initialize
    def __init__(self):
        PATH = "C:\chromedriver.exe"
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_experimental_option("detach", True)
        OPTIONS.add_experimental_option("excludeSwitches", ["enable-automation"])
        OPTIONS.add_experimental_option("useAutomationExtension", False)
        OPTIONS.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=OPTIONS)
        print(f"+ \n--- Starting WebDriver with Selenium {selenium.__version__} ---")

    # Wait random number of seconds
    def waitRandom(self):
        sleep = random.randint(5, 15)
        print(f"\n{c.BLUE}Waiting {sleep} seconds...{c.RESET}")
        time.sleep(sleep)

    # Stay open for number of seconds
    def stayOpen(self, seconds, countdown):
        print(f"{c.GREEN}\n--- DONE ---{c.RESET}")
        while seconds > 0:
            if countdown:
                print(f"{seconds}")
            seconds -= 1
            time.sleep(1)
        print("\nClosing Webdriver...")
        self.driver.quit()
        quit()

    # Navigate to specified URL
    def navTo(self, url):
        self.driver.get(url)
        self.waitRandom()

    # Refresh page & wait for number of seconds
    def refresh(self):
        print("\nRefreshing page")
        self.driver.refresh()
        self.waitRandom()

    # Go back one page & wait for number of seconds
    def back(self):
        print("\nGoing back one page")
        self.driver.back()
        self.waitRandom()

    # Returns current URL
    def getUrl(self):
        return self.driver.current_url

    # Scrolls down to bottom of page
    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Enter keywords
    def indeedEnterKeywords(self, keywords):
        print(f"\nEntering keywords: {c.YELLOW}{keywords}{c.RESET}")
        keywordBox = self.driver.find_element(By.ID, "text-input-what")
        keywordBox.send_keys(keywords)
        self.waitRandom()

    # Enter location
    def indeedEnterLocation(self, location):
        print(f"\nEntering location: {c.YELLOW}{location}{c.RESET}")
        locationBox = self.driver.find_element(By.ID, "text-input-where")
        locationBox.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        locationBox.send_keys(location)
        self.waitRandom()

    # Filter by experience level | 0=none | 1=entry | 2=mid | 3=senior |
    def indeedFilterExperience(self, experience):
        if experience == 0:
            xpString = "NO EXPERIENCE"
        elif experience == 1:
            xpString = "ENTRY LEVEL"
        elif experience == 2:
            xpString = "MID LEVEL"
        elif experience == 3:
            xpString = "SENIOR LEVEL"

        print(f"\nFiltering by {c.YELLOW}{xpString}{c.RESET}")

        xpDropdown = self.driver.find_element(By.ID, "filter-explvl")
        xpDropdown.click()

        dropdownContainer = self.driver.find_element(By.ID, "filter-explvl-menu")
        dropdownOptions = dropdownContainer.find_elements(By.TAG_NAME, "li")

        # Get available experience level categories
        for i in range(4):
            try:
                option = dropdownOptions[i]
                if option.text.startswith("No"):
                    optionNoExperience = option
                elif option.text.startswith("Entry"):
                    optionEntryLevel = option
                elif option.text.startswith("Mid"):
                    optionMidLevel = option
                elif option.text.startswith("Senior"):
                    optionSeniorLevel = option
                else:
                    pass
                print(f"\n{option.text}{c.GREEN} FOUND{c.RESET}")
            except:
                print(f"\nOption {i+1} {c.RED}NOT FOUND{c.RESET}")

        # Click on specified experience if available
        try:
            if experience == 0:
                optionNoExperience.click()
            elif experience == 1:
                optionEntryLevel.click()
            elif experience == 2:
                optionMidLevel.click()
            elif experience == 3:
                optionSeniorLevel.click()
            else:
                print(c.RED + "\nInvalid experience parameter" + c.RESET)
        except:
            print(c.RED + f"\nFailed to click {xpString} option" + c.RESET)

        self.waitRandom()

    # Click search
    def indeedClickSearch(self):
        print(f"\nClicking {c.YELLOW}SEARCH{c.RESET}")
        searchButton = self.driver.find_element(
            By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton"
        )
        searchButton.click()
        self.waitRandom()

    # Get jobs on page
    def indeedGetJobs(self, pages):
        urls = []
        pagesToSearch = pages

        while pagesToSearch > 0:
            # Grab job posts
            self.waitRandom()
            print(f"\nLooking for {c.YELLOW}JOBS{c.RESET}")
            self.scrollDown()
            jobs = self.driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

            # Grab job URLs
            for job in jobs:
                link = job.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
                urls.append(url)

            # Click next page
            navElements = self.driver.find_elements(By.TAG_NAME, "nav")
            for navElement in navElements:
                liElements = navElement.find_elements(By.TAG_NAME, "li")
                for liElement in liElements:
                    aElement = liElement.find_element(By.TAG_NAME, "a")
                    if aElement.get_attribute("data-testid") == "pagination-page-next":
                        nextPageButton = aElement
                        print(f"\nGoing to {c.YELLOW}NEXT PAGE{c.RESET}")
                        nextPageButton.click()
                        time.sleep(5)
            pagesToSearch -= 1

        self.waitRandom()
        return urls

    # Go through jobs & grab info
    def indeedFilterJobs(self, links):
        print(f"\nFound {c.YELLOW}{len(links)} JOBS{c.RESET}\n")
        for link in links:
            self.navTo(link)

            # Print URL
            print(c.UNDERLINE + c.DKGRAY + self.getUrl() + c.RESET)

            # Get job title
            try:
                titleContainer = self.driver.find_element(
                    By.CLASS_NAME, "jobsearch-JobInfoHeader-title"
                )
                title = titleContainer.find_element(By.TAG_NAME, "span")
                print(c.YELLOW + title.text + c.RESET)
            except:
                print(c.RED + "No title provided" + c.RESET)

            # Get job location
            try:
                location = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div',
                )
                print(location.text)
            except:
                print(c.RED + "No location provided" + c.RESET)

            # Get salary info
            try:
                salaryArea = self.driver.find_element(By.ID, "salaryInfoAndJobType")
                salaryInfo = salaryArea.find_elements(By.TAG_NAME, "span")
                for info in salaryInfo:
                    if info.text[0] == "-":
                        print(c.GREEN + info.text[2::] + c.RESET)
                    else:
                        print(c.GREEN + info.text + c.RESET)
            except:
                print(c.RED + "No salary provided" + c.RESET)

            # Get job rating
            try:
                jobRating = self.driver.find_element(By.ID, "companyRatings")
                rating = jobRating.get_attribute("aria-label")
                print(rating)
            except:
                print(c.RED + "No rating provided" + c.RESET)

            print(
                f"{c.DKGRAY}Jobs explored ({links.index(link) + 1}/{len(links)})\n{c.RESET}"
            )
        self.waitRandom()

    # Bypass CAPTCHA (not working)
    def verifyHuman(self, wait):
        print(f"\n{c.PURPLE}Checking for CAPTCHA{c.RESET}")
        try:
            self.waitRandom()
            WebDriverWait(self.driver, wait).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (
                        By.CSS_SELECTOR,
                        "#challenge-stage",
                    )
                )
            )
            WebDriverWait(driver, wait).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#challenge-stage > div > label")
                )
            ).click()
        except:
            print(f"\n{c.GREEN}CAPTCHA not found{c.RESET}\n")


# MAIN
if __name__ == "__main__":
    # Search Indeed
    def searchIndeed(keywords, location, pages):
        driver.navTo("https://www.indeed.com/")
        driver.indeedEnterKeywords(keywords)
        driver.indeedEnterLocation(location)
        driver.indeedClickSearch()
        indeedLinks = driver.indeedGetJobs(pages)
        driver.indeedFilterJobs(indeedLinks)

    driver = Driver()
    searchIndeed("python entry level", "75081", 2)
    driver.stayOpen(900, False)
