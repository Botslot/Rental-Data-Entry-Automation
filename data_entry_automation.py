import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# ----------------------------------BEAUTIFULSOUP--------------------------------------
links = []
prices= []
locations = []

SHEET_URL = "https://forms.gle/zBMqwVJm4zocyrXt9"
Url = "https://appbrewery.github.io/Zillow-Clone/"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}
response = requests.get(Url, headers=HEADER)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
all_links = soup.find_all(name="a",class_ ="StyledPropertyCardDataArea-anchor")
for link in all_links:
    href = link.get("href")
    if "https://www.zillow.com" in href:
        links.append(href)
    else:
        full_link = f"https://www.zillow.com{href}"
        links.append(full_link)
all_prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
for price in all_prices:
    new_price = price.get_text().strip()
    prices.append(new_price.split("+")[0].split("/")[0])
all_locations = soup.find_all(name="address")
for location in all_locations:
    loc = location.get_text().strip()
    loc = loc.replace("|", " ")
    parts = loc.split(",")
    if len(parts) > 2:
        first = parts[0]
        second = parts[1]

        if " ".join(first.split()[:2]) in " ".join(second.split()[:2]):
            loc = ",".join(parts[1:])

        elif "  " in loc:
            loc = loc.split("  ")[-1].strip()
    locations.append(loc)
#------------------------------------SELENIUM------------------------------------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get(SHEET_URL)
driver.implicitly_wait(2)
for n in range(len(links)):
    link = links[n]
    price = prices[n]
    location = locations[n]
    input_address = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    input_price = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    input_link = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    input_address.send_keys(location)
    input_price.send_keys(price)
    input_link.send_keys(link)
    submit_button = driver.find_element(By.CLASS_NAME,"NPEfkd")
    submit_button.click()
    wait = WebDriverWait(driver, 1)
    if n < len(links) - 1:
        another_response =wait.until(ec.element_to_be_clickable((By.LINK_TEXT,"Submit another response")))
        another_response.click()


