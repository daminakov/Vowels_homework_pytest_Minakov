"""Tests for homework.

Checked with Pylint and Flake8 (IMHO Pylint more useful).
"""
from time import sleep
from selenium import webdriver

import pyautogui

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_driver = webdriver.Chrome\
    (service=Service(ChromeDriverManager().install()))
VOWELS = {'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я'}
SPACE = {' '}
PUNTCUATION = {'.', ',', '-', '!', '?', ':', ';'}

chrome_driver.get('https://rioran.github.io/ru_vowels_filter/main.html')
chrome_driver.maximize_window()

BUTTON_VOWELS = chrome_driver.find_element \
        (By.XPATH, "//button[contains(.,\'Оставить только гласные\')]")
BUTTON_HIGHLIGHT =chrome_driver.find_element\
        (By.XPATH, "//button[contains(.,\'Выделить результат\')]")
BUTTON_SPACES = chrome_driver.find_element\
        (By.XPATH, "//button[contains(.,\'Ну и ещё пробелы\')]")
BUTTON_PUNCTUATION = chrome_driver.find_element\
        (By.XPATH, "//button[contains(.,\'Оставить ещё и .,-!?\')]")


def convert_text_into_set(text):
    """Cycle for text.

    This function deploy text into list and change it into set.
    """
    char_list = []
    for char in text:
        if char not in char_list:
            char_list.append(char)
    char_set = set(char_list)
    return char_set


def test_vowels_with_default_text():
    """TEST.

    This test checks if on page present buttons which
    filtrate in default text only vowels.
    """
    text_input = chrome_driver.find_element('id', 'text_input').text
    set_input = convert_text_into_set(text_input)
    match_input = set_input.intersection(VOWELS)
    sleep(1)
    BUTTON_VOWELS.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    output_text = output_text.replace('\n', '')
    output_set = convert_text_into_set(output_text)
    match_output = output_set.intersection(VOWELS)
    assert match_input == match_output


def test_vowels_space_with_default_text():
    """TEST.

    This test checks if on page present buttons which
    filtrate in default text only vowels and spaces.
    """
    vowels_space = VOWELS.union(SPACE)
    text_input = chrome_driver.find_element('id', 'text_input').text
    set_input = convert_text_into_set(text_input)
    match_input = set_input.intersection(vowels_space)
    sleep(1)
    BUTTON_SPACES.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    output_text = output_text.replace('\n', '')
    output_set = convert_text_into_set(output_text)
    match_output = output_set.intersection(vowels_space)
    assert match_input == match_output


def test_vowels_space_punctuation_with_default_text():
    """TEST.

    This test checks if on page present buttons which
    filtrate in default text only vowels, spaces and punctuation.
    """
    vowels_space_punct = (VOWELS.union(SPACE)).union(PUNTCUATION)
    text_input = chrome_driver.find_element('id', 'text_input').text
    set_input = convert_text_into_set(text_input)
    match_input = set_input.intersection(vowels_space_punct)
    sleep(1)
    BUTTON_PUNCTUATION.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    output_text = output_text.replace('\n', '')
    output_set = convert_text_into_set(output_text)
    match_output = output_set.intersection(vowels_space_punct)
    assert match_input == match_output


def test_vowels_in_random_input_text():
    """TEST.

    This test checks if on page present buttons which
    filtrate in random text only vowels.
    """
    chrome_driver.find_element('name', 'text_input').clear()
    chrome_driver.find_element \
        ('name', 'text_input').send_keys(
        'На золотом крыльце сидели,\nЦарь-царевич, '
        'Король-королевич,\nСапожник, портной. '
        'Кто ты будешь такой?\nВыбирай поскорей!\n'
        'Не задерживай добрых и честных людей!'
        '\n\nФёдор Михайлович Достоевский.'
    )
    match_input = {'ё', 'а', 'е', 'ю', 'о', 'у', 'ы', 'и'}
    BUTTON_VOWELS.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    set_output = convert_text_into_set(output_text)
    match_output = set_output.intersection(VOWELS)
    assert match_input == match_output


def test_vowels_space_in_random_input_text():
    """TEST.

    This test checks if on page present buttons which
    filtrate in random text only vowels and spaces.
    """
    vowels_space = VOWELS.union(SPACE)
    match_input = {'ё', 'а', 'е', 'ю', 'о', 'у', 'ы', 'и', ' '}
    BUTTON_SPACES.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    set_output = convert_text_into_set(output_text)
    match_output = set_output.intersection(vowels_space)
    assert match_input == match_output


def test_vowels_space_punct_in_random_input_text():
    """TEST.

    This test checks if on page present buttons which
    filtrate in random text only vowels, spaces and punctuation.
    """
    vowels_space_punct = (VOWELS.union(SPACE)).union(PUNTCUATION)
    match_input = {
        'ё', 'а', 'е', 'ю', 'о', 'у', 'ы', 'и',
        ' ', ',', '.', '?', '!', '-',
    }
    BUTTON_PUNCTUATION.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    output_text = chrome_driver.find_element('id', 'text_output').text
    set_output = convert_text_into_set(output_text)
    match_output = set_output.intersection(vowels_space_punct)
    assert match_input == match_output


def test_blank_input_text():
    """Tests for checking blank fild in input text and using all buttons."""
    chrome_driver.find_element('name', 'text_input').clear()
    BUTTON_VOWELS.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    result = chrome_driver.find_element('id', 'text_output').text
    assert result == ''
    BUTTON_SPACES.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    result = chrome_driver.find_element('id', 'text_output').text
    assert result == ''
    BUTTON_PUNCTUATION.click()
    BUTTON_HIGHLIGHT.click()
    sleep(1)
    result = chrome_driver.find_element('id', 'text_output').text
    assert result == ''


def test_check_button_location_on_max_window():
    """Check location of buttons with maximum windows size."""
    find_vowels_button_locatioin = BUTTON_VOWELS
    location_vowels_button = find_vowels_button_locatioin.location
    vowels_vertical = location_vowels_button['y']
    find_and_spaces_location = BUTTON_SPACES
    location_and_spaces_button = find_and_spaces_location.location
    and_spaces_vertical = location_and_spaces_button['y']
    find_so_punctuation_button = BUTTON_PUNCTUATION
    location_so_punctuation_button = find_so_punctuation_button.location
    so_punctuation_vertical = location_so_punctuation_button['y']
    find_highlight_results_button = BUTTON_HIGHLIGHT
    location_highlight_results_button = find_highlight_results_button.location
    highlight_results_vertical = location_highlight_results_button['y']
    assert vowels_vertical == and_spaces_vertical
    assert and_spaces_vertical == so_punctuation_vertical
    assert so_punctuation_vertical == highlight_results_vertical


def test_check_button_location_mid_size_window():
    """Check buttons location with middle window size."""
    chrome_driver.set_window_size(500, 800)
    find_vowels_button_locatioin = BUTTON_VOWELS
    location_vowels_button = find_vowels_button_locatioin.location
    vowels_vertical = location_vowels_button['y']
    find_and_spaces_location = BUTTON_SPACES
    location_and_spaces_button = find_and_spaces_location.location
    and_spaces_vertical = location_and_spaces_button['y']
    find_so_punctuation_button = BUTTON_PUNCTUATION
    location_so_punctuation_button = find_so_punctuation_button.location
    so_punctuation_vertical = location_so_punctuation_button['y']
    find_highlight_results_button = BUTTON_HIGHLIGHT
    location_highlight_results_button = find_highlight_results_button.location
    highlight_results_vertical = location_highlight_results_button['y']
    assert vowels_vertical <= and_spaces_vertical
    assert and_spaces_vertical == so_punctuation_vertical
    assert so_punctuation_vertical < highlight_results_vertical


def test_check_button_location_min_size_window():
    """Check button location with minimal window size."""
    chrome_driver.set_window_size(400, 800)
    sleep(1)
    pyautogui.press('F12')
    sleep(3)
    find_vowels_button_locatioin = BUTTON_VOWELS
    location_vowels_button = find_vowels_button_locatioin.location
    vowels_vertical = location_vowels_button['y']
    find_and_spaces_location = BUTTON_SPACES
    location_and_spaces_button = find_and_spaces_location.location
    and_spaces_vertical = location_and_spaces_button['y']
    find_so_punctuation_button = BUTTON_PUNCTUATION
    location_so_punctuation_button = find_so_punctuation_button.location
    so_punctuation_vertical = location_so_punctuation_button['y']
    find_highlight_results_button = BUTTON_HIGHLIGHT
    location_highlight_results_button = find_highlight_results_button.location
    highlight_results_vertical = location_highlight_results_button['y']
    assert vowels_vertical < and_spaces_vertical
    assert and_spaces_vertical < so_punctuation_vertical
    assert so_punctuation_vertical < highlight_results_vertical


    chrome_driver.close()
