# -*-coding:utf-8-*-
import time

def delete_words_item(words_list, index):
    # words_remove = words_list[index]
    # words_list.remove(words_remove)
    words_list[index] = ''


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

        new_words_list = []
        for item in words_list:
            if len(item) is not 0:
                new_words_list.append(item)

        # 规则: 如果‘...’或‘.’或‘ ’前一位字符是其他字符，且字符串以数字结尾，则删除这些‘...’符号
        # 删除中间的符号 如：abc......123 ，这种情况下会把省略号全部删除
        # 如 1.2.3...abc 这种情况下，省略号不会被删除
        middle_to_delete = []
        # for i in range(len(new_words_list)):
        #     # 如果不是要删除的字符
        #     if new_words_list[i] not in delete_items:
        #         continue
        #     # 如果属于要删除的字符
        #     else:
        #         from_digit = False
        #         if not any(middle_to_delete):
        #             middle_to_delete.append(i)
        #         else:
        #             if i - middle_to_delete[len(middle_to_delete)-1] == 1:
        #                 middle_to_delete.append(i)
        #             else:
        #                 middle_to_delete.clear()
        #         # 从这个字符的后一位开始遍历
        #         for j in range(i+1, len(new_words_list)):
        #             # 如果是要删除的字符
        #             if new_words_list[j] in delete_items:
        #                 if not any(middle_to_delete):
        #                     middle_to_delete.append(i)
        #                 else:
        #                     if i - middle_to_delete[len(middle_to_delete) - 1] == 1:
        #                         middle_to_delete.append(i)
        #                     else:
        #                         middle_to_delete.clear()
        #             # 如果是数字
        #             elif new_words_list[j].isdigit():
        #                 from_digit = True
        #                 is_num_end = True
        #                 for k in range(j+1, len(new_words_list)):
        #                     if not new_words_list[k].isdigit():
        #                         is_num_end = False
        #                         break
        #             # 如果是其他字符
        #             else:
        #                 middle_to_delete.clear()
        #                 break
        #         if from_digit:
        #             if is_num_end:
        #                 for index in middle_to_delete:
        #                     delete_words_item(new_words_list, index)
        #                 break
        #             else:
        #                 middle_to_delete.clear()

        #  1.2.3 测试字符串 第一章 abc…………123
        index_cursor = 0
        # middle_delete_list = {}
        for i in range(len(new_words_list)):
            if i == 0:
                if new_words_list[i] in delete_items:
                    index_cursor = i
                    middle_to_delete.append(i)
            else:
                if new_words_list[i] in delete_items:
                    if not any(middle_to_delete):
                        middle_to_delete.append(i)
                    else:
                        if i - middle_to_delete[len(middle_to_delete) - 1] == 1:
                            middle_to_delete.append(i)
                        else:
                            middle_to_delete = [i]
                else:
                    if not new_words_list[i].isdigit():
                        index_cursor = i
                        middle_to_delete.clear()

        for index in middle_to_delete:
            delete_words_item(new_words_list, index)

    except Exception as ex:
        print("format_words exception imformation: %s; words: %s" % (ex, words))
    words = ''.join(new_words_list)
    return words


if __name__ == '__main__':
    words = "abc 1.2"
    new_words = list(words)
    start = time.time()
    # str_index = new_words.index("串")
    print("start: %s" % start)
    # for i in range(100):
    #     new_words.insert(str_index+i, '…')
    words = ''.join(new_words)
    middle = time.time()
    print("middle: %s" % middle)
    print("middle-start: %s" % (middle-start))
    new_words = format_words(words)
    end = time.time()
    print("end: %s" % end)
    print("end-middle: %s" % (end-middle))
    print(new_words)
