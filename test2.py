# 打开一个iframe的src url,模拟点击iframe,找寻新出现的句柄,转换到对应句柄,输出url.

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == "__main__":
    page_url = 'https://mjs.sinaimg.cn/wap/custom_html/wap/20220705/62c3b4353cb3e.html'

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(page_url)
    driver.maximize_window()

    # 获取点击前标签页句柄
    main_window_handle = driver.current_window_handle
    print(main_window_handle)
    print("----------------------------")

    # 打开新标签页
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    iframe.click()

    time.sleep(5)

    # 获取点击后标签页的句柄
    all_window_handles = driver.window_handles
    print(all_window_handles)

    # 对比找到新标签页句柄
    new_window_handle = None
    for handle in all_window_handles:
        if handle != main_window_handle:
            new_window_handle = handle
            break

    # 切换到新打开标签页
    print(driver.current_url)
    driver.switch_to.window(new_window_handle)
    print(driver.current_url)

    driver.quit()
    # driver.close()只能关闭当前句柄,driver.quit()能关闭全部句柄.
