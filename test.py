from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os
from print_element import print_element

PATH = r"C:\Users\ruogan\Downloads\ad_xpaths.json"
def delete_data(path):
    try:
        os.remove(path)
        print(f"\"{path}\" 已成功删除")
        return 1
    except OSError as e:
        print(f"!#!Fail to delete {path} - {e}")
        return 0

def read_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # for i in range(0, len(data)):
        #     xpath = data[i]
        #     print(xpath)
        return data
    except Exception as e:
        print(f"!#!Fail to open {path} - {e}")
        return 0

if __name__=="__main__":
    delete_data(PATH)
    page_url = 'https://www.sina.com.cn'
    save_path = r'./pics/test_screen.png'
    options = webdriver.ChromeOptions()
    options.add_extension(r'F:\插件开发\workplace\test.crx')
    driver = webdriver.Chrome(options=options)
    driver.get(page_url)
    time.sleep(20)

    data=read_data(PATH)
    for i in range(0, len(data)):
        xpath = data[i]
        # print(xpath)
        print(f"----------------\n{i}:")
        ad_element = driver.find_element(By.XPATH, xpath)
        print_element(ad_element)
    time.sleep(40)
    delete_data(PATH)


    driver.close()