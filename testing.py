# 读取tranco的网站并自动化测试:
# 访问页面中的各个广告iframe元素的src url,并截图保存在对应文件夹中.
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
pic_num = 0


def get_landingpage_url(driver, element):
    original_handle = driver.current_window_handle
    original_handles = driver.window_handles

    try:
        print("click()")
        element.click()

    except:
        print("js_click()")
        driver.execute_script("arguments[0].click();", element)  # 使用 JavaScript 来执行点击操作

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
    print("landingpage handle: ", landing_page_handle)
    if landing_page_handle == None:
        print("no new tab after click")
        return None, None
    driver.switch_to.window(landing_page_handle)
    landing_page_url = driver.current_url
    landing_page_title = driver.title
    driver.close()
    print("switch to original")
    driver.switch_to.window(original_handle)
    return landing_page_url, landing_page_title


def mkdir(directory_path):  # 在指定路径创建文件夹.
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


# def visit_iframe_url(iframe_url):
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(options=options)
#     driver.get(iframe_url)
#     driver.maximize_window()
#
#     # 获取点击前标签页句柄
#     original_handle = driver.current_window_handle
#     original_handles = driver.window_handles
#     print("----------------------------")
#
#     # 打开新标签页
#     try:
#         iframe = driver.find_element(By.TAG_NAME, 'iframe')
#     except Exception as e:
#         print(f"in iframe url fail to find iframe element:{e}")
#         return None,None
#
#     iframe.click()
#
#     time.sleep(5)
#
#     # 获取点击后标签页的句柄
#     all_window_handles = driver.window_handles
#     # print(all_window_handles)
#
#     # 对比找到新标签页句柄
#     landing_page_handle = None
#     for handle in all_window_handles:
#         if handle not in original_handles:
#             landing_page_handle = handle
#             break
#     # 切换到新打开标签页
#     # print(driver.current_url)
#     driver.switch_to.window(landing_page_handle)
#     landing_page_url = driver.current_url
#     landing_page_title = driver.title
#     driver.close()
#     driver.switch_to.window(original_handle)
#     return landing_page_url,landing_page_title
#     # driver.quit()
#     # # driver.close()只能关闭当前句柄,driver.quit()能关闭全部句柄.

def test(id, page_url):
    global pic_num
    delete_data(PATH)
    # page_dir = f'./download/{id}'
    # mkdir(page_dir)

    options = webdriver.ChromeOptions()
    options.add_extension(r'F:\插件开发\workplace\test_3_7.crx')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(page_url)
    except Exception as e:
        print(f"Error accessing URL {check_url}: {e}")
        return
    driver.maximize_window()

    data = None
    j = 0
    while data == None:
        j += 1
        if j > 10:
            print("time out ")
            return
        time.sleep(5)
        data = read_data(PATH)
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

        # print_element(ad_element)

        def is_element_invisible(element):
            style = element.get_attribute("style")
            if "display: none;" in style or "visibility: hidden;" in style:
                return True
            else:
                return False

        if is_element_invisible(ad_element):
            print("元素不可见")
            continue
        # def get_element_size(element):
        #     try:
        #         size = element.size
        #         width = size['width']
        #         height = size['height']
        #         print(f"Element width: {width}px, height: {height}px")
        #     except Exception as e:
        #         print(f"Failed to get element size: {e}")
        # # 输出尺寸信息.
        # get_element_size(ad_element)

        print("=====================")
        # 新增内容:
        try:
            save_path = f"./test/{pic_num}.png"
            ad_element.screenshot(save_path)
            print(f"screenshot save in {save_path}")
            pic_num += 1
        except Exception as e:
            print(f"fail to save screenshot :{e}")
            return 1
        driver.switch_to.frame(ad_element)
        # 查找iframe内所有的<a>标签
        try:
            a_tag = driver.find_element(By.TAG_NAME, 'a')
            # print_element(a_tag)
            print('++++++++')
            landing_page_url, landing_page_title = get_landingpage_url(driver, a_tag)
            if landing_page_url == None:
                try:
                    os.remove(save_path)
                    pic_num -= 1
                    print(f"文件 \"{save_path}\" 已成功删除")
                except OSError as e:
                    print(f"无法删除文件 {save_path} - {e}")
                continue
            print(landing_page_url, '\n', landing_page_title)
            print(f"screenshot save in {save_path}")

            # 写入csv文件
            data_row = []
            data_row.append(id)
            data_row.append(save_path)
            data_row.append(landing_page_url)

            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data_row)
            print('++++++++')
        except Exception as e:
            print(f"error during visit <a :{e}")
            try:
                os.remove(save_path)
                pic_num -= 1
                print(f"文件 \"{save_path}\" 已成功删除")
            except OSError as e:
                print(f"无法删除文件 {save_path} - {e}")
            pass
        #
        # # 切换回主页面
        driver.switch_to.default_content()

    print("done")
    time.sleep(5000)
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


if __name__ == "__main__":
    test(1,
         "https://www.uol.com.br/tilt/noticias/redacao/2023/06/22/a-crise-de-semicondutores-poderia-ter-custado-a-democracia-brasileira.htm")

    # data2=read_data_csv(r"F:\插件开发\workplace\selenium\test\pythonProject\data\dataset_2.csv")
    # for i in range (0,len(data2)):
    #     print(f"{i+1}:{data2[i][1]}")
    #     page_url=data2[i][1]
    #     # page_url=f'https://www.{data2[i][1]}'
    #     test(i+1,page_url)

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
