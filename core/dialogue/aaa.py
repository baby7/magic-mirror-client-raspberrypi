import random
# 首先判断是否为指令
# 不是指令的话判断是否为信息查询
# 不是信息查询进行语料库匹配
# 语料库未匹配进行图灵聊天


# 敏感词判断
def filter_words(ask, answer):
    for i in filtered_words_list:
        if i in ask:
            return True
        if i in answer:
            return True
    return False


# 前置对话
def preposition_dialogue(word):
    dialogues_list = mrening.split('E')
    dialogues_list_good = []
    for dialogues in dialogues_list:
        dialogue = dialogues.split('M ')
        if (len(dialogue) is 3) and (dialogue[1].replace('\n', '') == word):
            if not filter_words(dialogue[1], dialogue[2]):
                dialogues_list_good.append([dialogue[1].replace('\n', ''), dialogue[2].replace('\n', '')])
    if len(dialogues_list_good) > 0:
        return dialogues_list_good[random.randint(0, len(dialogues_list_good) - 1)][1]
    else:
        return ''


with open("mrening.conv", "r", encoding='utf8') as f:
    mrening = f.read()
with open('filtered_words.txt', 'r', encoding='utf8') as f:
    filtered_words = f.read()
filtered_words_list = filtered_words.split('\n')
print(preposition_dialogue("不要学我说话"))
