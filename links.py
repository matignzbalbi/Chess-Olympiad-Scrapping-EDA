from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time 
import csv

chrome_options = Options()
chrome_options.add_experimental_option("detach", True) 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.chess.com/events/2024-fide-chess-olympiad-open/dashboard/11/Fedoseev_Vladimir-Gukesh_D")
time.sleep(5)

select = driver.find_element(By.CLASS_NAME, "cc-select-component.cc-select-large.dashboard-game-header-select")

select.click()

options = select.find_elements(By.TAG_NAME, "option")

links = []

for option in options:
    option.click()
    time.sleep(1)
    current_url = driver.current_url
    links.append(current_url)
    print(f"Link: {current_url}, agregado")

with open (r"round11.csv", 'w', newline='') as f:

    write = csv.writer(f)
    
    for link in links:
        write.writerow([link])

driver.quit
