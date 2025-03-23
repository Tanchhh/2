from maps_data import village_map
from quests_data import village_quests
from utils import render_map, calculate_damage

map_width = len(village_map[0])
map_height = len(village_map)

player_hp = 10
player_mp = 5
player_armor = 2
player_damage = 3
player_level = 1
player_experience = 0
inventory = []

def create_village_map():
    return [row.copy() for row in village_map]

def start_village():
    print("\n--- Деревня ---")
    print("Квесты:")
    for quest in village_quests.values():
        print(f"- {quest}")

    game_map = create_village_map()
    interacted_objects = set()  
    player_x, player_y = map_width // 2, map_height // 2

    while game_map[player_y][player_x] in ['S', 'W', 'H']:
        player_x = (player_x + 1) % map_width
        player_y = (player_y + 1) % map_height
    game_map[player_y][player_x] = '@'

    while True:
        render_map(game_map)
        print(f"Ваше здоровье: {player_hp}, Инвентарь: {inventory}, Уровень: {player_level}, Опыт: {player_experience}")
        move = input("Введите направление (w-вверх, s-вниз, a-влево, d-вправо, pick-взаимодействие, attack-атака, exit-выход): ")

        if move == 'exit':
            print("Вы покинули деревню.")
            break

        dx, dy = 0, 0
        if move == 'w': dy = -1
        elif move == 's': dy = 1
        elif move == 'a': dx = -1
        elif move == 'd': dx = 1

        new_x = player_x + dx
        new_y = player_y + dy

        if move == 'pick':
            current_pos = (player_x, player_y)
            if current_pos in interacted_objects:
                print("Здесь уже ничего нет.")
                continue

            current_symbol = village_map[player_y][player_x]
            if current_symbol == 'W':
                print("Вы собрали лечебные травы!")
                inventory.append("Лечебные травы")
                interacted_objects.add(current_pos)
                game_map[player_y][player_x] = '@'
            elif current_symbol == 'S':
                print("Вы исследовали сарай и нашли лопату!")
                inventory.append("Лопата")
                interacted_objects.add(current_pos)
                game_map[player_y][player_x] = '@'
            elif current_symbol == 'H':
                print("Житель хижины дал задание собрать шкуры.")
                inventory.append("Задание: собрать шкуры")
                interacted_objects.add(current_pos)
                game_map[player_y][player_x] = '@'
            else:
                print("Здесь нечего подбирать.")
            continue

        if move == 'attack':
            print("Здесь нет врагов для атаки!")
            continue

        if 0 <= new_x < map_width and 0 <= new_y < map_height:
            if (player_x, player_y) in interacted_objects:
                game_map[player_y][player_x] = '.'  
            else:
                game_map[player_y][player_x] = village_map[player_y][player_x]  

            player_x, player_y = new_x, new_y
            game_map[player_y][player_x] = '@'
        else:
            print("Неверное направление!")