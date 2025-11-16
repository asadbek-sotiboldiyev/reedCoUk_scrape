from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select


def applytimerange(driver):
    dropdown  = driver.find_element(By.NAME, 'dateCreatedOffSet')
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", dropdown)
    select = Select(dropdown)
    select.select_by_index(1)
    #1 = last day
    #2 last 3 days
    #3 last week
    #4 last 2 weeks
    
def searching(driver, keyword):
    keywordfield = driver.find_element(By.CSS_SELECTOR, '#__next > form > div > div.row > div:nth-child(1) > div > input')
    locationfield = driver.find_element(By.CSS_SELECTOR, '#__next > form > div > div.row > div:nth-child(2) > div > input')
    keywordfield.clear()
    keywordfield.send_keys(keyword)
    locationfield.clear()
    locationfield.send_keys('United Kingdom', Keys.ENTER)


