# 打开一个iframe的src url,模拟点击iframe,找寻新出现的句柄,转换到对应句柄,输出url.
# 暂时弃用.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from screenshot import page_screenshot


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
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
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


if __name__ == "__main__":
    iframe_url = 'https://mjs.sinaimg.cn/wap/custom_html/wap/20220705/62c3b4353cb3e.html'
    landing_page_url,landing_page_title = visit_iframe_url(iframe_url)
    page_screenshot(iframe_url,'./test/test.png')
    print(landing_page_url,'\n',landing_page_title)
    time.sleep(100)
