from maps_data import forest_map
from quests_data import forest_quests
from utils import render_map, calculate_damage
from game_state import player_hp, player_mp, player_armor, player_damage, player_level, player_experience, inventory, update_player_stats, add_to_inventory

map_width = len(forest_map[0])
map_height = len(forest_map)

enemy_hp = 5
enemy_armor = 1
enemy_damage = 2
enemy_alive = False
spawn_counter = 0
enemy_x = -1  
enemy_y = -1  

def create_forest_map():
    return [row.copy() for row in forest_map]

def respawn_enemy(game_map):
    global enemy_hp, enemy_alive, spawn_counter, enemy_x, enemy_y
    enemy_hp = 5 + player_level * 2
    enemy_alive = True

    edges = ['top', 'bottom', 'left', 'right']
    edge = edges[spawn_counter % len(edges)]

    if edge == 'top':
        enemy_x, enemy_y = 0, map_width // 2
    elif edge == 'bottom':
        enemy_x, enemy_y = map_height - 1, map_width // 2
    elif edge == 'left':
        enemy_x, enemy_y = map_height // 2, 0
    elif edge == 'right':
        enemy_x, enemy_y = map_height // 2, map_width - 1

    if game_map[enemy_y][enemy_x] != '.':
        print("Ошибка: враг не может появиться здесь!")
        return

    game_map[enemy_y][enemy_x] = 'E'
    print(f"Враг респавнится на новой позиции: ({enemy_x}, {enemy_y}).")
    spawn_counter += 1

def start_forest():
    print("\n--- Лес ---")
    print("Квесты:")
    for quest in forest_quests.values():
        print(f"- {quest}")

    game_map = create_forest_map()
    interacted_objects = set()  
    player_x, player_y = map_width // 2, map_height // 2

    while game_map[player_y][player_x] == 'T':
        player_x = (player_x + 1) % map_width
        player_y = (player_y + 1) % map_height
    game_map[player_y][player_x] = '@'

    respawn_enemy(game_map)

    while True:
        render_map(game_map)
        print(f"Ваше здоровье: {player_hp}, Инвентарь: {inventory}, Уровень: {player_level}, Опыт: {player_experience}")
        move = input("Введите направление (w-вверх, s-вниз, a-влево, d-вправо, pick-взаимодействие, attack-атака, exit-выход): ")

        if move == 'exit':
            print("Вы покинули лес.")
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

            current_symbol = forest_map[player_y][player_x]
            if current_symbol == 'G':
                print("Вы собрали грибы!")
                add_to_inventory("Грибы")  
                interacted_objects.add(current_pos)
                game_map[player_y][player_x] = '@'
            elif current_symbol == 'A':
                print("Вы напугали животное, и оно убежало!")
                add_to_inventory("Шкура животного") 
                interacted_objects.add(current_pos)
                game_map[player_y][player_x] = '@'
            else:
                print("Здесь нечего подбирать.")
            continue

        if move == 'attack':
            if abs(player_x - enemy_x) <= 1 and abs(player_y - enemy_y) <= 1:
                damage = calculate_damage(player_damage, enemy_armor)
                enemy_hp -= damage
                print(f"Вы нанесли {damage} урона врагу. У врага осталось {enemy_hp} HP.")
                if enemy_hp <= 0:
                    print("Вы победили врага!")
                    enemy_alive = False
                    game_map[enemy_y][enemy_x] = '.'  
                    update_player_stats(experience=player_experience + 5) 
                    continue
                enemy_damage_to_player = calculate_damage(enemy_damage, player_armor)
                update_player_stats(hp=player_hp - enemy_damage_to_player) 
                print(f"Враг нанес вам {enemy_damage_to_player} урона. У вас осталось {player_hp} HP.")
                if player_hp <= 0:
                    print("Вы проиграли!")
                    exit()
            else:
                print("Рядом нет врага для атаки!")
            continue

        if 0 <= new_x < map_width and 0 <= new_y < map_height:
            if (player_x, player_y) in interacted_objects:
                game_map[player_y][player_x] = '.'  
            else:
                game_map[player_y][player_x] = forest_map[player_y][player_x]  

            player_x, player_y = new_x, new_y
            game_map[player_y][player_x] = '@'
        else:
            print("Неверное направление!")