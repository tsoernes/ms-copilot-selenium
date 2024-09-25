#!/usr/bin/env python

from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Path to your Edge WebDriver
edge_driver_path = Path.home() / ("bin/msedgedriver")
assert edge_driver_path.exists()

# Path to your Edge user data directory
# NOTE cannot have two Edge instances use the same directory at once.
edge_user_data_dir = Path.home() / ".config/microsoft-edge-beta-selenium"

# Initialize the WebDriver with your Edge profile
options = webdriver.EdgeOptions()
options.add_argument(f"user-data-dir={edge_user_data_dir}")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

# Create a Service object
service = Service(executable_path=str(edge_driver_path))


# Initialize the Edge WebDriver with the service object
driver = webdriver.Edge(service=service, options=options)

# Open the Microsoft Copilot login page
driver.get("https://copilot.microsoft.com")

# Ask a question to Copilot
question = "Why do people fly in their dreams?"

# Locate the shadow host element
shadow_host1 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "cib-serp-main"))
)

# Access the shadow root
shadow_root1 = driver.execute_script("return arguments[0].shadowRoot", shadow_host1)

# Continue inwards until we get the input element
shadow_host2 = shadow_root1.find_element(By.CSS_SELECTOR, "#cib-action-bar-main")
shadow_root2 = driver.execute_script("return arguments[0].shadowRoot", shadow_host2)
shadow_host3 = shadow_root2.find_element(
    By.CSS_SELECTOR, "div > div.main-container > div > div.input-row > cib-text-input"
)
shadow_root3 = driver.execute_script("return arguments[0].shadowRoot", shadow_host3)
text_input_sel = "#searchboxform > label"
input_el = shadow_root3.find_element(By.CSS_SELECTOR, text_input_sel)

input_el.send_keys(question)
input_el.send_keys(Keys.ENTER)

shadow_host4 = shadow_root1.find_element(By.ID, "cib-conversation-main")
shadow_root4 = driver.execute_script("return arguments[0].shadowRoot", shadow_host4)

shadow_hosts5 = shadow_root4.find_elements(
    By.CSS_SELECTOR, "#cib-chat-main > cib-chat-turn"
)
shadow_roots5 = [
    driver.execute_script("return arguments[0].shadowRoot", sh5)
    for sh5 in shadow_hosts5
]

shadow_hosts6 = [
    sr5.find_elements(By.CSS_SELECTOR, "cib-message-group") for sr5 in shadow_roots5
]
shadow_hosts6 = [sh for shs in shadow_hosts6 for sh in shs]
shadow_roots6 = [
    driver.execute_script("return arguments[0].shadowRoot", sh6)
    for sh6 in shadow_hosts6
]

message_els = [
    sr6.find_element(By.CSS_SELECTOR, "cib-message") for sr6 in shadow_roots6
]
messages = [el.get_attribute("aria-label") for el in message_els]

messages_with_links = []
# Find links
for message, message_el in zip(messages, message_els):
    shadow_root7 = driver.execute_script("return arguments[0].shadowRoot", message_el)
    try:
        shadow_host8 = shadow_root7.find_element(
            By.CSS_SELECTOR, "cib-message-attributions"
        )
    except NoSuchElementException:
        # Message without attributions at the bottom
        messages_with_links.append(message)
        continue

    shadow_root8 = driver.execute_script("return arguments[0].shadowRoot", shadow_host8)
    shadow_hosts9 = shadow_root8.find_elements(
        By.CSS_SELECTOR, "div > div.attribution-container > div > cib-attribution-item"
    )
    shadow_roots10 = [
        driver.execute_script("return arguments[0].shadowRoot", sh)
        for sh in shadow_hosts9
    ]
    link_els = [sr.find_element(By.CSS_SELECTOR, "a") for sr in shadow_roots10]
    links = "\n".join(
        [
            f"[{el.get_attribute('aria-label')}]({el.get_attribute('href')})"
            for el in link_els
        ]
    )

    message_with_links = message + "\n" + links if links else message
    messages_with_links.append(message_with_links)

conversation = "\n\n".join(messages_with_links)

print(conversation)
