from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebAutomation:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)

    def open(self, url):
        self.driver.get(url)

    def click(self, element_id):
        element = self.wait.until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        element.click()

    def close(self):
        self.driver.quit()


# -----------------------------
# Example
# -----------------------------

browser = WebAutomation()

browser.open("https://amazon.com")

browser.click("a-page")

# browser.close()