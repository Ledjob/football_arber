from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from PIL import Image
import time
import os
import io

chromedriver_autoinstaller.install()

def take_scrolling_screenshot(driver, save_path):
    # Set a fixed viewport size
    viewport_width = 1920
    viewport_height = 1080
    driver.set_window_size(viewport_width, viewport_height)
    
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Calculate number of screenshots needed
    num_screenshots = -(-total_height // viewport_height)  # Ceiling division
    
    screenshots = []
    for i in range(num_screenshots):
        # Scroll to the appropriate position
        driver.execute_script(f"window.scrollTo(0, {i * viewport_height});")
        time.sleep(1)  # Wait for any dynamic content to load
        
        # Take screenshot of current viewport
        screenshot = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        screenshots.append(screenshot)
    
    # Create a new image with the full height
    full_image = Image.new('RGB', (viewport_width, total_height))
    
    # Paste all screenshots into the full image
    for i, screenshot in enumerate(screenshots):
        full_image.paste(screenshot, (0, i * viewport_height))
    
    # Save the full screenshot
    full_image.save(save_path)

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(chromedriver_autoinstaller.install())

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get('https://www.netbet.fr/football/france/ligue-1-mcdonald-stm')
    
    # Wait for the cookie popup to appear and click "Accepter"
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter')]"))
        ).click()
    except:
        print("Cookie acceptance button not found or not clickable. Proceeding anyway.")
    
    # Wait for the page to load
    time.sleep(5)
    
    # Take scrolling screenshot
    screenshot_path = 'full_page_screenshot.png'
    take_scrolling_screenshot(driver, screenshot_path)
    
    if os.path.exists(screenshot_path):
        print(f"Screenshot saved successfully at {os.path.abspath(screenshot_path)}")
    else:
        print("Failed to save screenshot.")

except Exception as e:
    print("An error occurred:", str(e))
    
    # Attempt to take a screenshot even if an error occurred
    try:
        driver.save_screenshot('error_screenshot.png')
        print("Error screenshot saved as error_screenshot.png")
    except:
        print("Failed to save error screenshot.")

finally:
    driver.quit()