from selenium import webdriver
import time


def page_screenshot(page_url, save_path):  # 输入url和保存路径,将url对应的网页截图存储到对应路径.

    # 配置 Chrome 开启的模式，headless是无界面模式,否则截不了全页面，只能截到你电脑的高度
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(page_url)
    time.sleep(1)

    # 获取页面的宽高,将浏览器的宽高设置成刚刚获取的宽高
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width, height)
    time.sleep(1)

    # 截图并关闭浏览器
    driver.save_screenshot(save_path)
    print(f"successfully save page {page_url} in {save_path}!")
    driver.close()


# class MyPage(object):
#     def __init__(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get('https://www.sina.com.cn/')
#
#     def test_screen(self):
#         self.driver.get_screenshot_as_file("test_baidu2.png")
#
#     def teardown(self):
#         self.driver.quit()
#

if __name__ == '__main__':
    # start_time = time.time()

    url = 'https://www.sina.com.cn'
    pic_name = r'./pics/test_screen.png'
    page_screenshot(page_url=url, save_path=pic_name)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"the script took {execution_time:.2f}s to execute")
    exit(0)
