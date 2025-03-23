import village
import forest
import dungeon
import custom_location
from game_state import player_hp, player_mp, player_armor, player_damage, player_level, player_experience, inventory

def start_game():
    print("Добро пожаловать в игру!")
    print("Вы начинаете в стартовой зоне обучения.")
    input("Нажмите Enter, чтобы продолжить...")

    training_zone = [['.' for _ in range(5)] for _ in range(5)]
    training_zone[2][2] = '@'
    village.render_map(training_zone)

    print("В этой зоне вы можете:")
    print("1. Перемещаться по карте (w, s, a, d).")
    print("2. Атаковать мобов (attack).")
    print("3. Взаимодействовать с объектами (pick, enter).")
    input("Нажмите Enter, чтобы покинуть зону обучения...")

    while True:
        print("\nВыберите локацию:")
        print("1. Деревня")
        print("2. Лес")
        print("3. Подземелье")
        print("4. Пользовательская локация")
        print("5. Выход из игры")
        
        choice = input("Введите номер локации: ").strip()
        if choice == '1':
            village.start_village()
        elif choice == '2':
            forest.start_forest()
        elif choice == '3':
            dungeon.start_dungeon()
        elif choice == '4':
            custom_location.start_custom_location()
        elif choice == '5':
            print("Спасибо за игру! До свидания.")
            exit()
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    start_game()