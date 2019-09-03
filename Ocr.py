# -*-coding:utf-8-*-

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
        print("open img failed %s" % ex)
        return None


def delete_words_item(words_list, index):
    # words_remove = words_list[index]
    # words_list.remove(words_remove)
    words_list[index] = ''


# 删除字符串头部和尾部的.......符号
def format_words(words):
    try:
        if len(words) == 0:
            return words
        words_list = list(words)
        # print(words_list)
        # 正序（头部）
        delete_index = []
        delete_items = ['.', ' ', '…']
        # 正序遍历字符串数组，符合删除条件的，将索引存入delete_index
        for index in range(len(words_list)):
            if words_list[index] in delete_items:
                delete_index.append(index)
        # print(delete_index)
        # 如果delete_index的第一位等于字符串数组的第一位，则遍历delete_index
        if len(delete_index) >= 1:
            if delete_index[0] == 0:
                for index in range(len(delete_index)):
                    if index == 0:
                        delete_words_item(words_list, delete_index[index])
                    else:
                        # 如果索引连续，则删除，否则跳出循环
                        if delete_index[index] - delete_index[index - 1] == 1:
                            delete_words_item(words_list, delete_index[index])
                        else:
                            break
        # 倒序（尾部）
        # 倒序遍历整个字符串数组，记录下所有需删除的符号的索引
        if len(words_list) == 0:
            return ''
        reverse_delete_index = []
        for index in range(len(words_list) - 1, -1, -1):
            if words_list[index] in delete_items:
                reverse_delete_index.append(index)
        # print(reverse_delete_index)
        # 如果reverse_delete_index的最大值为字符串最后一位下标，则遍历reverse_delete_index
        if len(reverse_delete_index) >= 1:
            if reverse_delete_index[0] == len(words_list) - 1:
                for index in range(len(reverse_delete_index)):
                    if index == 0:
                        delete_words_item(words_list, reverse_delete_index[index])
                    else:
                        # 如果下标号连续，则删除，否则跳出循环
                        if reverse_delete_index[index - 1] - reverse_delete_index[index] == 1:
                            delete_words_item(words_list, reverse_delete_index[index])
                        else:
                            break
    except Exception as ex:
        print("format_words exception imformation: %s; words: %s" % (ex, words))
    words = ''.join(words_list)
    return words


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
            words = format_words(list["words"])  # 格式化字符串
            # words = list["words"]
            height = list["location"]["top"]
            data = {"words": words, "top": height}
            ocr_result.append(data)
        print(img_name + "   finished")
    except Exception as ex:
        print("get_file_ocr exception imformation: %s" % ex)


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
        with open(txt_path, "w") as f:
            length = len(ocr_result)
            for index in range(length):
                # 判断两个string在原pdf文件中，是否在同一行
                if index > 1:
                    if abs(ocr_result[index - 1]["top"] - ocr_result[index]["top"]) <= 10:
                        f.write("  " + ocr_result[index]["words"])
                    else:
                        f.write("\n" + ocr_result[index]["words"])
                else:
                    f.write(ocr_result[index]["words"])

    except Exception as ex:
        print("recognize_my_picture failed %s" % ex)


if __name__ == '__main__':
    """ 你的 APPID AK SK """
    APP_ID = '17130574'
    API_KEY = 'eMzx7UaG6BrEFRkzFQbuS7Bm'
    SECRET_KEY = 'wWSlbzm4B0heD6uInZvIqtmvKPjcqDYD'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    file_path = "C:\\git\\baidu_ocr\\assets\\img\\"
    recognize_my_picture()
