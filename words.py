from utils import valuedWords, words


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
        closest_word = min(distances)[1]
        handled_closest = f"{word} -- {closest_word} -- {min(distances)[0]}/{len(closest_word)} -- {int((round((min(distances)[0] / len(closest_word)) * 100, 0)))}%"
        handled_word = f"{word} -- {min(distances)[0]}/{len(closest_word)} -- {int((round((min(distances)[0] / len(closest_word)) * 100, 0)))}%    ----- {closest_word}"
        if int((round((min(distances)[0] / len(closest_word)) * 100, 0))) < 27:
            return handled_closest, 0
        return handled_word, 1

changed_list = []
original_list = []
counter = 1
for word in words:
    temp = correct_spelling(word, valuedWords)
    if temp[1]:
        original_list.append(temp[0])
    else:
        changed_list.append(temp[0])
    
    if counter % 100 == 0:
        print(f'{counter} {"▮" * int(str((counter / len(words)) * 100)[:1])}{"▯" * (10 - int(str((counter / len(words)) * 100)[:1]))} {str((counter / len(words)) * 100)[:5]}%')
    if counter == len(words):
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

print(f'Changed length: {len(changed_list)}')

print(f'Original length: {len(original_list)}')

print(f'Swear: {len(changed_list)}')