from aip import AipOcr
import json
import os
import os.path

ocr_result = []


def get_image(img_path):
    try:
        with open(img_path, 'rb') as fp:
            return fp.read()
    except Exception as ex:
        print("open img failed %s" %ex)
        return None


def get_file_ocr(img_path, img_name):
    try:
        img = get_image(img_path)
        print("dealing with " + img_name + "...")
        if img is not None:
            result = client.basicAccurate(img)
        else:
            return
        result_lists = result["words_result"]
        for list in result_lists:
            words = list["words"]
            ocr_result.append(words)
        print(img_name + "finished")
    except Exception as ex:
        print("get_file_ocr exception imformation: %s" %ex)


def recognize_my_picture():
    try:
        files = os.listdir(file_path)
        for file in files:
            img_path = file_path + file
            get_file_ocr(img_path, file)
        txt_path = "%sresult.txt" % file_path
        with open(txt_path,"w") as f:
            for info in ocr_result:
                # print(info)
                f.write(info)
    except Exception as ex:
        print("recognize_my_picture failed %s" %ex)


if __name__ == '__main__':
    """ 你的 APPID AK SK """
    APP_ID = '17130574'
    API_KEY = 'eMzx7UaG6BrEFRkzFQbuS7Bm'
    SECRET_KEY = 'wWSlbzm4B0heD6uInZvIqtmvKPjcqDYD'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    file_path = "C:\\git\\baidu_ocr\\assets\\img\\"
    recognize_my_picture()
