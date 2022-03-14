import pandas as pd
from bs4 import BeautifulSoup
import requests
import selenium
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options
        )
driver.get("https://cpj.org/data/killed")

list_of_rows = []
counter = 0
while counter < 100:
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"table js-report-builder-table"})
    for row in table.find_all('tr'):
        list_of_cells = []
        for cell in row.find_all('td'):
            if cell.find('a'):
                list_of_cells.append(cell.find('a')['href'])
            text = cell.text.strip()
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    counter = counter + 1
    next_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[1]/div/nav/ul/li[8]/a')
    next_button.click()
    time.sleep(1)
    
data = pd.DataFrame(list_of_rows, columns=["link","name", "organization", "date", "location","killed","type_of_death", ""]).dropna().drop_duplicates()

data.to_csv("data.csv",index=False)
