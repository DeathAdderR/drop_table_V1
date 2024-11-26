

import sqlite3

class MonsterDropTable:
    def __init__(self):
        self.connection = sqlite3.connect("drop_table.db")
        self.cursor = self.connection.cursor()
        self._initialize_database()
        self.item_qualities = ['common', 'uncommon', 'rare', 'epic']
    
    def _initialize_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS drop_table (
                            monster_name TEXT,
                            has_drop BOOLEAN,
                            item_name TEXT,
                            item_price INTEGER,
                            item_quality TEXT,
                            item_episode TEXT,
                            item_level INTEGER)''')
        self.connection.commit()

    def close_db(self):
        self.connection.close()
        print("Connection to database terminated")
        
    def add_kill(self, monster_name, has_drop, item_name, item_price, item_quality, item_episode, item_level):
        self.cursor.execute('''INSERT INTO drop_table (monster_name, has_drop, item_name, item_price, item_quality, item_episode, item_level) VALUES (?,?,?,?,?,?,?)''', (monster_name, has_drop, item_name, item_price, item_quality, item_episode, item_level,))
        self.connection.commit()
    
    def view_all_kills(self):
        self.cursor.execute('''SELECT * FROM drop_table''')  
        entries = self.cursor.fetchall()
        total_entries = 0

        if entries:
            for entry in entries:
                total_entries += 1
                monster_name, has_drop, item_name, item_price, item_quality, item_episode, item_level = entry
                
                if not has_drop:
                    print(f"Monster Killed: {monster_name} dropped nothing this fight.")
                else:
                    print(f"Monster Killed: {monster_name}\nItem Dropped: {item_name}\nItem Level: {item_level}\nItem Price: {item_price}\nItem Quality: {item_quality}\nEpisode: {item_episode}\n")

        print(f"\nThere are '{total_entries}' entries in the database")

    def view_kills_by_monster(self, monster_name):
        self.cursor.execute('''SELECT * FROM drop_table WHERE monster_name = ?''', (monster_name,))  
        entries = self.cursor.fetchall()
        kill_count = 0

        if entries:
            for entry in entries:
                kill_count += 1
                monster_name, has_drop, item_name, item_price, item_quality, item_episode, item_level = entry
                
                if not has_drop:
                    print(f"Monster Killed: {monster_name} dropped nothing this fight.")
                else:
                    print(f"Monster Killed: {monster_name}\nItem Dropped: {item_name}\nItem Level: {item_level}\nItem Price: {item_price}\nItem Quality: {item_quality}\nEpisode: {item_episode}\n")

        print(f"\nThere are '{kill_count}' entries for {monster_name}")

    def view_drop_chance_by_quality(self, quality):
        # get total entry count
        self.cursor.execute('''SELECT COUNT(*) FROM drop_table''')
        total_entries = self.cursor.fetchone()[0]
        # get item by quality count
        self.cursor.execute('''SELECT COUNT(*) FROM drop_table WHERE item_quality = ?''', (quality,))
        searched_entries = self.cursor.fetchone()[0] 
        drop_rate_step = int(searched_entries) / int(total_entries)
        drop_rate = drop_rate_step * 100
        print(f"\n\nDROP RATE FOR QUALITY '{quality}': {drop_rate}\n")


    def view_items_by_quality(self, quality):
        self.cursor.execute('''SELECT item_name, item_price, item_quality, item_level from drop_table WHERE item_quality = ?''', (quality,))
        entries = self.cursor.fetchall()

        if entries:
            total_entries = 0
            total_price = 0
            print(f"\n--- PRINTING BY QUALITY '{quality}'")
            for entry in entries:
                total_entries += 1
                item_name, item_price, item_quality, item_level = entry
                total_price += item_price
                print(f"\nName: {item_name}  Price: {item_price}  Level: {item_level}")
            
            print(f"\nTotal Entries: {total_entries}  Total Price: {total_price/1000} silver\n")



def track_kills(db):
    print("\n\n\n\n\n\t\t\t\t--- LAUNCHING KILL TRACKER ---")

    while True:
        print("\nOptions: A - Add kill  Q - Return to main menu\n=> ")
        user_input = input().strip().upper()

        if not user_input in ["A", "Q"]:
            print("\nThat was not a valid option")
            break
        else:
            if user_input == "A":
                monster_name = input("\nEnter the monster name: ").lower()
                no_drop_confirmation = input("Is this an empty drop?(Y/N): ").strip().upper()
                if not no_drop_confirmation in ["Y", "N"]:
                    print("\nThat was not a valid response")
                    break
                else:
                    if no_drop_confirmation == "Y":
                        item_name, item_quality, item_episode = "N/A", "N/A", "N/A"
                        item_price = -1
                        item_level = -1
                        has_drop = 0
                    else:
                        item_name = input("\nEnter the Item Name: ").lower()
                        item_quality = input("\nEnter the Item Quality: ").lower()
                        item_episode = input("\nEnter the Item Episode: ").lower()
                        has_drop = 1
                        item_price = int(input("\nEnter the Item Price: "))
                        item_level = int(input("\nEnter the Item Level: "))

                    confirm_entry = input(f"\n--- ENTRY CONFIRMATION ---\nMonster Name: '{monster_name}', Item Name: '{item_name}',  Item Quality: '{item_quality}',  Item Price: '{item_price}',  Item Level: '{item_level}',  Item Episode: '{item_episode}'\n(Y/N): ").strip().upper()

                    if not confirm_entry in ["Y", "N"]:
                        print("\nThat was not a valid entry")
                        break
                    else:
                        if confirm_entry == "Y":
                            db.add_kill(monster_name, has_drop, item_name, item_price, item_quality, item_episode, item_level)
                            print("\nENTRY ADDED\n")
                        else:
                            print("\nENTRY CANCELLED\n")
                            break
            else:
                print("\nReturning to main menu")
                return
            
def view_all_kills_cli(db):
    print("\n\n--- VIEWING ALL KILLS ---\n\n")
    db.view_all_kills()

def view_kills_by_monster_cli(db):
    print("\n\n--- VIEWING KILLS BY MONSTER ---\n\n")
    monster_name = input("\nEnter the Monster Kills you wish to view: ").strip().lower()
    db.view_kills_by_monster(monster_name)

def view_by_item_quality_cli(db):
    print("\n\n--- SEARCHING ITEMS BY QUALITY ---")

    while True:
        print("\n 'q' 'quit' - Back to main menu OR 'item quality' to view items")
        user_input = input().strip().lower()
        
        if user_input in ["q", "quit"]:
            print("\n Returning to the main menu")
            return
        else:
            if not user_input in db.item_qualities:
                print("\nNo quality by that name found in the db")
                break
            else:
                db.view_items_by_quality(user_input)
                db.view_drop_chance_by_quality(user_input)
                break


def main():
    print("\n\n\n\n\n\t\t\t\t--- BRIGHTER SHORES MONSTER DROP TABLE V1.0 ---\n\n")
    db = MonsterDropTable()

    while True:
        print("Options:  T - Track Kills  VA - View all kill data  VM - View kill data by monster  VC - View by item quality  Q - Quit program\n=> ")
        user_input = input().strip().upper()

        if user_input == "T":
            track_kills(db)
        elif user_input == "VA":
            view_all_kills_cli(db)
        elif user_input == "VM":
            view_kills_by_monster_cli(db)
        elif user_input == "VC":
            view_by_item_quality_cli(db)
        elif user_input == "Q":
            print("\n...exiting....\n....")
            break
    
    db.close_db()

main()
