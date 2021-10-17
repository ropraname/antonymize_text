import string
import requests as re
from bs4 import BeautifulSoup
from random import randint


def antonymize_text(text):
    punctuation_symbols = set(string.punctuation)
    prepared_text = []
    new_text_name = text[:text.find('.')] + '_antonymized.txt'

    with open(text, "r") as text:
        for line in text:
            prepared_line = line.split(' ')
            for word_index, word in enumerate(prepared_line):
                for letter_index, letter in enumerate(word):
                    if letter in punctuation_symbols:
                        prepared_line[word_index] = [word[:letter_index], word[letter_index:]]
            for word in prepared_line:
                prepared_text.append(word)

    for word_index, word in enumerate(prepared_text):
        if type(word) == str:
            try:
                prepared_text[word_index] = get_antonym_with_random(word)
            except:
                continue
        else:
            try:
                prepared_text[word_index][0] = get_antonym_with_random(word[0])
            except:
                continue

    for word_index, word in enumerate(prepared_text):
        if type(word) == list:
            for word_el_index, word_el in enumerate(word):
                prepared_text[word_index][word_el_index] = word_el.replace(' ', '')
            prepared_text[word_index] = ''.join(word)
        else:
            prepared_text[word_index] = prepared_text[word_index].replace(' ', '')
    
    prepared_text = ' '.join(prepared_text)
    prepared_text = prepared_text.replace('\n ', '\n')

    with open(new_text_name, "w") as text:
        text.write(prepared_text)

    return prepared_text

def get_antonym_with_random(word):
    url = f'https://razbiraem-slovo.ru/antonyms/{word}'
    content = re.get(url)
    soup = BeautifulSoup(content.text, "html.parser")
    all_antonym_tags = soup.find_all('div', class_='words-columns__breaker')
    num_of_antonyms = len(all_antonym_tags)
    random_antonym_tag = all_antonym_tags[randint(0, num_of_antonyms - 1)]
    random_antonym = random_antonym_tag.find('a').text
    return random_antonym

if __name__ == "__main__":
    antonymize_text("text.txt")