import json

with open('valuedWords.txt', 'r', encoding='UTF-8') as f:
    valuedWords = f.readlines()
    valuedWords = [
        x
        for x in [x[:-1] if x != valuedWords[-1] else x for x in valuedWords]
        if x
    ]

with open('result.json', 'r', encoding='UTF-8') as json_file:
    data = json.load(json_file)

messages_texts = []

for message in data['messages']:
    messages_texts.append(message['text'])

words = []


def add_words(text):
    words.extend(text.split())


for sentence in messages_texts:
    if isinstance(sentence, str):
        add_words(sentence)
    elif isinstance(sentence, list):
        for item in sentence:
            if isinstance(item, str):
                add_words(item)
            elif isinstance(item, dict) and 'text' in item:
                add_words(item['text'])

print('DONE WITH UTILS')