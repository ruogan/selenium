from selenium import webdriver
from selenium.webdriver.common.by import By
import print_element
from selenium.webdriver.common.keys import Keys
import time
import sys

DEBUG=0
def youdao_translate(str):
    # 加载浏览器驱动
    driver = webdriver.Chrome()

    # 加载有道翻译页面
    driver.get("https://fanyi.youdao.com/")
    time.sleep(1)
    # 点击关闭广告
    try:
        ad_close_button = driver.find_element(By.XPATH, "/html/body/div[5]/div/img[2]")
        ad_close_button.click()
    except:
        print("no ad")
        pass
    # 点击选择文本翻译按钮
    try:
        wenben_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]')
        wenben_button.click()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # print("异常类型:", exc_type)
        print(exc_value)
        # print("回溯对象:", exc_traceback)
        time.sleep(100)
        sys.exit(1)

    # 选择输入框并输入"hello"
    input_div = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div")
    input_div.click()
    input_div.send_keys(str)
    if DEBUG:
        print_element.print_element(input_div)
    time.sleep(5)
    output_div = driver.find_element(By.XPATH,
                                     "/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div[3]/div[2]/div[1]")
    if DEBUG:
        print_element.print_element(output_div)
    output_text=output_div.text
    print(output_text)
    # time.sleep(100)
    driver.quit()
    return output_text

if __name__=="__main__":
    youdao_translate("How do you do?")
