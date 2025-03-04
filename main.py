from enum import Enum
from typing import List, Union, Dict, Tuple


# Определение типов тайлов
class TileType(Enum):
    MANZU = 'm'
    PINZU = 'p'
    SOUZU = 's'
    WIND = 'z'
    DRAGON = 'd'


class Tile:
    def __init__(self, type: TileType, value: Union[int, str]):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.value}{self.type.value}"


# Парсинг ввода
wind_map = {'east': 1, 'south': 2, 'west': 3, 'north': 4}
dragon_map = {'white': 5, 'green': 6, 'red': 7}
reverse_wind_map = {v: k for k, v in wind_map.items()}
reverse_dragon_map = {v: k for k, v in dragon_map.items()}


def parse_input(input_str: str) -> List[Tile]:
    tiles = []
    for token in input_str.replace('0', '5').split():
        raw_value = token[:-1]
        type_char = token[-1].lower()

        # Проверка, если введён текстовый ветер или дракон
        if token.lower() in wind_map:
            tiles.append(Tile(TileType.WIND, wind_map[token.lower()]))
            continue
        elif token.lower() in dragon_map:
            tiles.append(Tile(TileType.DRAGON, dragon_map[token.lower()]))
            continue

        try:
            if type_char == 'z':
                value = int(raw_value)
                if value in wind_map.values():
                    tiles.append(Tile(TileType.WIND, value))
                elif value in dragon_map.values():
                    tiles.append(Tile(TileType.DRAGON, value))
                else:
                    raise ValueError(f"Invalid tile: {token}")
            else:
                tile_type = {'m': TileType.MANZU, 'p': TileType.PINZU, 's': TileType.SOUZU}[type_char]
                value = int(raw_value)
                if not 1 <= value <= 9:
                    raise ValueError(f"Invalid tile value: {value}")
                tiles.append(Tile(tile_type, value))
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid tile: {token}. Error: {e}")
    return tiles



# Подсчет количества каждого тайла в руке
def count_tiles(tiles: List[Tile]) -> Dict[Tuple[TileType, Union[int, str]], int]:
    counts = {}
    for tile in tiles:
        key = (tile.type, tile.value)
        counts[key] = counts.get(key, 0) + 1
    return counts


# Ищем последовательности (чии)
def find_sequences(counts):
    sequence_counts = counts.copy()
    sequences = 0

    for (tile_type, value), count in list(sequence_counts.items()):
        if tile_type in [TileType.MANZU, TileType.PINZU, TileType.SOUZU]:
            while sequence_counts.get((tile_type, value), 0) > 0 and \
                    sequence_counts.get((tile_type, value + 1), 0) > 0 and \
                    sequence_counts.get((tile_type, value + 2), 0) > 0:
                sequence_counts[(tile_type, value)] -= 1
                sequence_counts[(tile_type, value + 1)] -= 1
                sequence_counts[(tile_type, value + 2)] -= 1
                sequences += 1

    return sequences


# Проверка завершенности
#руки
def is_complete(counts):
    groups = 0
    pair_found = False
    temp_counts = counts.copy()

    for key, count in temp_counts.items():
        if count >= 3:
            groups += 1
            temp_counts[key] -= 3

    groups += find_sequences(temp_counts)

    for key, count in temp_counts.items():
        if count >= 2:
            pair_found = True
            break

    return groups >= 4 and pair_found


# Поиск тайлов для темпая
def find_tenpai_tiles(tiles: List[Tile]):
    counts = count_tiles(tiles)
    possible_tiles = []

    for tile_type in [TileType.MANZU, TileType.PINZU, TileType.SOUZU, TileType.WIND, TileType.DRAGON]:
        for value in range(1, 10):
            new_counts = counts.copy()
            key = (tile_type, value)
            new_counts[key] = new_counts.get(key, 0) + 1

            if is_complete(new_counts):
                if tile_type == TileType.WIND:
                    possible_tiles.append(reverse_wind_map.get(value, f"{value}{tile_type.value}"))
                elif tile_type == TileType.DRAGON:
                    possible_tiles.append(reverse_dragon_map.get(value, f"{value}{tile_type.value}"))
                else:
                    possible_tiles.append(f"{value}{tile_type.value}")

    return possible_tiles


# Функция анализа руки
def analyze_hand(tiles: List[Tile]):
    tenpai_tiles = find_tenpai_tiles(tiles)
    return {
        "is_tenpai": len(tenpai_tiles) > 0,
        "waiting_tiles": tenpai_tiles
    }


# Интерфейс командной строки
def main():
    input_str = input("Введите руку (например, '1m 2m 3m 4p 5p 6p 7s 8s 9s east east west west'): ")
    try:
        tiles = parse_input(input_str)
        result = analyze_hand(tiles)
        if result["is_tenpai"]:
            print("Темпай: Да")
            print("Ждём тайлы:", ", ".join(result["waiting_tiles"]))
        else:
            print("Темпай: Нет")
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()