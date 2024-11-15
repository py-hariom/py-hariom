from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import logging

# Set up logging to capture details during the script execution
logging.basicConfig(filename='scraping_log.log', level=logging.INFO)
logger = logging.getLogger()

# Configure WebDriver (adjust the path to your actual chromedriver location)
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Open the login page
login_url = "https://55club05.com/#/login"
driver.get(login_url)
logger.info("Navigated to login page")

# Wait for login page elements to load
try:
    phone_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[4]/div[1]/div/div[1]/div[2]'))
    )
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[4]/div[1]/div/div[2]/div[2]'))
    )
    logger.info("Login page elements loaded")
except Exception as e:
    logger.error(f"Error loading login page elements: {e}")
    driver.quit()

# Manually log in with provided credentials
phone_number = "9876543210"
password = "password@123"

# Enter phone number
phone_input.send_keys(phone_number)
logger.info("Entered phone number")

# Enter password
password_input.send_keys(password)
logger.info("Entered password")

# Submit the login form
password_input.send_keys(Keys.RETURN)
logger.info("Login submitted")

# Wait for successful login and page redirection to the main lottery page
try:
    WebDriverWait(driver, 30).until(
        EC.url_contains("/home/AllLotteryGames/WinGo?id=1")
    )
    logger.info("Successfully logged in and redirected to the lottery page")
except Exception as e:
    logger.error(f"Login failed or page redirection error: {e}")
    driver.quit()

# Now scrape the lottery data page
lottery_page_url = "https://55club05.com/#/home/AllLotteryGames/WinGo?id=1"
driver.get(lottery_page_url)
logger.info(f"Navigating to lottery page: {lottery_page_url}")

# Wait for key data elements to load before scraping
try:
    period = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[8]/div[2]/div[1]/div[1]'))
    ).text
    logger.info(f"Period: {period}")

    winning_number = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[8]/div[2]/div[1]/div[2]'))
    ).text
    logger.info(f"Winning Number: {winning_number}")

    big_small = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[8]/div[2]/div[1]/div[3]'))
    ).text
    logger.info(f"Big/Small: {big_small}")

    color = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[8]/div[2]/div[1]/div[4]'))
    ).text
    logger.info(f"Color: {color}")

except Exception as e:
    logger.error(f"Error while extracting lottery data: {e}")
    driver.quit()

# Navigate through multiple data sections or lottery results
try:
    # Example: Click a button to view more results
    more_results_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div[4]/div[1]/div/div[2]/div[1]'))
    )
    ActionChains(driver).move_to_element(more_results_button).click().perform()
    logger.info("Clicked to view more results")
    
    # Wait for new data to load
    time.sleep(5)
    
    # Scrape more results or lottery info
    additional_info = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[4]/div[2]/div/div[2]').text
    logger.info(f"Additional Info: {additional_info}")
    
except Exception as e:
    logger.error(f"Error during interaction or additional data scraping: {e}")
    driver.quit()

# Navigate through pages or multiple sections if necessary
try:
    # Example: Click on the next page button or similar interaction
    next_page_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div[8]/div[3]/button'))
    )
    ActionChains(driver).move_to_element(next_page_button).click().perform()
    logger.info("Navigated to the next page")
    
    # Wait and scrape additional data if needed
    time.sleep(3)
    
except Exception as e:
    logger.error(f"Error while navigating to the next page: {e}")
    driver.quit()

# Extract a detailed list of all available lottery games
try:
    games_list = driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div[8]/div[2]/div[2]/div')
    logger.info(f"Found {len(games_list)} games listed")
    for game in games_list:
        game_name = game.text
        logger.info(f"Game: {game_name}")
except Exception as e:
    logger.error(f"Error extracting games list: {e}")
    driver.quit()

# Finally, close the driver
driver.quit()
logger.info("Driver closed")
