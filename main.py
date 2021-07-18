import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSeN4ohdh5wbIyWlH8-Iuv-eUjalKBr0ZW0cdYrfdSJOinFRKA/viewform?usp" \
            "=sf_link "
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
              "%22mapBounds%22%3A%7B%22west%22%3A-122.76830289734521%2C%22east%22%3A-122.22859952820458%2C%22south%22" \
              "%3A37.52893563750139%2C%22north%22%3A37.84767897962086%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22" \
              "%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22" \
              "%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B" \
              "%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C" \
              "%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B" \
              "%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D "

headers_zillow = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US",
}
response = requests.get(ZILLOW_LINK, headers=headers_zillow)
content = response.text

soup = BeautifulSoup(content, "html.parser")
price_code = soup.find_all(class_="list-card-price")
price = []
for each_element in price_code:
    element = each_element.getText()
    element_list = element.split('$')
    element1 = element_list[1]
    element2 = element1[:5]
    element_list2 = element2.split(",")
    final_element = int(element_list2[0]+element_list2[1])
    price.append(final_element)
address_code = soup.find_all(name="address")
address_list = [address.text for address in address_code]
link_code = soup.find_all(class_="list-card-link")
links = [link.get("href") for link in link_code]

for i in range(0, len(address_list)):
    chrome_driver_path = "D:/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(FORM_LINK)
    time.sleep(4)
    input1 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                          '1]/div/div[1]/input')
    input1.send_keys(address_list[i])
    input2 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                          '1]/div/div[1]/input')
    input2.send_keys(price[i])
    input3 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                          '1]/div/div[1]/input')
    input3.send_keys(links[i])
    button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    button.click()
    time.sleep(2)
    driver.quit()
