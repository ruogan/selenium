import json
import os

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
        for i in range(0, len(data)):
            xpath = data[i]
            print(xpath)
            return 1
    except Exception as e:
        print(f"!#!Fail to open {path} - {e}")
        return 0

if __name__ =="__main__":
    PATH = r"C:\Users\ruogan\Downloads\ad_xpaths.json"
    read_data(PATH)
    # delete_data(PATH)