Проект pythonMahjong - реализация основной логики инструмента для сбора руки в игре Риичи Маджонг.
Инструмент помогает пользователю увидеть что он находится в темпай, помогает определить выигрышный тайл и собрать оптимальную относительно его требований руку.

На данный момент реализовано:

Класс tiles: каждый тайл имеет свой тип 
    MANZU = 'm'
    PINZU = 'p'
    SOUZU = 's'
    WIND = 'z'
    DRAGON = 'd'

MANZU, PINZU и SOUZU имеют значения от 1 до 9
    

parse_input - переводит написанную в консоль руку из формата "1m 2m 3m 4p 5p 6p 7s 8s 9s east east west west" в формат 1m, 2m, 3m, 4p, 5p, 6p, 7s, 8s, 9s, 1z, 1z, 3z, 3z для удобства.
Так же информирует об ошибках в написании руки.

count_tiles - Принимает список тайлов руки и возвращает словарь тайлов и количества каждого из них.

find_sequences - Примимает словарь count_tiles и проверяет его на наличие последовательностей чии, проверяет для каждого тайла есть ли у него последовательность и возвращает количество тайлов этой последовательности 
(3 если последовательность закончена)

is_complete Принимает словарь count_tiles, проверяет есть ли в нем 3 сета и пара, возвращает булевое значение статуса проверки.

find_tenpai_tiles - ПРинимает руку и проверяет каого тайла не хватает для победы.
analyze_hand - принимает на вход руку и возвращает статус тенпай
