# 访问页面中的各个广告iframe元素的src url,并截图保存在对应文件夹中.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os
from print_element import print_element
from screenshot import page_screenshot
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

PATH = r"C:\Users\ruogan\Downloads\ad_xpaths.json"


def mkdir(directory_path):# 在指定路径创建文件夹.
    try:
        os.makedirs(directory_path)
        print(f"文件夹 '{directory_path}' 创建成功")
        return True
    except OSError as e:
        print(f"创建文件夹 '{directory_path}' 失败: {e}")
        return False


def remove_prefix(url):  # 去除http://或者https://前缀
    if url.startswith("http://"):
        return url.replace("http://", "", 1)
    elif url.startswith("https://"):
        return url.replace("https://", "", 1)
    else:
        return url


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


def check_url(check_url):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(check_url)
        print(f"URL {check_url} is accessible")
        driver.quit()
        return True
    except Exception as e:
        print(f"Error accessing URL {check_url}: {e}")
        return False



if __name__ == "__main__":
    delete_data(PATH)
    page_url = 'https://www.sina.com.cn/'
    # save_path = r'./pics/test_screen.png'
    options = webdriver.ChromeOptions()
    options.add_extension(r'F:\插件开发\workplace\test_3_7.crx')
    driver = webdriver.Chrome(options=options)
    driver.get(page_url)
    driver.maximize_window()
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # slow_scroll_to_bottom(driver)
    time.sleep(20)


    # 读取iframe_urls
    iframe_urls = []
    data = read_data(PATH)
    for i in range(0, len(data)):
        xpath = data[i]
        print(f"----------------\n{i}:")
        # print(xpath)
        try:
            ad_element = driver.find_element(By.XPATH, xpath)
        except:
            print(f"fail to find xpath:{xpath}")
            continue
        print(f"xpath:{xpath}")
        print_element(ad_element)
        attributes = ad_element.get_property("attributes")
        for attribute in attributes:
            flag = 0
            if (attribute['name'] == 'src'):
                print(attribute['name'], ":", attribute['value'])
                print(attribute['value'])
                iframe_urls.append(attribute['value'])
                flag = 1
                break
        if (flag == 0):
            print("no src")

    # 去重
    unique_urls = []
    for url in iframe_urls:
        if url not in unique_urls:
            unique_urls.append(url)
    iframe_urls = unique_urls
    print("---------------")
    print(iframe_urls)
    print("---------------")

    # 新建网页对应目录
    new_url = remove_prefix(page_url)
    dir_url = './' + new_url
    mkdir(dir_url)
    # 测试是否能访问
    for i in range(len(iframe_urls)):
        url = iframe_urls[i]
        if url.startswith('javascript:'):
            print(f"not a URL: {url}")
            continue
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        if check_url(url):
            save_path = f"{dir_url}/{i}.png"
            page_screenshot(url, save_path)
    print("done")

    time.sleep(1000)
    delete_data(PATH)

    driver.close()
