player_hp = 10
player_mp = 5
player_armor = 2
player_damage = 3
player_level = 1
player_experience = 0
inventory = []

spawn_counter = 0

def update_player_stats(hp=None, mp=None, armor=None, damage=None, level=None, experience=None):
    global player_hp, player_mp, player_armor, player_damage, player_level, player_experience
    if hp is not None:
        player_hp = hp
    if mp is not None:
        player_mp = mp
    if armor is not None:
        player_armor = armor
    if damage is not None:
        player_damage = damage
    if level is not None:
        player_level = level
    if experience is not None:
        player_experience = experience

def add_to_inventory(item):
    global inventory
    inventory.append(item)