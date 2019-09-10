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


def append_delete_list(middle_to_delete, index):
    if not any(middle_to_delete):
        middle_to_delete.append(index)
    else:
        if index - middle_to_delete[len(middle_to_delete) - 1] == 1:
            middle_to_delete.append(index)
        else:
            middle_to_delete = [index]
    return middle_to_delete


# 删除字符串头部的所有空格，逗号及省略号
# 例：'...1.2.3 abc456' 格式化后变为 '1.2.3 abc456'
def format_head(words_list, delete_items):
    if len(words_list) == 0:
        return words_list
    # 正序（头部）
    delete_index = []
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
    return words_list


# 删除字符串尾部的所有空格，逗号及省略号
# 例：'1.2.3 abc...' 格式化后变为 '1.2.3 abc'
def format_tail(words_list, delete_items):
    if len(words_list) == 0:
        return words_list
    # 倒序（尾部）
    # 倒序遍历整个字符串数组，记录下所有需删除的符号的索引
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
    return words_list


# 规则: 字符串如果以数字结尾，则把与这些数字相邻的标点符号全部删除
# 例1：1.2.3 abc......123 ，这种情况下会把与结尾的123相邻的省略号全部删除，而保留1.2.3中的省略号
# 例2  1.2.3...abc 这种情况下，不会有任何符号被删除
def format_middle_old(new_words_list, delete_items):
    if len(new_words_list) == 0:
        return new_words_list
    middle_to_delete = []
    for i in range(len(new_words_list)):
        # 如果不是要删除的字符
        if new_words_list[i] not in delete_items:
            continue
        # 如果属于要删除的字符
        else:
            middle_to_delete = append_delete_list(middle_to_delete, i)
            # 从这个字符的后一位开始遍历
            for j in range(i + 1, len(new_words_list)):
                from_digit = False
                # 如果是要删除的字符
                if new_words_list[j] in delete_items:
                    middle_to_delete = append_delete_list(middle_to_delete, j)
                # 如果是数字
                elif new_words_list[j].isdigit():
                    from_digit = True
                    is_num_end = False
                    has_other_words = filter(lambda x: not new_words_list[x].isdigit(),
                                             range(j + 1, len(new_words_list)))
                    if not any(has_other_words):
                        is_num_end = True
                        break
                # 如果是其他字符
                else:
                    middle_to_delete.clear()
                    break
            if from_digit:
                if is_num_end:
                    if any(middle_to_delete):
                        if len(middle_to_delete) == 1:
                            if new_words_list[middle_to_delete[0]] == '…':
                                delete_words_item(new_words_list, middle_to_delete[0])
                        else:
                            for index in middle_to_delete:
                                delete_words_item(new_words_list, index)
                    break
                else:
                    middle_to_delete.clear()
    return new_words_list


# 规则: 字符串如果以数字结尾，则把与这些数字相邻的标点符号全部删除
# 例1：1.2.3 abc......123 ，这种情况下会把与结尾的123相邻的省略号全部删除，而保留1.2.3中的省略号
# 例2：1.2.3...abc 这种情况下，不会有任何符号被删除
def format_middle_new(new_words_list, delete_items):
    if len(new_words_list) == 0:
        return new_words_list
    middle_to_delete = []
    for i in range(len(new_words_list)):
        if i == 0:
            if new_words_list[i] in delete_items:
                middle_to_delete.append(i)
        else:
            if new_words_list[i] in delete_items:
                middle_to_delete = append_delete_list(middle_to_delete, i)
            else:
                if not new_words_list[i].isdigit():
                    middle_to_delete.clear()

    if any(middle_to_delete):
        if len(middle_to_delete) == 1:
            if new_words_list[middle_to_delete[0]] == '…':
                delete_words_item(new_words_list, middle_to_delete[0])
        else:
            for index in middle_to_delete:
                delete_words_item(new_words_list, index)
    return new_words_list


def format_words(words):
    delete_items = ['.', ' ', '…']
    try:
        if len(words) == 0:
            return words
        words_list = list(words)
        # print(words_list)
        # 正序（头部）
        words_list = format_head(words_list, delete_items)
        # 倒序（尾部）
        words_list = format_tail(words_list, delete_items)
        new_words_list = []
        for item in words_list:
            if len(item) is not 0:
                new_words_list.append(item)

        # new_words_list = format_middle_old(new_words_list, delete_items)
        # 中间
        new_words_list = format_middle_new(new_words_list, delete_items)

    except Exception as ex:
        print("format_words exception imformation: %s; words: %s" % (ex, words))
    words = ''.join(new_words_list)
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
        # print(result_lists)
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
                img_name = file
                get_file_ocr(img_path, img_name)
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
    with open("config.json", 'r') as conf:
        load_dict = json.load(conf)
        APP_ID = load_dict['APP_ID']
        API_KEY = load_dict['API_KEY']
        SECRET_KEY = load_dict['SECRET_KEY']
        file_path = load_dict['FILE_PATH']
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    recognize_my_picture()
