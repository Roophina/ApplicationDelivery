"""Функции для генерации тестовых данных."""
import string
import random


def generate_random_string(length: int) -> str:
    """Генерация строки, содержащей строчные буквы и цифры."""
    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


def generate_random_status() -> str:
    """Генерация случайного значения из списка."""
    status_list = ["to_do", "in_progress", "done"]
    return random.choice(status_list)
