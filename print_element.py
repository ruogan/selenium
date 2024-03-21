def print_element(input):# 输入一个查找返回的remote webelement,输出元素的tagname,text,以及全部属性.

    attributes = input.get_property("attributes")
    print("tagname:",input.tag_name)
    print("text:",input.text)
    # try:
    #     print("text:",input.text)
    # except:
    #     print("text:","none")
    for attribute in attributes:
        print(f"{attribute['name']}:{attribute['value']}")