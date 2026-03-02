from selenium import webdriver
import os
import subprocess
import shutil

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def _find_chrome_executable():
    common_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return shutil.which("chrome")


def _start_chrome_debug_session():
    chrome_executable = _find_chrome_executable()
    if not chrome_executable:
        raise FileNotFoundError("Chrome executable not found. Please install Google Chrome.")

    os.makedirs(r"C:\chromedata\debugger", exist_ok=True)
    subprocess.Popen([
        chrome_executable,
        "--remote-debugging-port=9222",
        r"--user-data-dir=C:\chromedata\debugger",
    ])


_start_chrome_debug_session()

class Browser:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("debuggerAddress", "localhost:9222")
        self.driver = webdriver.Chrome(options=self.options)
        self.likeButton = None
        self.dislikeButton = None


    def likeVideo(self):
        try:
            if self.checkButtonsDefined() and self.likeButton.get_attribute("aria-pressed") == "false":
                self.likeButton.click()
        except ElementNotInteractableException:
            print("not interactable")

    def dislikeVideo(self):
        try:
            if self.checkButtonsDefined() and self.dislikeButton.get_attribute("aria-pressed") == "false":
                self.dislikeButton.click()
        except ElementNotInteractableException:
            print("not interactable")


    def defineButtons(self):
        self.likeButton = self.driver.find_element(By.CSS_SELECTOR, "div.style-scope.ytd-video-primary-info-renderer div div#menu-container div#menu button")
        self.dislikeButton = self.driver.find_element(By.CSS_SELECTOR, "div.style-scope.ytd-video-primary-info-renderer div div#menu-container div#menu ytd-toggle-button-renderer:nth-child(2) button")


    def checkButtonExists(self):
        if "watch" in self.driver.current_url:
            try:
                self.driver.find_element(By.CSS_SELECTOR, "div.style-scope.ytd-video-primary-info-renderer div div#menu-container div#menu button")
            except NoSuchElementException:
                return False
            return True

    def checkButtonsDefined(self):
        return self.likeButton is not None and self.dislikeButton is not None