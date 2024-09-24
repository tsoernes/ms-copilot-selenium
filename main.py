#!/usr/bin/env python

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Path to your Edge WebDriver
edge_driver_path = Path.home() / ("bin/msedgedriver")
assert edge_driver_path.exists()
#
# Path to your Edge user data directory
edge_user_data_dir = Path.home() / ".config/microsoft-edge-beta"
assert edge_user_data_dir.exists()

# Initialize the WebDriver with your Edge profile
options = webdriver.EdgeOptions()
options.add_argument(f"user-data-dir={edge_user_data_dir}")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

# Create a Service object
service = Service(executable_path=edge_driver_path)

# NOTE does not work when there's already an existing Edge instance running.

# Initialize the Edge WebDriver with the service object
driver = webdriver.Edge(service=service, options=options)

# Open the Microsoft Copilot login page
driver.get("https://copilot.microsoft.com")

# Wait for the login page to load and find the username field
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "loginfmt")))

# Enter the username
username = driver.find_element(By.NAME, "loginfmt")
username.send_keys("your_email@example.com")
username.send_keys(Keys.RETURN)

# Wait for the password field to load and enter the password
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "passwd")))
password = driver.find_element(By.NAME, "passwd")
password.send_keys("your_password")
password.send_keys(Keys.RETURN)

# Handle any additional authentication steps if necessary
# For example, handling MFA (Multi-Factor Authentication) prompts

# Wait for the login process to complete
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "copilot-dashboard"))
)

print("Logged in successfully!")

# Close the browser
driver.quit()
