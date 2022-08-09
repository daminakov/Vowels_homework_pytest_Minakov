'''Tests for home works with Pylint Flake8'''
from time import sleep
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
VOWELS = {'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я'}
SPACE = {' '}
PUNTCUATION = {'.', ',', '-', '!', '?', ':', ';'}

chrome_driver.get('https://rioran.github.io/ru_vowels_filter/main.html')
chrome_driver.maximize_window()


def convert_text_into_set(text):
    '''This function deploy text into list and change it into set'''
    char_list = []
    for char in text:
        if char not in char_list:
            char_list.append(char)
    char_set = set(char_list)
    return char_set


def test_vowels_with_default_text():
    '''This test checks if on page present buttons which filtrate in default text only vowels'''
    text_input = chrome_driver.find_element('id', 'text_input').text
    set_input = convert_text_into_set(text_input)
    match_input = set_input.intersection(VOWELS)
    sleep(1)
    chrome_driver.find_element \
        (By.XPATH, "//button[contains(.,\'Оставить только гласные\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    output_text = output_text.replace('\n', '')
    output_set = convert_text_into_set(output_text)
    match_output = output_set.intersection(VOWELS)
    assert match_input == match_output


def test_vowels_space_with_default_text():
    '''This test checks if on page present buttons which filtrate in default text only vowels
    and spaces'''
    vowels_space = VOWELS.union(SPACE)
    text_input = chrome_driver.find_element('id', 'text_input').text
    set_input = convert_text_into_set(text_input)
    match_input = set_input.intersection(vowels_space)
    sleep(1)
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Ну и ещё пробелы\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    output_text = output_text.replace('\n', '')
    output_set = convert_text_into_set(output_text)
    match_output = output_set.intersection(vowels_space)
    assert match_input == match_output


def test_vowels_space_punctuation_with_default_text():
    '''This test checks if on page present buttons which filtrate in default text only
    vowels, spaces and punctuation'''
    vowels_space_punct = (VOWELS.union(SPACE)).union(PUNTCUATION)
    text_input = chrome_driver.find_element('id', 'text_input').text
    set_input = convert_text_into_set(text_input)
    match_input = set_input.intersection(vowels_space_punct)
    sleep(1)
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Оставить ещё и .,-!?\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    output_text = output_text.replace('\n', '')
    output_set = convert_text_into_set(output_text)
    match_output = output_set.intersection(vowels_space_punct)
    assert match_input == match_output


def test_vowels_in_random_input_text():
    '''This test checks if on page present buttons which filtrate in random text only vowels'''
    chrome_driver.find_element('name', 'text_input').clear()
    chrome_driver.find_element \
        ('name', 'text_input').send_keys(
        'На золотом крыльце сидели,\nЦарь-царевич, Король-королевич,'
        '\nСапожник, портной. Кто ты будешь такой?\n'
        'Выбирай поскорей!\nНе задерживай добрых и честных людей!'
        '\n\nФёдор Михайлович Достоевский.')
    match_input = {'ё', 'а', 'е', 'ю', 'о', 'у', 'ы', 'и'}
    chrome_driver.find_element \
        (By.XPATH, "//button[contains(.,\'Оставить только гласные\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    set_output = convert_text_into_set(output_text)
    match_output = set_output.intersection(VOWELS)
    assert match_input == match_output


def test_vowels_space_in_random_input_text():
    '''This test checks if on page present buttons which filtrate in random text only
        vowels and spaces'''
    vowels_space = VOWELS.union(SPACE)
    match_input = {'ё', 'а', 'е', 'ю', 'о', 'у', 'ы', 'и', ' '}
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Ну и ещё пробелы\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    set_output = convert_text_into_set(output_text)
    match_output = set_output.intersection(vowels_space)
    assert match_input == match_output


def test_vowels_space_punct_in_random_input_text():
    '''This test checks if on page present buttons which filtrate in random text only
        vowels, spaces and punctuation'''
    vowels_space_punct = (VOWELS.union(SPACE)).union(PUNTCUATION)
    match_input = {'ё', 'а', 'е', 'ю', 'о', 'у', 'ы', 'и', ' ', ',', '.', '?', '!', '-'}
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Оставить ещё и .,-!?\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    set_output = convert_text_into_set(output_text)
    match_output = set_output.intersection(vowels_space_punct)
    assert match_input == match_output


def test_blank_input_text():
    '''Tests for checking blank fild in input text and using all buttons'''
    chrome_driver.find_element \
        ('name', 'text_input').clear()
    chrome_driver.find_element \
        (By.XPATH, "//button[contains(.,\'Оставить только гласные\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    result = chrome_driver.find_element('id', 'text_output').text
    assert result == ''
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Ну и ещё пробелы\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    result = chrome_driver.find_element('id', 'text_output').text
    assert result == ''
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Оставить ещё и .,-!?\')]").click()
    chrome_driver.find_element(By.XPATH, "//button[contains(.,\'Выделить результат\')]").click()
    sleep(1)
    result = chrome_driver.find_element('id', 'text_output').text
    assert result == ''


    chrome_driver.close()
