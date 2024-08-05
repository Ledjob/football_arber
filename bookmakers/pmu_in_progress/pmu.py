from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller


chromedriver_autoinstaller.install()

# URL of the website
url = "https://parisportif.pmu.fr/home/wrapper/events?activeSportId=1&leagues=%5B123%5D"



# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (optional)
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# Set up Chrome WebDriver
service = Service()  # Update with your path to chromedriver
driver = webdriver.Chrome(service=service)

# Open the website
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds for the elements to appear

try:
    # Check if the content is within an iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        driver.switch_to.frame(iframes[0])

    # Wait until at least one match element is present
    matches = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sb-event-list__sport-wrapper ng-tns-c287-189 ng-trigger ng-trigger-fadeIn sb-event-list__sport-wrapper--desktop sb-event-list__sport-wrapper--first ng-star-inserted")))
    

    # Extract teams and odds
    for match in matches:
        # Find team names within the match element
        teams = match.find_elements(By.CSS_SELECTOR, "span.sb-event-list__competitor")
        
        # Find odds within the match element
        odds = match.find_elements(By.CSS_SELECTOR, "div.sb-event-list__outcome")

        # Extract and print team names and odds
        if teams and odds:
            team_names = [team.text for team in teams]
            odds_values = [odd.text for odd in odds]
            print(f"Teams: {team_names}, Odds: {odds_values}")

except Exception as e:
    # Print the page source for debugging
    # print("this is: {}", driver.page_source)
    print("can't find it bro")
    print(e)

finally:
    # Close the WebDriver
    driver.quit()



