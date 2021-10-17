'''This is a module for replacing Russian words in the text with their antonyms'''
import string
from random import randint
import requests as re
from bs4 import BeautifulSoup


def antonymize_text(text):
    '''Function for replacing Russian words in the text with their antonyms'''
    new_text_name = text[:text.find('.')] + '_antonymized.txt'

    prepared_text = parse_text_to_words(text)

    text_with_replacements = repl_with_antonyms_in_parsed_text(prepared_text)

    collected_text_with_replacements = reassemble_parsed_text(text_with_replacements)

    with open(new_text_name, "w", encoding="utf-8") as text_file:
        text_file.write(collected_text_with_replacements)

    return collected_text_with_replacements

def parse_text_to_words(text):
    '''Function for parsing a given text into an array of words and punctuation marks'''
    prepared_text = []
    punctuation_symbols = set(string.punctuation)
    with open(text, "r", encoding="utf-8") as text_file:
        for line in text_file:
            prepared_line = line.split(' ')
            for word_index, word in enumerate(prepared_line):
                for letter_index, letter in enumerate(word):
                    if letter in punctuation_symbols:
                        prepared_line[word_index] = [word[:letter_index], word[letter_index:]]
            for word in prepared_line:
                prepared_text.append(word)
    return prepared_text

def repl_with_antonyms_in_parsed_text(prepared_text):
    '''Function to replace all matching words of the parsed text with their antonyms'''
    for word_index, word in enumerate(prepared_text):
        if isinstance(word, str):
            try:
                prepared_text[word_index] = get_antonym_with_random(word)
            except ValueError:
                continue
        else:
            try:
                prepared_text[word_index][0] = get_antonym_with_random(word[0])
            except ValueError:
                continue
    return prepared_text

def reassemble_parsed_text(parsed_text):
    '''Function for assembling parsed text into a string'''
    prepared_text = parsed_text
    for word_index, word in enumerate(prepared_text):
        if isinstance(word, list):
            for word_el_index, word_el in enumerate(word):
                prepared_text[word_index][word_el_index] = word_el.replace(' ', '')
            prepared_text[word_index] = ''.join(word)
        else:
            prepared_text[word_index] = prepared_text[word_index].replace(' ', '')
    prepared_text = ' '.join(prepared_text)
    prepared_text = prepared_text.replace('\n ', '\n')
    return prepared_text

def get_antonym_with_random(word):
    '''Function to get the antonym for a given word'''
    url = f'https://razbiraem-slovo.ru/antonyms/{word}'
    content = re.get(url)
    soup = BeautifulSoup(content.text, "html.parser")
    all_antonym_tags = soup.find_all('div', class_='words-columns__breaker')
    num_of_antonyms = len(all_antonym_tags)
    random_antonym_tag = all_antonym_tags[randint(0, num_of_antonyms - 1)]
    random_antonym = random_antonym_tag.find('a').text
    return random_antonym

if __name__ == "__main__":
    print(antonymize_text("text.txt"))
