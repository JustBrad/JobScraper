# Selenium

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ColorCodes import Colors as c
import undetected_chromedriver as uc
import keyboard
import os
import platform
import time
import random
import pandas as pd


# DRIVER
class Driver:
    # Initialize
    def __init__(self):
        self.TITLES = []
        self.LOCATIONS = []
        self.TYPES = []
        self.PAYRATES = []
        self.URLS = []

        if platform.system() == "Darwin":
            PATH = r"\Users\bradegbert\chromedriver"
            OPTIONS = webdriver.ChromeOptions()
            OPTIONS.add_experimental_option("detach", True)
            OPTIONS.add_experimental_option("excludeSwitches", ["enable-automation"])
            OPTIONS.add_experimental_option("useAutomationExtension", False)
            OPTIONS.add_argument("--disable-blink-features=AutomationControlled")
            self.driver = webdriver.Chrome(options=OPTIONS)
            print(
                f"\n{c.PURPLE}--- Starting WebDriver with Selenium {selenium.__version__} on macOS ---{c.RESET}"
            )
        else:
            PATH = "C:\chromedriver.exe"
            OPTIONS = uc.ChromeOptions()
            self.driver = uc.Chrome(use_subprocess=True, options=OPTIONS)
            print(
                f"\n{c.PURPLE}--- Starting WebDriver with Selenium {selenium.__version__} on Windows ---{c.RESET}"
            )

    # Wait random number of seconds
    def waitRandom(self):
        sleep = random.randint(2, 3)
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
        self.driver.close()
        self.driver.quit()

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
        print(f"\nScrolling {c.YELLOW}DOWN{c.RESET}")
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        y = 500
        for timer in range(0, 5):
            self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 500
            time.sleep(1)

    ### --- INDEED --- ###

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
        if platform.system() == "Darwin":
            locationBox.send_keys(Keys.COMMAND + "a", Keys.BACKSPACE)
        else:
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
    def indeedGetJobInfo(self, links):
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
                self.TITLES += title.text
                print(c.YELLOW + title.text + c.RESET)
            except:
                self.TITLES += "NONE"
                print(c.RED + "No title provided" + c.RESET)

            # Get job location
            try:
                location = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="viewJobSSRRoot"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div',
                )
                self.LOCATIONS += location.text
                print(location.text)
            except:
                self.LOCATIONS += "NONE"
                print(c.RED + "No location provided" + c.RESET)

            # Get salary info
            try:
                salaryArea = self.driver.find_element(By.ID, "salaryInfoAndJobType")
                salaryInfo = salaryArea.find_elements(By.TAG_NAME, "span")
                for info in salaryInfo:
                    if info.text[0] == "-":
                        self.TYPES += info.text[2::]
                        print(c.GREEN + info.text[2::] + c.RESET)
                    else:
                        self.PAYRATES += info.text
                        print(c.GREEN + info.text + c.RESET)
            except:
                self.PAYRATES += "NONE"
                print(c.RED + "No salary provided" + c.RESET)

            print(
                f"{c.DKGRAY}Jobs explored ({links.index(link) + 1}/{len(links)})\n{c.RESET}"
            )
        self.waitRandom()

    ### --- SIMPLY HIRED --- ###

    def shEnterKeywords(self, keywords):
        print(f"\nEntering keywords: {c.YELLOW}{keywords}{c.RESET}")
        keywordBox = self.driver.find_element(By.ID, "field-:R3bakt9fbqm:")
        keywordBox.send_keys(keywords)
        self.waitRandom()

    def shEnterLocation(self, location):
        print(f"\nEntering location: {c.YELLOW}{location}{c.RESET}")
        locationBox = self.driver.find_element(By.ID, "field-:R5bakt9fbqm:")
        if platform.system() == "Darwin":
            locationBox.send_keys(Keys.COMMAND + "a", Keys.BACKSPACE)
        else:
            locationBox.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        locationBox.send_keys(location)
        self.waitRandom()

    def shClickSearch(self):
        print(f"\nClicking {c.YELLOW}SEARCH{c.RESET}")
        searchButton = self.driver.find_element(
            By.CSS_SELECTOR,
            "#__next > main > div > div.css-imseer > form > div > div.css-nq12ob > div > div > button",
        )
        searchButton.click()
        self.waitRandom()
        self.waitRandom()

    def shGetJobs(self, pages):
        urls = []
        pagesToSearch = pages

        while pagesToSearch > 0:
            self.scrollDown()
            jobList = self.driver.find_element(By.ID, "job-list")
            listElements = jobList.find_elements(By.TAG_NAME, "li")
            for l in listElements:
                aTag = l.find_element(By.TAG_NAME, "a")
                urls.append(aTag.get_attribute("href"))

            pagesToSearch -= 1

            # Look for next page button
            if pagesToSearch > 0:
                try:
                    print(f"\nGoing to {c.YELLOW}NEXT PAGE{c.RESET}")
                    nextPageButton = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "#__next > div > main > div > div.css-17iqsqz > div > div > div.css-2jn6zr > div > div.css-15g2oxy > div.css-ukpd8g > nav > a.chakra-link.css-1puj5o8",
                    )
                    nextPageButton.click()
                    self.waitRandom()
                except:
                    print(f"\n{c.RED}No more pages{c.RESET}")

        return urls

    def shGetJobInfo(self, links):
        print(f"\nFound {c.YELLOW}{len(links)} JOBS{c.RESET}\n")
        for link in links:
            self.navTo(link)

            # Print URL
            print(c.UNDERLINE + c.DKGRAY + self.getUrl() + c.RESET)

            # Get job title
            try:
                title = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div/main/div/div/aside/header/div/div/div[1]/h1",
                )
                self.TITLES.append(title.text)
                print(c.YELLOW + title.text + c.RESET)
            except:
                self.TITLES.append("NONE")
                print(c.RED + "No title provided" + c.RESET)

            # Get job location
            try:
                location = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > div > main > div > div > aside > header > div > div > div.css-1r85bh9 > div.chakra-stack.css-m3jj3s > span:nth-child(2) > span > span",
                )
                self.LOCATIONS.append(location.text)
                print(location.text)
            except:
                self.LOCATIONS.append("NONE")
                print(c.RED + "No location provided" + c.RESET)

            # Get type info
            try:
                type = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > div > main > div > div > aside > div > div:nth-child(1) > div > div:nth-child(1) > div > span:nth-child(1) > span > span",
                )
                self.TYPES.append(type.text)
                print(f"{c.GREEN}{type.text}{c.RESET}")
            except:
                self.TYPES.append("NONE")
                print(c.RED + "No type provided" + c.RESET)

            # Get pay info
            try:
                pay = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > div > main > div > div > aside > div > div:nth-child(1) > div > div:nth-child(1) > div > span:nth-child(2) > span > span",
                )
                self.PAYRATES.append(pay.text)
                print(f"{c.GREEN}{pay.text}{c.RESET}")
            except:
                self.PAYRATES.append("NONE")
                print(c.RED + "No salary provided" + c.RESET)

            print(
                f"{c.DKGRAY}Jobs explored ({links.index(link) + 1}/{len(links)})\n{c.RESET}"
            )


# MAIN
if __name__ == "__main__":
    # Export CSV
    def exportCsv(driver):
        print(f"TITLES: {len(driver.TITLES)}")
        print(f"LOCATIONS: {len(driver.LOCATIONS)}")
        print(f"TYPES: {len(driver.TYPES)}")
        print(f"PAYRATES: {len(driver.PAYRATES)}")
        print(f"URLS: {len(driver.URLS)}")
        data = {
            "JOB TITLE": driver.TITLES,
            "LOCATION": driver.LOCATIONS,
            "DETAILS": driver.TYPES,
            "DETAILS 2": driver.PAYRATES,
            "URL": driver.URLS,
        }

        df = pd.DataFrame(data)
        df.to_csv("JobListings.csv", index=False)
        print(f"\n{c.PURPLE}--- CSV GENERATED ---{c.RESET}")

    # Search Indeed
    def searchIndeed(keywords, location, pages):
        driver.navTo("https://www.indeed.com/")
        driver.indeedEnterKeywords(keywords)
        driver.indeedEnterLocation(location)
        driver.indeedClickSearch()
        indeedJobLinks = driver.indeedGetJobs(pages)
        driver.URLS += indeedJobLinks
        driver.indeedGetJobInfo(indeedJobLinks)

    # Search SimplyHired
    def searchSimplyHired(keywords, location, pages):
        driver.navTo("https://www.simplyhired.com/")
        driver.shEnterKeywords(keywords)
        driver.shEnterLocation(location)
        driver.shClickSearch()
        shJobLinks = driver.shGetJobs(pages)
        driver.URLS += shJobLinks
        driver.shGetJobInfo(shJobLinks)

        driver.stayOpen(3, False)

    driver = Driver()
    # searchIndeed("python entry level", "75081", 1)
    searchSimplyHired("ups", "75081", 1)
    exportCsv(driver)
    quit()
