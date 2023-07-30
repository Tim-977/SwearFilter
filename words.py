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

with open('good_list.txt', "r", encoding="utf-8") as file:
    content = file.read()

wordss = content.split()
good_words = wordss



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


def detect_spam(text):
    text = text.lower()
    if 'аааа' in text or 'аха' in text or 'яяя' in text or 'f[f' in text or 'axa' in text or 'еее' in text or 'ойой' in text or 'оооо' in text or 'блябля' in text or 'feulnaim' in text or 'спасспас' in text or 'пжпжпжпж' in text or 'ээээ' in text or 'susalarm' in text or 'мммм' in text or 'аахх' in text or 'http' in text or 'pрууp' in text or 'kфklkфsфоф' in text or 'дvхfvpsfcхs' in text or 'шзолдюиа' in text or 'sxdvgrextpa' in text or 'уууу' in text or 'фjъaячъ' in text or 'ййй' in text or len(text) > 23:
        return True
    return False


def remove_non_alpha(word):
    return ''.join(char for char in word if char.isalpha())


spam = []
temp_words = []

parsed_words = [remove_non_alpha(word) for word in words]

givenWords = list(filter(None, parsed_words))

givenWords = [x.lower() for x in givenWords[:]]

for word in givenWords:
    if not detect_spam(word):
        temp_words.append(word)
    else:
        spam.append(word)

givenWords = temp_words[:]

maxx, maxelem = 0, ''

for elem in givenWords:
    if len(elem) > maxx:
        maxx = len(elem[:])
        maxelem = elem[:]

print(maxx)
print(maxelem)

def levenshtein_distance(s, t):
    m = len(s)
    n = len(t)
    d = [[0] * (n + 1) for i in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + 1)
    return d[m][n]


def correct_spelling(word, valued_words):
    if word == '':
        closest_word = ''
    else:
        distances = [(levenshtein_distance(word, w), w) for w in valued_words]
        # print(sorted(distances))
        closest_word = min(distances)[1]
        handled_closest = f"{word} -- {closest_word} -- {min(distances)[0]}/{len(closest_word)} -- {int((round((min(distances)[0] / len(closest_word)) * 100, 0)))}%"
        handled_word = f"{word} -- {min(distances)[0]}/{len(closest_word)} -- {int((round((min(distances)[0] / len(closest_word)) * 100, 0)))}%    ----- {closest_word}"
        if int((round((min(distances)[0] / len(closest_word)) * 100, 0))) < 27:
            return handled_closest, 0
        return handled_word, 1

changed_list = []
original_list = []

counter = 1

for word in givenWords:
    temp = correct_spelling(word, valuedWords)
    if temp[1] or word in good_words:
        original_list.append(temp[0])
    else:
        changed_list.append(temp[0])
    
    if counter % 100 == 0:
        print(f'{counter} {"▮" * int(str((counter / len(givenWords)) * 100)[:1])}{"▯" * (10 - int(str((counter / len(givenWords)) * 100)[:1]))} {str((counter / len(givenWords)) * 100)[:5]}% {word}')
    if counter == len(givenWords):
        print(f'{counter} "▮▮▮▮▮▮▮▮▮▮ 100%')
    counter += 1

with open('original_list.txt', 'w', encoding='UTF-8') as file:
    file.write('Original list\n')
    file.write('original_word | distance | distance_% | closest_word\n')
    for elem in original_list:
        file.write(elem + '\n')
    file.write(str(len(original_list)))

with open('changed_list.txt', 'w', encoding='UTF-8') as file:
    file.write('Changed list\n')
    file.write('original_word | closest_word | distance | distance_%\n')
    for elem in changed_list:
        file.write(elem + '\n')
    file.write(str(len(changed_list)))

with open('spam.txt', 'w', encoding='UTF-8') as file:
    file.write('Spam list\n')
    for elem in spam:
        file.write(elem + '\n')
    file.write(str(len(spam)))

print(f'Original length: {len(original_list)}')

print(f'Swear: {len(changed_list)}')

print(f'Swear_%: {len(changed_list) / len(original_list)}')

print(f'Spam: {len(spam)}')
