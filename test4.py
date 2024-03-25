# 读取tranco的网站并自动化测试:
# 访问页面中的各个广告iframe元素的src url,并截图保存在对应文件夹中.
# 暂时弃用.效果不好.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import csv
import os
from print_element import print_element
from screenshot import page_screenshot
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

PATH = r"C:\Users\ruogan\Downloads\ad_xpaths.json"
csv_file_path = './data.csv'

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
        return None


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

def visit_iframe_url(iframe_url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(iframe_url)
    driver.maximize_window()

    # 获取点击前标签页句柄
    original_handle = driver.current_window_handle
    original_handles = driver.window_handles
    print("----------------------------")

    # 打开新标签页
    try:
        iframe = driver.find_element(By.TAG_NAME, 'iframe')
    except Exception as e:
        print(f"in iframe url fail to find iframe element:{e}")
        return None,None

    iframe.click()

    time.sleep(5)

    # 获取点击后标签页的句柄
    all_window_handles = driver.window_handles
    # print(all_window_handles)

    # 对比找到新标签页句柄
    landing_page_handle = None
    for handle in all_window_handles:
        if handle not in original_handles:
            landing_page_handle = handle
            break

    # 切换到新打开标签页
    # print(driver.current_url)
    driver.switch_to.window(landing_page_handle)
    landing_page_url = driver.current_url
    landing_page_title = driver.title
    driver.close()
    driver.switch_to.window(original_handle)
    return landing_page_url,landing_page_title
    driver.quit()
    # # driver.close()只能关闭当前句柄,driver.quit()能关闭全部句柄.

def test(id,page_url):
    delete_data(PATH)

    page_dir = f'./download/{id}'
    mkdir(page_dir)

    # page_url = 'https://www.sina.com.cn/'
    # save_path = r'./pics/test_screen.png'
    options = webdriver.ChromeOptions()
    options.add_extension(r'F:\插件开发\workplace\test_3_7.crx')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(page_url)
    except Exception as e:
        print(f"Error accessing URL {check_url}: {e}")
        return
    driver.maximize_window()
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # slow_scroll_to_bottom(driver)

    # 读取iframe_urls
    iframe_urls = []
    data = None
    j=0
    while data==None:
        j+=1
        if j>10:
            print("time out ")
            return
        time.sleep(5)
        data=read_data(PATH)
        print("no data..wait..")
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

    # 测试是否能访问
    for i in range(len(iframe_urls)):
        url = iframe_urls[i]
        if url.startswith('javascript:'):
            print(f"not a URL: {url}")
            continue
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        if check_url(url):
            iframe_pic_dir=f'{page_dir}/{id}.png'
            landing_page_url, landing_page_title = visit_iframe_url(url)
            if(landing_page_url == None or landing_page_title == None):
                continue
            page_screenshot(url, iframe_pic_dir)
            print(landing_page_url, '\n', landing_page_title)
            data_row = []
            data_row.append(id)
            data_row.append(page_url)
            data_row.append(landing_page_url)
            data_row.append(iframe_pic_dir)
            data_row.append(landing_page_title)
            # 将数据行追加到 CSV 文件
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data_row)

    print("done")

    time.sleep(5)
    delete_data(PATH)

    driver.close()
def read_data_csv(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = [row for row in reader]
        return data
    except Exception as e:
        print(f"Failed to read CSV data from {path}: {e}")
        return None


data2=read_data_csv(r"F:\插件开发\workplace\selenium\test\pythonProject\data\dataset_2.csv")
for i in range (0,len(data2)):
    print(f"{i+1}:{data2[i][1]}")
    page_url=data2[i][1]
    # page_url=f'https://www.{data2[i][1]}'
    test(i+1,page_url)

# data_row=[]
# data_row.append('John')
# data_row.append('30')
# data_row.append('New York')
# # 指定 CSV 文件路径
# # 将数据行追加到 CSV 文件
# with open(csv_file_path, mode='a', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(data_row)
#
# print("数据已成功追加到 CSV 文件！")
