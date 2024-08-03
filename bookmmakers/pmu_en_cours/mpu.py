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

# Get the page source
html_content = driver.page_source

# Save the HTML content to a file
with open("pmu.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Close the browser
driver.quit()