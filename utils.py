def render_map(game_map):
    for row in game_map:
        print(' '.join(row))
    print()

def calculate_damage(attacker_damage, defender_armor):
    damage = max(0, attacker_damage - defender_armor)
    return damage