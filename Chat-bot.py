from random import choice
import re
import nltk

intents = {
    'hello': {
        'examples': ['Хелло', "Привет", "Здравствуйте"],
        'responses': ['Добрый день!', "Как дела?", "Как настроение?"]
    },
    'weather': {
        'examples': ['Какая погода?', 'Что за окном', "Во что одеваться?"],
        'responses': ['Погода отличная!', "У природы нет плохой погоды!"]
    },
    'undefined': {
        'examples': ['Какая погода?', 'Что за окном', "Во что одеваться?"],
        'responses': ["Ничем не могу помочь(", 'Попробуй еще раз']
    },
    'exit': {
        'examples': ['Выход', 'Пока'],
        'responses': ["До скорого", 'Всего хороошего']
    }
}


def clean_up(text):
    text = text.lower()  # преобразуем слово к нижнему регистру
    re_not_word = r'[^\w\s]'  # описываем текстовый шаблон для удаления: "все,
    # что не является буквой \w или пробелом \s"
    text = re.sub(re_not_word, '', text)  # заменяем в исходном тексте то, что соответствует шаблону,
    # на пустой текст (удаляем)

    return text  # возвращаем очищенный текст


def text_match(user_text, example):
    user_text = clean_up(user_text)
    example = clean_up(example)
    if user_text.find(example) != -1:  # find возвращает -1 в случае, если ничего не нашла
        return True
    if example.find(user_text) != -1:
        return True
    example_len = len(example)
    distance = nltk.edit_distance(user_text, example) / example_len

    return distance < 0.4


def get_intent(text):  # Определить намерение по тексту
    for intent_name in intents:
        for example in intents[intent_name]['examples']:
            if text_match(text, example):
                return intent_name
    return "undefined"


def get_response(intent):  # Берет случайны response для данного intent'а
    return choice(intents[intent]['responses'])


def bot(text):
    intent = get_intent(text)
    answer = get_response(intent)
    return answer


text = 'Привет'
while get_intent(text) != "exit":
    text = input('< ')
    print('>', bot(text))
