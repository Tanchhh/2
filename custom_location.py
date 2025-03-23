from maps_data import custom_map
from quests_data import custom_quests
from utils import render_map, calculate_damage
from game_state import player_hp, player_mp, player_armor, player_damage, player_level, player_experience, inventory, update_player_stats, add_to_inventory

map_width = len(custom_map[0])
map_height = len(custom_map)

def create_custom_map():
    return [row.copy() for row in custom_map]

def start_custom_location():
    print("\n--- Таинственная пещера ---")
    print("Квесты:")
    for quest in custom_quests.values():
        print(f"- {quest}")

    game_map = create_custom_map()
    interacted_objects = set()  
    player_x, player_y = map_width // 2, map_height // 2

    while game_map[player_y][player_x] in ['M', 'C']:
        player_x = (player_x + 1) % map_width
        player_y = (player_y + 1) % map_height
    game_map[player_y][player_x] = '@'

    while True:
        render_map(game_map)
        print(f"Ваше здоровье: {player_hp}, Инвентарь: {inventory}, Уровень: {player_level}, Опыт: {player_experience}")
        move = input("Введите направление (w-вверх, s-вниз, a-влево, d-вправо, pick-взаимодействие, attack-атака, exit-выход): ")

        if move == 'exit':
            print("Вы покинули пещеру.")
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

            current_symbol = custom_map[player_y][player_x]
            if current_symbol == 'C':
                print("Вы нашли магический кристалл! Игра завершена!")
                exit()
            else:
                print("Здесь нечего подбирать.")
            continue

        if move == 'attack':
            if custom_map[new_y][new_x] == 'M':
                mini_boss_hp = 15
                mini_boss_armor = 2
                mini_boss_damage = 4

                while mini_boss_hp > 0:
                    damage = calculate_damage(player_damage, mini_boss_armor)
                    mini_boss_hp -= damage
                    print(f"Вы нанесли {damage} урона мини-боссу. У мини-босса осталось {mini_boss_hp} HP.")

                    if mini_boss_hp <= 0:
                        print("Вы победили мини-босса!")
                        game_map[new_y][new_x] = '.'  
                        update_player_stats(experience=player_experience + 10)  
                        break

                    mini_boss_damage_to_player = calculate_damage(mini_boss_damage, player_armor)
                    update_player_stats(hp=player_hp - mini_boss_damage_to_player)  
                    print(f"Мини-босс нанес вам {mini_boss_damage_to_player} урона. У вас осталось {player_hp} HP.")

                    if player_hp <= 0:
                        print("Вы проиграли!")
                        exit()

            else:
                print("Здесь нет врага для атаки!")
            continue

        if 0 <= new_x < map_width and 0 <= new_y < map_height:
            if (player_x, player_y) in interacted_objects:
                game_map[player_y][player_x] = '.'  
            else:
                game_map[player_y][player_x] = custom_map[player_y][player_x]  

            player_x, player_y = new_x, new_y
            game_map[player_y][player_x] = '@'
        else:
            print("Неверное направление!")