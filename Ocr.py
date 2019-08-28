#-*-coding:utf-8-*-

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
            result = client.accurate(img)
        else:
            return
        result_lists = result["words_result"]
        for list in result_lists:
            words = list["words"]
            height = list["location"]["top"]
            data = {"words":words,"top":height}
            ocr_result.append(data)
        print(img_name + "finished")
    except Exception as ex:
        print("get_file_ocr exception imformation: %s" %ex)


def recognize_my_picture():
    try:
        files = os.listdir(file_path)
        for file in files:
            img_path = file_path + file
            if os.path.isdir(img_path):
                continue
            file_type = file.split('.')[1].lower()
            type_list = ["jpg", "png", "img"]
            if file_type in type_list:
                # img_path = file_path + file
                get_file_ocr(img_path, file)
        txt_path = "%sresult.txt" % file_path
        with open(txt_path,"w") as f:
            length = len(ocr_result)
            for index in range(length):
                # 判断两个string在原pdf文件中，是否在同一行
                if index > 1:
                    if abs(ocr_result[index-1]["top"] - ocr_result[index]["top"]) <= 10:
                        f.write("  " + ocr_result[index]["words"])
                    else:
                        f.write("\n" + ocr_result[index]["words"])
                else:
                    f.write(ocr_result[index]["words"])

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
