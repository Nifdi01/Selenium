from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Initialize an empty list to store the scraped data
data_list = []

with open('data.json', 'w') as f:
    json.dump([], f)


def write_json(new_data, filename='data.json'):
    """Writes information to the json file

    Args:
        new_data (_type_): _description_
        filename (str, optional): _description_. Defaults to 'data.json'.
    """
    
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

browser = webdriver.Firefox()
browser.get("https://www.amazon.com/laptop/s?k=laptop")

isNextDisabled = False

while not isNextDisabled:
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")))
        next_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "s-pagination-next")))
        elem_list = browser.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")
        
        items = elem_list.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        
        for item in items:
            title = item.find_element(By.TAG_NAME, 'h2').text
            price = "None"
            img = "None"
            rating = "None"
            link = "None"
            
            try:
                price = item.find_element(By.CLASS_NAME, 'a-price').text.replace("\n", ",")
                img = item.find_element(By.CLASS_NAME, 's-image').get_attribute('src')
                rating = item.find_element(By.CSS_SELECTOR, 'div.a-row.a-size-small > span:nth-child(1)').get_attribute('aria-label').split(' ')[0]
                link = item.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('href')
            except:
                pass

            write_json({
                'title': title,
                'image': img,
                'price': price,
                'rating': rating,
                'link': link
            })
        
        next_class = next_btn.get_attribute('class')
        if 's-pagination-disabled' in next_class:
            isNextDisabled = True
        else:
            browser.find_element(By.CLASS_NAME, "s-pagination-next").click()

    except Exception as e:
        print(e, "Main Error")
        isNextDisabled = True

browser.quit()
