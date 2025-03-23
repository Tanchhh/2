from maps_data import dungeon_map
from quests_data import dungeon_quests
from utils import render_map, calculate_damage
from game_state import player_hp, player_mp, player_armor, player_damage, player_level, player_experience, inventory, update_player_stats, add_to_inventory

map_width = len(dungeon_map[0])
map_height = len(dungeon_map)

def create_dungeon_map():
    return [row.copy() for row in dungeon_map]

def start_dungeon():
    print("\n--- Подземелье ---")
    print("Квесты:")
    for quest in dungeon_quests.values():
        print(f"- {quest}")

    game_map = create_dungeon_map()
    interacted_objects = set()  
    player_x, player_y = map_width // 2, map_height // 2

    while game_map[player_y][player_x] == '#':
        player_x = (player_x + 1) % map_width
        player_y = (player_y + 1) % map_height
    game_map[player_y][player_x] = '@'

    while True:
        render_map(game_map)
        print(f"Ваше здоровье: {player_hp}, Инвентарь: {inventory}, Уровень: {player_level}, Опыт: {player_experience}")
        move = input("Введите направление (w-вверх, s-вниз, a-влево, d-вправо, pick-взаимодействие, attack-атака, exit-выход): ")

        if move == 'exit':
            print("Вы покинули подземелье.")
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

            current_symbol = dungeon_map[player_y][player_x]
            if current_symbol == 'T':
                print("Вы открыли сундук и нашли золото!")
                add_to_inventory("Золото")  
                interacted_objects.add(current_pos)
                game_map[player_y][player_x] = '@'
            else:
                print("Здесь нечего подбирать.")
            continue

        if move == 'attack':
            if dungeon_map[new_y][new_x] == 'R':
                rat_hp = 5
                rat_armor = 0
                rat_damage = 1

                while rat_hp > 0:
                    damage = calculate_damage(player_damage, rat_armor)
                    rat_hp -= damage
                    print(f"Вы нанесли {damage} урона крысе. У крысы осталось {rat_hp} HP.")

                    if rat_hp <= 0:
                        print("Вы победили крысу!")
                        game_map[new_y][new_x] = '.'  
                        update_player_stats(experience=player_experience + 3) 
                        break

                    rat_damage_to_player = calculate_damage(rat_damage, player_armor)
                    update_player_stats(hp=player_hp - rat_damage_to_player)  
                    print(f"Крыса нанесла вам {rat_damage_to_player} урона. У вас осталось {player_hp} HP.")

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
                game_map[player_y][player_x] = dungeon_map[player_y][player_x]  

            player_x, player_y = new_x, new_y
            game_map[player_y][player_x] = '@'
        else:
            print("Неверное направление!")