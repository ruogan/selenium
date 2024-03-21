from selenium import webdriver

# 创建 WebDriver 实例
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.example.com")

# 定位到需要截图的元素
element = driver.find_element_by_xpath("//div[@id='example']")

# 对元素进行截图
element.screenshot("element_screenshot.png")

# 关闭 WebDriver 实例
driver.quit()
