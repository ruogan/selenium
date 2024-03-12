import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def search_in_baidu(driver, str):
    driver.get("https://www.baidu.com")
    driver.find_element(By.ID, 'kw').send_keys(str)
    a = driver.find_element(By.ID, 'su')
    print(a)
    a.click()
    time.sleep(20)

def main():
    browser = webdriver.Chrome()
    search_in_baidu(browser, "123")
    browser.quit()

if __name__=="__main__":
    main()
