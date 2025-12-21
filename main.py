
import random
import textwrap
import keyboard

#region Constants ("enums"):

TOTAL_LINE_W = 150

NIFFY_W = 26*2
NIFFY_H = 26*2

GAME_STATE_CHOOSE_CHARS = 0
GAME_STATE_MAIN = 1
GAME_STATE_ACCESS_INV = 2
GAME_STATE_PRINT_BIO = 3

ENUM_LOCATION_NIFFY = 0
ENUM_LOCATION_PLANET = 1
ENUM_LOCATION_ASTARES = 2
ENUM_LOCATION_SPACE = 3
ENUM_LOCATION_BATTLESHIP = 4
ENUM_LOCATION_NIFFY_SHUTTLE = 5
ENUM_LOCATION_ESCAPE_POD = 6
ENUM_LOCATION_RAPTOR = 7
ENUM_LOCATION_MOON_PALE = 8
ENUM_LOCATION_PIRATE_SHIP = 9
ENUM_LOCATION_DERELICT = 10
ENUM_LOCATION_GARBAGE_FREIGHTER = 11
ENUM_LOCATION_PLANET_SHUTTLE = 12
ENUM_LOCATION_MOON_DARK = 13
ENUM_LOCATION_MOON_RED = 14

ENUM_ROOM_NIFFY_CORRIDOR_BASIC_EAST_WEST = 0
ENUM_ROOM_NIFFY_STASIS_CHAMBER = 1 #This is where our players start the game. Also can insert badly injured or infected players in here and they will remain safe and ignored by enemies. Requires someone else to open again however.
ENUM_ROOM_NIFFY_COMMISSARY = 2 #Can find food for free here, or pay for it
ENUM_ROOM_NIFFY_BARRACKS = 3
ENUM_ROOM_NIFFY_ARMORY = 4 #Can find weapons for free here
ENUM_ROOM_NIFFY_SEC_ROOM = 5 #Can lock or open doors from here
ENUM_ROOM_NIFFY_BRIDGE = 6 #Can use sensors from here to locate enemies throughout the map, and can also direct the ship toward another location in the game, such as the planet, one of its moons, the battleship, etc.
ENUM_ROOM_NIFFY_ENVIRONMENTAL_CONTROL = 7 #Can vent or pressurize rooms from here, thereby suffocating enemies, fires, and toxic gas
ENUM_ROOM_NIFFY_AIRLOCK = 8 #Allows access to outside of ship
ENUM_ROOM_NIFFY_MEDBAY = 9 #Can exchange technology for healing items
ENUM_ROOM_NIFFY_ENGINE_ROOM = 10 #Powers or unpowers rooms in the game, must be operated to be used.
ENUM_ROOM_NIFFY_SHUTTLE_BAY = 11 #Can provide win scenario if a certain amount of scrap and/or technology is invested
ENUM_ROOM_NIFFY_ENGINEERING_BAY = 12 #Can fabricate new items and equipment here
ENUM_ROOM_NIFFY_CREW_QUARTERS = 13 #Can sleep here at the cost of food to regain some hp and sanity; can only be every 10-20 turns
ENUM_ROOM_NIFFY_SUPPLY_CLOSET = 14 #Can find free useful items
ENUM_ROOM_NIFFY_HYDROPONICS_LAB = 15 #Can slowly grow food here
ENUM_ROOM_NIFFY_OFFICERS_LOUNGE = 16
ENUM_ROOM_NIFFY_COMMUNICATION_STATION = 17 #Can broadcast for help from here (invites Pirates faster), can also create sounds in powered rooms where there are no characters in order to lure enemies there
ENUM_ROOM_NIFFY_ARBORETUM = 18 #High concentration of enemies here
ENUM_ROOM_NIFFY_STORAGE_ROOM = 19 #Can find scrap and tech here
ENUM_ROOM_NIFFY_LABORATORY = 20 #Can perform experiments on enemies here (dead or alive) to learn about their vulnerabilities.
ENUM_ROOM_NIFFY_REC_ROOM = 21
ENUM_ROOM_NIFFY_GROWTH_VATS = 22
ENUM_ROOM_NIFFY_ROBOTICS_BAY = 23
ENUM_ROOM_NIFFY_STORAGE_LOCKER = 24 #At the cost of credits, can store items here to retrieve between runs
ENUM_ROOM_NIFFY_RECYCLER = 25 #Can exchange resources here: scrap, technology and items for credits
ENUM_ROOM_NIFFY_ASTROMETRICS = 26
ENUM_ROOM_NIFFY_ANIMAL_LAB = 27
ENUM_ROOM_NIFFY_READY_ROOM = 28 #Can view upcoming crisis events from here
ENUM_ROOM_NIFFY_COMPUTER_CORE = 29 #This room has a terminal from which you can remotely OPERATE other rooms, if you pass a science skill test. Characters only have to pass this skill check once until they move again.
ENUM_ROOM_NIFFY_INTERSECTION = 30 #Like the corridor but contains more doors.
ENUM_ROOM_NIFFY_CORRIDOR_SR_WEST = 31
ENUM_ROOM_NIFFY_CORRIDOR_SR_EAST = 32
ENUM_ROOM_NIFFY_CORRIDOR_BASIC_NORTH_SOUTH = 33
ENUM_ROOM_VACUUM = -1 #This is what each location grid is initialized to start

ENUM_ITEM_FLASHLIGHT = 0
ENUM_ITEM_SHOTGUN = 1
ENUM_ITEM_BALLISTIC_PISTOL = 2
ENUM_ITEM_LASER_PISTOL = 3
ENUM_ITEM_SNIPER_RIFLE = 4
ENUM_ITEM_MOP = 5
ENUM_ITEM_FIRE_AXE = 6
ENUM_ITEM_TORQUE_WRENCH = 7
ENUM_ITEM_SUB_MACHINE_GUN = 8
ENUM_ITEM_LASER_RIFLE = 9
ENUM_ITEM_FLAME_THROWER = 10
ENUM_ITEM_GRENADES = 11
ENUM_ITEM_ROCKET_LAUNCHER = 12
ENUM_ITEM_LEAD_PIPE = 13
ENUM_ITEM_ASSAULT_RIFLE = 14
ENUM_ITEM_EMP_GRENADES = 15
ENUM_ITEM_MOTION_DETECTOR = 16
ENUM_ITEM_MEDKIT = 17
ENUM_ITEM_NANITE_INJECTOR = 18
ENUM_ITEM_TASER = 19
ENUM_ITEM_DNA_TESTER = 20
ENUM_ITEM_TRICORDER = 21
ENUM_ITEM_FIRE_EXTINGUISHER = 22
ENUM_ITEM_SUIT_ENVIRONMENTAL = 23
ENUM_ITEM_SUIT_MARINE = 24
ENUM_ITEM_SUIT_VACUUM = 25
ENUM_ITEM_SHIELD_BELT = 26
ENUM_ITEM_PRISONER_JUMPSUIT = 27
ENUM_ITEM_ENGINEER_GARB = 28
ENUM_ITEM_MEDICAL_SCRUBS = 29
ENUM_ITEM_SCIENTIST_LABCOAT = 30
ENUM_ITEM_OFFICER_JUMPSUIT = 31
ENUM_ITEM_CIVILIAN_JUMPSUIT = 32
ENUM_ITEM_FLAK_ARMOR = 33
ENUM_ITEM_ADRENAL_PEN = 34
ENUM_ITEM_TARGETING_HUD = 35
ENUM_ITEM_TOTAL_ITEMS = 36

ENUM_CHARACTER_MERCENARY_MECH = 0 #Sec - Comes equipped with built-in hand-flamer, laser, and wrist rockets which use ability points rather than ammunition.
ENUM_CHARACTER_GAMER = 1 #Survivor - Hacker, gamer, a girl
ENUM_CHARACTER_ENGINEER = 2 #Engineer - Can interact with engineering bay in useful ways.
ENUM_CHARACTER_MECH_MAGICIAN = 3 #Engineer - A 'summoner': Can transform scrap into useful droids.
ENUM_CHARACTER_SCIENTIST = 4 #Scientist
ENUM_CHARACTER_CRIMINAL = 5 #Survivor; aka 'The Werewolf' - slowly transforms and will eventually turn on the player.
ENUM_CHARACTER_SERVICE_DROID = 6 #Scientist
ENUM_CHARACTER_OGRE = 7 #Sec - Tanky melee damage dealer, has
ENUM_CHARACTER_JANITOR = 8 #Survivor - Comes equipped with a mop (clears various harmful slimes and sludges) and a fire extinguisher, as well as a few key cards. Is otherwise useless.
ENUM_CHARACTER_PLAYBOY = 9 #Civilian - Is generally useless but a wealthy prince, gives extra completion points if you finish the game with him.
ENUM_CHARACTER_CEO = 10 #Civilian - Is secretly a traitor?
ENUM_CHARACTER_BIOLOGIST = 11 #Scientist - Can interact with the laboratory in useful ways
ENUM_CHARACTER_SOLDIER = 12 #Security - Standard and basic security choice, comes equipped with high quality items but is otherwise not exceptional.
ENUM_CHARACTER_MAX_CHARS = 13

ENUM_SCAVENGE_RESOURCE_TECH_BASIC = 0
ENUM_SCAVENGE_RESOURCE_TECH_ADVANCED = 1
ENUM_SCAVENGE_RESOURCE_FOOD = 2
ENUM_SCAVENGE_RESOURCE_CREDITS = 3
ENUM_SCAVENGE_RESOURCE_FUEL_ENGINE = 4
ENUM_SCAVENGE_RESOURCE_AMMO = 5
ENUM_SCAVENGE_TOTAL_RESOURCES = 6

ENUM_DOOR_UNLOCKED = 0
ENUM_DOOR_LOCKED = 1
ENUM_DOOR_JAMMED = 2

ENUM_FEATURE_NIFFY_SR_PIPE_LEAKY = 0
ENUM_FEATURE_NIFFY_VALVE_BRONZE_BROKEN = 1
ENUM_FEATURE_NIFFY_VALVE_STEEL_BROKEN = 2
ENUM_FEATURE_ALIEN_EGG_SACK = 3

ENUM_HAZARD_GAS_TOXIC = 0
ENUM_HAZARD_GAS_VACUUM = 1
ENUM_HAZARD_FIRE = 2
ENUM_HAZARD_ELECTRIC_CURRENT = 3

ENUM_EQUIP_SLOT_BODY = 0
ENUM_EQUIP_SLOT_ACCESSORY = 1
ENUM_EQUIP_SLOT_HANDS = 2
ENUM_EQUIP_SLOT_TOTAL_SLOTS = 3 #Any element at or beyond this index in the character.inv_list should be considered to be an instance of an item.

ENUM_ITEM_STAT_BOOST_SECURITY = 0
ENUM_ITEM_STAT_BOOST_ENGINEERING = 1
ENUM_ITEM_STAT_BOOST_SCIENCE = 2
ENUM_ITEM_STAT_BOOST_STEALTH = 3
ENUM_ITEM_STAT_BOOST_STRENGTH = 4
ENUM_ITEM_STAT_BOOST_WISDOM = 5
ENUM_ITEM_STAT_BOOST_INTELLIGENCE = 6
ENUM_ITEM_STAT_BOOST_DEXTERITY = 7
ENUM_ITEM_STAT_BOOST_ACCURACY = 8
ENUM_ITEM_STAT_BOOST_HP = 9
ENUM_ITEM_STAT_BOOST_SANITY = 10
ENUM_ITEM_STAT_BOOST_ACTION_POINTS = 11
ENUM_ITEM_STAT_BOOST_ABILITY_POINTS = 12
ENUM_ITEM_STAT_BOOST_SCAVENGING = 13
ENUM_ITEM_STAT_BOOST_ARMOR = 14
ENUM_ITEM_STAT_BOOST_EVASION = 15
ENUM_ITEM_STAT_BOOST_FIRE_RES = 16
ENUM_ITEM_STAT_BOOST_GAS_RES = 17
ENUM_ITEM_STAT_BOOST_VACUUM_RES = 18
ENUM_ITEM_STAT_BOOST_ELECTRIC_RES = 19
ENUM_ITEM_STAT_BOOST_TOTAL_STATS = 20

#endregion

if __name__ == '__main__':

    escape_was_pressed = False

    def handle_escape_release(event):
        global escape_was_pressed
        escape_was_pressed = True

    #region Define functions

    def return_val_in_list(ar_to_search,val_to_find):
        for i in ar_to_search:
            if i == val_to_find:
                return True

        return False

    #endregion

    #region Define global vars:

    game_end = False
    print_room_recap = True

    cur_char = -1

    cur_game_state = GAME_STATE_CHOOSE_CHARS

    #Global resources:
    basic_tech_total = 0
    advanced_tech_total = 0
    credits_total = 0
    food_total = 0
    fuel_total = 0 #Called 'neutronium' fuel, used for niffy engine
    ammo_total = 0

    #endregion

    #region Define classes:

    class Character:

        #region Constructor event for character stats:
        def __init__(self, char_type_enum, spawn_grid_x, spawn_grid_y, spawn_grid):

            #Default values for instance vars for this particularly character:
            self.strength = 0
            self.intelligence = 0
            self.wisdom = 0
            self.dexterity = 0
            self.accuracy = 0
            self.stealth = 0

            self.security = 0
            self.engineering = 0
            self.science = 0
            self.scavenging = 0 #Not currently used

            self.hp_cur = 0
            self.hp_max = 0
            self.ability_points_cur = 0
            self.ability_points_max = 0
            self.sanity_cur = 0
            self.sanity_max = 0

            self.armor = 0
            self.evasion = 0
            self.res_fire = 0
            self.res_vacuum = 0
            self.res_gas = 0
            self.res_electric = 0

            self.action_points = 2

            self.inv_list = []

            self.name = "Not defined"

            #Initialize inv_list and nested ENUM_EQUIP_BACKLIST_LIST:
            for i in range(0,ENUM_EQUIP_SLOT_TOTAL_SLOTS):
                self.inv_list.append(-1)

            self.char_type_enum = char_type_enum
            self.current_grid = spawn_grid
            self.cur_grid_x = spawn_grid_x
            self.cur_grid_y = spawn_grid_y

            if char_type_enum == ENUM_CHARACTER_OGRE:

                self.name = "Cragos, 'The Ogre'"
                self.hp_max = 16
                self.hp_cur = 16
                self.ability_points_cur = 5
                self.ability_points_max = 5
                self.sanity_cur = 10
                self.sanity_max = 10

                self.engineering = 1
                self.security = 5
                self.science = 0
                self.scavenging = 0
                self.stealth = 0

                self.strength = 7
                self.intelligence = 0
                self.wisdom = 1
                self.dexterity = 0

                self.armor = 1

                #Starting equipment:
                #item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
                #self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)
                item_to_equip = Item(ENUM_ITEM_SUIT_MARINE)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum, True)

            elif char_type_enum == ENUM_CHARACTER_BIOLOGIST:
                self.name = "Revita, 'The Biologist'"
                self.hp_max = 6
                self.hp_cur = 6
                self.ability_points_cur = 3
                self.ability_points_max = 3
                self.sanity_cur = 8
                self.sanity_max = 8

                self.engineering = 2
                self.security = 0
                self.science = 5
                self.scavenging = 0
                self.stealth = 2

                self.strength = 0
                self.intelligence = 5
                self.wisdom = 3
                self.dexterity = 0

                #Starting equipment
                item_to_equip = Item(ENUM_ITEM_MEDICAL_SCRUBS)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)
                item_to_equip = Item(ENUM_ITEM_MEDKIT)
                self.add_item_to_backpack(item_to_equip, True)

            elif char_type_enum == ENUM_CHARACTER_ENGINEER:
                self.name = "Amos, 'The Engineer'"
                self.hp_max = 8
                self.hp_cur = 8
                self.ability_points_cur = 4
                self.ability_points_max = 4
                self.sanity_cur = 6
                self.sanity_max = 6

                self.engineering = 5
                self.security = 0
                self.science = 2
                self.scavenging = 0
                self.stealth = 1

                self.strength = 2
                self.intelligence = 2
                self.wisdom = 3
                self.dexterity = 1

                #Starting equipment
                #item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
                #self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)
                item_to_equip = Item(ENUM_ITEM_SUIT_ENVIRONMENTAL)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum, True)

            elif char_type_enum == ENUM_CHARACTER_JANITOR:
                self.name = "Johns, 'The Janitor'"
                self.hp_max = 7
                self.hp_cur = 7
                self.ability_points_cur = 5
                self.ability_points_max = 5
                self.sanity_cur = 6
                self.sanity_max = 6

                self.engineering = 2
                self.security = 0
                self.science = 0
                self.scavenging = 5
                self.stealth = 4

                self.strength = 2
                self.intelligence = 2
                self.wisdom = 2
                self.dexterity = 2

                # Starting equipment
                item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_MECH_MAGICIAN:
                self.name = "Avia, 'The Mechanician'"
                self.hp_max = 5
                self.hp_cur = 5
                self.ability_points_cur = 3
                self.ability_points_max = 3
                self.sanity_cur = 10
                self.sanity_max = 10

                self.engineering = 3
                self.security = 1
                self.science = 2
                self.scavenging = 1
                self.stealth = 2

                self.strength = 1
                self.intelligence = 3
                self.wisdom = 3
                self.dexterity = 1

                self.res_fire = 50
                self.res_vacuum = 50
                self.res_gas = 50
                self.res_electric = -50

                # Starting equipment
                item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_MERCENARY_MECH:
                self.name = "Torvald, 'The Cyborg'"
                self.hp_max = 12
                self.hp_cur = 12
                self.ability_points_cur = 8
                self.ability_points_max = 8
                self.sanity_cur = 10
                self.sanity_max = 10

                self.engineering = 1
                self.security = 4
                self.science = 1
                self.scavenging = 1
                self.stealth = 1

                self.strength = 4
                self.intelligence = 2
                self.wisdom = 1
                self.dexterity = 1

                self.armor = 1

                self.res_fire = 50
                self.res_vacuum = 50
                self.res_gas = 50
                self.res_electric = -50

                # Starting equipment
                item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_SOLDIER:
                self.name = "Cooper, 'The Security Guard'"
                self.hp_max = 10
                self.hp_cur = 10
                self.ability_points_cur = 14
                self.ability_points_max = 14
                self.sanity_cur = 9
                self.sanity_max = 9

                self.engineering = 1
                self.security = 4
                self.science = 0
                self.scavenging = 2
                self.stealth = 1

                self.strength = 3
                self.intelligence = 1
                self.wisdom = 2
                self.dexterity = 2

                # Starting equipment
                item_to_equip = Item(ENUM_ITEM_FLAK_ARMOR)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)
                item_to_equip = Item(ENUM_ITEM_ASSAULT_RIFLE)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)
                item_to_equip = Item(ENUM_ITEM_TARGETING_HUD)
                self.equip_item(item_to_equip, item_to_equip.equip_slot_enum, True)
                item_to_equip = Item(ENUM_ITEM_BALLISTIC_PISTOL)
                self.add_item_to_backpack(item_to_equip,True)
                item_to_equip = Item(ENUM_ITEM_TASER)
                self.add_item_to_backpack(item_to_equip,True)
                item_to_equip = Item(ENUM_ITEM_FLASHLIGHT)
                self.add_item_to_backpack(item_to_equip,True)
                item_to_equip = Item(ENUM_ITEM_ADRENAL_PEN)
                self.add_item_to_backpack(item_to_equip,True)
                item_to_equip = Item(ENUM_ITEM_SUIT_MARINE)
                self.add_item_to_backpack(item_to_equip, True)

            elif char_type_enum == ENUM_CHARACTER_SCIENTIST:
                self.name = "Darius, 'The Physicist'"
                self.hp_max = 5
                self.hp_cur = 5
                self.ability_points_cur = 3
                self.ability_points_max = 3
                self.sanity_cur = 6
                self.sanity_max = 6

                self.engineering = 0
                self.security = 0
                self.science = 6
                self.scavenging = 1
                self.stealth = 3

                self.strength = 3
                self.intelligence = 1
                self.wisdom = 2
                self.dexterity = 2

                item_to_equip = Item(ENUM_ITEM_SCIENTIST_LABCOAT)
                self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_CRIMINAL:
                self.name = "Emeran, 'The Criminal'"
                self.hp_max = 9
                self.hp_cur = 9
                self.ability_points_cur = 12
                self.ability_points_max = 12
                self.sanity_cur = 9
                self.sanity_max = 9

                self.engineering = 0
                self.security = 3
                self.science = 0
                self.scavenging = 4
                self.stealth = 4

                self.strength = 4
                self.intelligence = 0
                self.wisdom = 0
                self.dexterity = 4

                item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
                self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_SERVICE_DROID:
                self.name = "RG-88, 'Service Droid'"
                self.hp_max = 14
                self.hp_cur = 14
                self.ability_points_cur = 15
                self.ability_points_max = 15
                self.sanity_cur = 10
                self.sanity_max = 10

                self.engineering = 3
                self.security = 2
                self.science = 3
                self.scavenging = 0
                self.stealth = 0

                self.strength = 0
                self.intelligence = 4
                self.wisdom = 4
                self.dexterity = 0

                self.res_fire = 100
                self.res_vacuum = 100
                self.res_gas = 100
                self.res_electric = -100

            elif char_type_enum == ENUM_CHARACTER_CEO:
                self.name = "Jens, 'The CEO'"
                self.hp_max = 7
                self.hp_cur = 7
                self.ability_points_cur = 8
                self.ability_points_max = 8
                self.sanity_cur = 4
                self.sanity_max = 4

                self.engineering = 2
                self.security = 0
                self.science = 2
                self.scavenging = 3
                self.stealth = 2

                self.strength = 1
                self.intelligence = 3
                self.wisdom = 2
                self.dexterity = 1

                item_to_equip = Item(ENUM_ITEM_OFFICER_JUMPSUIT)
                self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_GAMER:
                self.name = "Kira, 'The Gamer'"
                self.hp_max = 3
                self.hp_cur = 3
                self.ability_points_cur = 6
                self.ability_points_max = 6
                self.sanity_cur = 5
                self.sanity_max = 5

                self.engineering = 1
                self.security = 0
                self.science = 1
                self.scavenging = 5
                self.stealth = 5

                self.strength = 0
                self.intelligence = 2
                self.wisdom = 1
                self.dexterity = 5

                item_to_equip = Item(ENUM_ITEM_CIVILIAN_JUMPSUIT)
                self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)

            elif char_type_enum == ENUM_CHARACTER_PLAYBOY:
                self.name = "Oberon, 'The Playboy'"
                self.hp_max = 8
                self.hp_cur = 8
                self.ability_points_cur = 6
                self.ability_points_max = 6
                self.sanity_cur = 3
                self.sanity_max = 3

                self.engineering = 0
                self.security = 0
                self.science = 0
                self.scavenging = 3
                self.stealth = 3

                self.strength = 2
                self.intelligence = 2
                self.wisdom = 1
                self.dexterity = 3

                item_to_equip = Item(ENUM_ITEM_CIVILIAN_JUMPSUIT)
                self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)

        #endregion

        def print_char_inv(self):

            print(f"{self.name} is wearing and carrying the following items:")

            #Print body slot:
            item_slot_str = "Nothing"
            if isinstance(self.inv_list[ENUM_EQUIP_SLOT_BODY], Item):
                item_slot_str = self.inv_list[ENUM_EQUIP_SLOT_BODY].item_name
            print(f"Wearing on body: 0.) {item_slot_str}")

            #Print accessory slot:
            item_slot_str = "Nothing"
            if isinstance(self.inv_list[ENUM_EQUIP_SLOT_ACCESSORY], Item):
                item_slot_str = self.inv_list[ENUM_EQUIP_SLOT_ACCESSORY].item_name
            print(f"Also wearing: 1.) {item_slot_str}")

            #Print Hands slot:
            item_slot_str = "Nothing"
            if isinstance(self.inv_list[ENUM_EQUIP_SLOT_HANDS], Item):
                item_slot_str = self.inv_list[ENUM_EQUIP_SLOT_HANDS].item_name
            print(f"Wielding in hands: 2.) {item_slot_str}")

            #Print backpack items
            print("They are carrying on their person:")

            for i in range(ENUM_EQUIP_SLOT_TOTAL_SLOTS,len(self.inv_list)):
                if isinstance(self.inv_list[i], Item): #If there's actually an item here
                    print(f"{i}.) {self.inv_list[i].item_name}")
                else:
                    #print for debug purposes:
                    print(f"{self.inv_list[i]}")

            print("")
            print("Simply enter the associated number to use, equip, unequip, or swap an item; or enter 'BACK' to leave the inventory screen.")
            print("You can also enter 'L{ITEM NUMBER} to get a description of the corresponding item;")
            print("Or 'D{ITEM NUMBER} to drop the item back into your current room (you could retrieve it again with 'SCAVENGE').")
            print("Enter your selection now:")

        def equip_item(self,item_inst_id,item_index,starting_equip_boolean = False):
            if item_inst_id.equip_slot_enum != -1:
                self.inv_list[item_inst_id.equip_slot_enum] = item_inst_id
                # Only remove from backpack if item_index points to a backpack slot; this is necessary because when we're adding an item
                # for the first time as part of a character's starting kit, it doesn't yet exist as one of the 'backpack slots'
                if item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS and item_index < len(self.inv_list):
                    #Remove corresponding position in list, this should be one of the 'backpack' indices:
                    del self.inv_list[item_index]
            else:
                print(f"equip_item method for {cur_char.name} with item: {item_inst_id.item_name}, equip_slot_enum == -1, which means we're trying to equip an item that is not equippable, something went wrong.")
            if not starting_equip_boolean:
                print(f"{self.name} has equipped the {item_inst_id.item_name}")
            if item_inst_id.changes_stats_boolean:
                self.change_char_stats(item_inst_id, True,starting_equip_boolean)

        def unequip_item(self,item_inst_id,starting_equip_boolean = False):
            #Remove from current list position, add to end of list:
            self.inv_list[item_inst_id.equip_slot_enum] = -1
            #add to end of list:
            self.inv_list.append(item_inst_id)
            print(f"{self.name} has unequipped the {item_inst_id.item_name}")
            if item_inst_id.changes_stats_boolean:
                self.change_char_stats(item_inst_id, False,starting_equip_boolean)

        def swap_equip_item(self,first_item_id,first_item_index,second_item_id,second_item_index,starting_equip_boolean = False):
            self.inv_list[first_item_index] = second_item_id
            self.inv_list[second_item_index] = first_item_id
            print(f"{self.name} has unequipped the {first_item_id.item_name}, and equipped the {second_item_id.item_name}")
            if first_item_id.changes_stats_boolean:
                self.change_char_stats(first_item_id,False,starting_equip_boolean)
            if second_item_id.changes_stats_boolean:
                self.change_char_stats(second_item_id, True,starting_equip_boolean)

        def add_item_to_backpack(self,item_id_to_add,starting_equip_boolean = False):
            self.inv_list.append(item_id_to_add)
            if not starting_equip_boolean:
                print(f"{self.name} has picked up the {item_id_to_add.item_name}")

        def drop_item_into_room(self,item_id,item_index,room_inst_id):
            #Change stats:
            if item_id.changes_stats_boolean == True:
                self.change_char_stats(item_id,False, False)
            if item_index < ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                self.inv_list[item_index] = -1 #Change corresponding slot to 'empty'
            elif item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                #Delete corresponding position in one of the 'backpack slots':
                del self.inv_list[item_index]
            #Add to room scavenge list:
                #Create scavenge_resource_list for room_inst_id:
            if isinstance(room_inst_id.scavenge_resource_list, list) == False:
                room_inst_id.scavenge_resource_list = []
                for i in range(0,ENUM_EQUIP_SLOT_TOTAL_SLOTS):
                    room_inst_id.scavenge_resource_list.append(-1)
                room_inst_id.scavenge_resource_list.append(item_id)
            else:
                #Extend the length of the room_inst_id.scavenge_resource_list if necessary, adding -1 to non-existant indices:
                """
                if len(room_inst_id.scavenge_resource_list) <= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                    # The '*' here is an overloaded operand and doesn't actually represent multiplcation; it represents 'copying' a list element that many times, in this case: [-1] is copied into the list a certain amount of times until the length is exactly where we want it
                    room_inst_id.scavenge_resource_list.extend([-1] * (ENUM_EQUIP_SLOT_TOTAL_SLOTS - len(room_inst_id.scavenge_resource_list)))
                """
                # Now append item_id (which will be at either index ENUM_EQUIP_SLOT_TOTAL_SLOTS if we extended our list match, or beyond that at the end of the list, if the len of the list was already > ENUM_EQUIP_SLOT_TOTAL_SLOTS)
                room_inst_id.scavenge_resource_list.append(item_id)

            print(f"{self.name} has dropped the {item_id.item_name}. It can be retrieved again from this room using the 'SCAVENGE' command.")
            print("")

        def change_char_stats(self,item_id,equipping_boolean,starting_equip_boolean):
            #If equipping_boolean == false, we're ADDING the effect of the item stat
            #elif equipping_boolean == True, we're REMOVING the effect of the item stat
            addition_int = 1
            if not equipping_boolean:
                addition_int = -1
            #region Iterate through stat_boost_list, adding/removing the corresponding stat from the char_inst:
            mod_amount_list = []
            stat_str_list = []
            for i in range(0,len(item_id.stat_boost_list)):
                #Define mod amount:
                mod_amount = item_id.stat_boost_list[i] * addition_int

                if i == ENUM_ITEM_STAT_BOOST_HP and mod_amount != 0:
                    stat_str_list.append("Maximum Hit Points")
                    mod_amount_list.append(str(mod_amount))
                    self.hp_max += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_SCAVENGING and mod_amount != 0:
                    stat_str_list.append("Maximum Hit Points")
                    mod_amount_list.append(str(mod_amount))
                    self.scavenging += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_ACCURACY and mod_amount != 0:
                    stat_str_list.append("Accuracy")
                    mod_amount_list.append(str(mod_amount))
                    self.accuracy += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_SECURITY and mod_amount != 0:
                    stat_str_list.append("Security")
                    mod_amount_list.append(str(mod_amount))
                    self.security += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_ENGINEERING and mod_amount != 0:
                    stat_str_list.append("Engineering")
                    mod_amount_list.append(str(mod_amount))
                    self.engineering += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_SCIENCE and mod_amount != 0:
                    stat_str_list.append("Science")
                    mod_amount_list.append(str(mod_amount))
                    self.science += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_STEALTH and mod_amount != 0:
                    stat_str_list.append("Stealth")
                    mod_amount_list.append(str(mod_amount))
                    self.stealth += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_ABILITY_POINTS and mod_amount != 0:
                    stat_str_list.append("Ability Points")
                    mod_amount_list.append(str(mod_amount))
                    self.ability_points_max += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_ACTION_POINTS and mod_amount != 0:
                    stat_str_list.append("Action Points")
                    mod_amount_list.append(str(mod_amount))
                    self.action_points += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_SANITY and mod_amount != 0:
                    stat_str_list.append("Sanity")
                    mod_amount_list.append(str(mod_amount))
                    self.sanity_max += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_STRENGTH and mod_amount != 0:
                    stat_str_list.append("Strength")
                    mod_amount_list.append(str(mod_amount))
                    self.strength += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_DEXTERITY and mod_amount != 0:
                    stat_str_list.append("Dexterity")
                    mod_amount_list.append(str(mod_amount))
                    self.dexterity += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_INTELLIGENCE and mod_amount != 0:
                    stat_str_list.append("Intelligence")
                    mod_amount_list.append(str(mod_amount))
                    self.intelligence += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_WISDOM and mod_amount != 0:
                    stat_str_list.append("Wisdom")
                    mod_amount_list.append(str(mod_amount))
                    self.widsom += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_ARMOR and mod_amount != 0:
                    stat_str_list.append("Armor")
                    mod_amount_list.append(str(mod_amount))
                    self.armor += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_EVASION and mod_amount != 0:
                    stat_str_list.append("Evasion")
                    mod_amount_list.append(str(mod_amount))
                    self.evasion += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_VACUUM_RES and mod_amount != 0:
                    stat_str_list.append("Vacuum Res.")
                    mod_amount_list.append(str(mod_amount))
                    self.res_vacuum += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_GAS_RES and mod_amount != 0:
                    stat_str_list.append("Gas Res.")
                    mod_amount_list.append(str(mod_amount))
                    self.res_gas += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_FIRE_RES and mod_amount != 0:
                    stat_str_list.append("Fire Res.")
                    mod_amount_list.append(str(mod_amount))
                    self.res_fire += mod_amount
                elif i == ENUM_ITEM_STAT_BOOST_ELECTRIC_RES and mod_amount != 0:
                    stat_str_list.append("Electric Res.")
                    mod_amount_list.append(str(mod_amount))
                    self.res_electric += mod_amount

            #endregion
            if not starting_equip_boolean: #Only print any of this if the equipment was used after the game actually started:
                #Concatenate each element in the stat_str_list with each corresponding element in the mod_amount_list:
                joined_stat_str = ""
                for i in range(0,len(stat_str_list)):
                    semicolon_str = ""
                    if i < (len(stat_str_list) - 1):
                        semicolon_str = "; "
                    joined_stat_str += stat_str_list[i]+" by "+mod_amount_list[i]+semicolon_str
                #Combine into result string:
                result_str = f"{self.name} has had their following stats modified: {joined_stat_str}."
                #Wrap string based upon length:
                wrapped_result_str = textwrap.fill(result_str, TOTAL_LINE_W)
                print(wrapped_result_str)

        def print_char_stats(self):
            print(f"{self.name} has the following stats:")
            char_stats_str = f"Security: {self.security}, Engineering: {self.engineering}, Science: {self.science}, Stealth: {self.stealth}, Strength: {self.strength}, Intelligence: {self.intelligence}, Widsom: {self.wisdom}, Dexterity: {self.dexterity}, Accuracy: {self.accuracy}, Vacuum Res.: {self.res_vacuum}, Fire Res.: {self.res_fire}, Electric Res.: {self.res_fire}, Gas Res.: {self.res_gas}."
            char_stats_str = textwrap.fill(char_stats_str, TOTAL_LINE_W)
            print(char_stats_str)
            print("")

    class Item:

        #region Constructor event for item stats:
        def __init__(self,item_enum):

            self.item_enum = item_enum

            self.stat_boost_list = []
            for i in range(0,ENUM_ITEM_STAT_BOOST_TOTAL_STATS):
                self.stat_boost_list.append(0)

            #Default values for instance vars for each item:
            self.dmg_min = 0
            self.dmg_max = 0
            self.requires_ammo_boolean = True
            self.accuracy_bonus = 0
            self.max_range = 0
            self.max_targets = 1  # If == -1, will hit all targets in that distance group
            self.ammo_per_shot = 1

            self.single_use_boolean = False
            self.melee_debuff_boolean = False
            self.equippable_boolean = True
            self.usable_boolean = False
            self.changes_stats_boolean = False

            #None of these are in use and are used within the stat_boost_list instead:
            self.vacuum_res = 0
            self.gas_res = 0
            self.fire_res = 0
            self.electrical_res = 0
            self.armor_bonus = 0
            self.evade_bonus = 0
            self.shield_bonus = 0

            self.item_name = "Not defined"
            self.item_desc = "Not defined"

            self.equip_slot_enum = -1 #Default, this means that this item cannot be equipped: such as medkit, etc.

            if self.item_enum == ENUM_ITEM_FLASHLIGHT:
                self.dmg_min = 1
                self.dmg_max = 1
                self.item_name = "FLASHLIGHT"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_ACCESSORY
            elif self.item_enum == ENUM_ITEM_SHOTGUN:
                self.dmg_min = 3
                self.dmg_max = 6
                self.max_range = 2
                self.ammo_per_shot = 5
                self.max_targets = 3
                self.item_name = "SHOTGUN"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_BALLISTIC_PISTOL:
                self.dmg_min = 1
                self.dmg_max = 4
                self.max_range = 2
                self.ammo_per_shot = 1
                self.item_name = "BALLISTIC PISTOL"
            elif self.item_enum == ENUM_ITEM_LASER_PISTOL:
                self.dmg_min = 1
                self.dmg_max = 3
                self.requires_ammo_boolean = False
                self.max_range = 3
                self.item_name = "LASER PISTOL"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_GRENADES:
                self.dmg_min = 4
                self.dmg_max = 8
                self.max_range = 2
                self.single_use_boolean = True
                self.item_name = "FRAGMENTATION GRENADE"
            elif self.item_enum == ENUM_ITEM_FLAME_THROWER:
                self.max_range = 1
                self.dmg_min = 3
                self.dmg_max = 6
                self.max_targets = -1
                self.item_name = "FLAMETHROWER"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_ROCKET_LAUNCHER:
                self.max_range = 6
                self.dmg_min = 12
                self.dmg_max = 24
                self.max_range = 6
                self.single_use_boolean = True
                self.item_name = "ROCKET LAUNCHER"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_LEAD_PIPE:
                self.dmg_min = 1
                self.dmg_max = 3
                self.requires_ammo_boolean = False
                self.item_name = "LEAD PIPE"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_FIRE_AXE:
                self.dmg_min = 2
                self.dmg_max = 4
                self.requires_ammo_boolean = False
                self.item_name = "FIRE AXE"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_TASER:
                self.dmg_min = 1
                self.dmg_max = 1
                self.requires_ammo_boolean = False
                self.item_name = "TASER"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_ASSAULT_RIFLE:
                self.dmg_min = 5
                self.dmg_max = 10
                self.max_range = 3
                self.requires_ammo_boolean = 3
                self.max_targets = 2
                self.item_name = "ASSAULT RIFLE"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_SNIPER_RIFLE:
                self.dmg_min = 10
                self.dmg_max = 15
                self.max_range = 4
                self.requires_ammo_boolean = 1
                self.max_targets = 1
                self.melee_debuff_boolean = True
                self.item_name = "SNIPER RIFLE"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_HANDS
            elif self.item_enum == ENUM_ITEM_MEDKIT:
                self.max_targets = 1
                self.single_use_boolean = True
                self.usable_boolean = True
                self.item_name = "MED KIT"
                self.equippable_boolean = False
            elif self.item_enum == ENUM_ITEM_SUIT_ENVIRONMENTAL:
                self.fire_res = 50
                self.electrical_res = 50
                self.gas_res = 100
                self.armor_bonus = 1
                self.evade_bonus = -1
                self.item_name = "HAZMAT SUIT"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -1
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 1
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_FIRE_RES] = 50
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ELECTRIC_RES] = 50
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_GAS_RES] = 100
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_PRISONER_JUMPSUIT:
                self.item_name = "PRISONER JUMPSUIT"
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
                self.changes_stats_boolean = True
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
            elif self.item_enum == ENUM_ITEM_ENGINEER_GARB:
                self.item_name = "ENGINEER GARB"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_SCIENTIST_LABCOAT:
                self.item_name = "SCIENTIST LABCOAT"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_MEDICAL_SCRUBS:
                self.item_name = "MEDICAL SCRUBS"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_OFFICER_JUMPSUIT:
                self.item_name = "OFFICER JUMPSUIT"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_CIVILIAN_JUMPSUIT:
                self.item_name = "CIVILIAN JUMPSUIT"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_FLAK_ARMOR:
                self.item_name = "FLAK ARMOR"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 2
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -1
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_SUIT_MARINE:
                self.item_name = "MARINE ARMOR"
                self.equip_slot_enum = ENUM_EQUIP_SLOT_BODY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 5
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ELECTRIC_RES] = 100
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -3
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_VACUUM_RES] = 50
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_GAS_RES] = 100
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_FIRE_RES] = 100
                self.changes_stats_boolean = True
            elif self.item_enum == ENUM_ITEM_ADRENAL_PEN:
                self.max_targets = 1
                self.single_use_boolean = True
                self.usable_boolean = True
                self.item_name = "ADRENAL PEN"
                self.equippable_boolean = False
            elif self.item_enum == ENUM_ITEM_DNA_TESTER:
                self.max_targets = 1
                self.single_use_boolean = True
                self.usable_boolean = True
                self.item_name = "DNA ANALYZER"
                self.equippable_boolean = False
            elif self.item_enum == ENUM_ITEM_TARGETING_HUD:
                self.item_name = "TARGETING H.U.D."
                self.equip_slot_enum = ENUM_EQUIP_SLOT_ACCESSORY
                self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ACCURACY] = 1
                self.changes_stats_boolean = True

        #endregion

        def print_item_desc(self):
            print(f"print_item_desc method called for item with name: {self.item_name}")
            wrapped_item_desc_str = textwrap.fill(self.item_desc, TOTAL_LINE_W)
            print(wrapped_item_desc_str)
            print("")

        def use_item(self):
            print(f"use_item method for item with name: {self.item_name} hasn't been completed yet.\n")

    class Room:

        def __init__(self,location_type_enum,room_type_enum,grid_x,grid_y):

            #Instance vars for each room:
            self.tech_count = 0
            self.credits_count = 0
            self.food_count = 0
            self.cover_int = 0  # 0:none; 1: small amount of cover; 2: medium amount; 3: plenty of useful cover.
            self.powered_status_boolean = False
            self.unpowered_room_desc = "Not defined"
            self.powered_room_desc = "Not defined"
            self.scavenged_once_boolean = False

            # keyword_interaction_dict - used for room feature keywords associated with this room
            self.keyword_interaction_dict = {}

            # directional dictionary
            self.directional_dict = {}

            # Initialize to 0:
            self.scavenge_resource_list = []
            for i in range(0, ENUM_SCAVENGE_TOTAL_RESOURCES):
                self.scavenge_resource_list.append(0)

            self.grid_x = grid_x
            self.grid_y = grid_y
            self.room_type_enum = room_type_enum
            self.location_type_enum = location_type_enum

            if self.location_type_enum == ENUM_LOCATION_NIFFY:
                if self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_BASIC_NORTH_SOUTH:
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = random.randint(0,3)
                    self.unpowered_room_desc = [ "This basic corridor only serves as a connection between two areas on the ship. The floor is metal grating and the walls are dirty panels of burnished steel. A few piles of refuse lay scattered about, evidence of the vessel's disuse." ]
                    self.directional_dict["NORTH"] = ENUM_DOOR_UNLOCKED
                    self.directional_dict["SOUTH"] = ENUM_DOOR_UNLOCKED
                elif self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_BASIC_EAST_WEST:
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = random.randint(0,3)
                    self.unpowered_room_desc = [ "This basic corridor only serves as a connection between two areas on the ship. The floor is metal grating and the walls are dirty panels of burnished steel. A few piles of refuse lay scattered about, evidence of the vessel's disuse." ]
                    self.directional_dict["EAST"] = ENUM_DOOR_UNLOCKED
                    self.directional_dict["WEST"] = ENUM_DOOR_UNLOCKED
                elif self.room_type_enum == ENUM_ROOM_NIFFY_STORAGE_ROOM:
                    self.cover = 2
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = random.randint(0,3)
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_ADVANCED] = 1
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_FOOD] = random.randint(0,2)
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_CREDITS] = random.randint(0,2)
                    self.unpowered_room_desc = [ "Racks of mostly empty shelving and opened boxes indicate that this room was once used for storage. Dust and debris are mostly all that remain. It looks as though the most important items have been pilfered already. The whirling red flare of the emergency lights overhead sends strange shadows pin-wheeling across the room." ]
                elif self.room_type_enum == ENUM_ROOM_NIFFY_HYDROPONICS_LAB:
                    self.cover = 1
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_FOOD] = random.randint(0, 2)
                    self.unpowered_room_desc = [ "Rows and rows of metal grow boxes line the room, their contents nothing more than withered weeds to clutching to dry, gray dirt. There's a nest of hydraulics and hoses in the walls, and huge sunlamps are recessed in the ceiling, now dark and inert. If you can restore power to this room, perhaps there's a way to get these hydroponics working again?" ]
                    self.powered_room_desc = [ "The rows of hydroponics buzz happily with spray from the moisture pumps, while the leafy green vegetables within eagerly drink the light from the sunlamps overhead. These crops of potatoes, beans, and cabbages have clearly been genetically modified to grow quickly." ]
                elif self.room_type_enum == ENUM_ROOM_NIFFY_STASIS_CHAMBER:
                    self.cover = 1
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = 3
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_FOOD] = 15
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_AMMO] = 17
                    self.scavenge_resource_list.append(Item(ENUM_ITEM_SUIT_ENVIRONMENTAL))
                    self.scavenge_resource_list.append(Item(ENUM_ITEM_MEDKIT))

                    self.directional_dict["EAST"] = ENUM_DOOR_JAMMED
                    self.directional_dict["WEST"] = ENUM_DOOR_JAMMED

                    self.unpowered_room_desc = [
                        "Klaxons blare, and an eerie red illumination seeps from the emergency lights in the floor. Row upon row of stasis pods have been arranged in this room, most of them shattered or inoperable. Those corpses who had sought refuge within them have met a truly ignoble end, asphyxiated in their sleep. There's only one STASIS POD that still looks operational and inviting, gleaming pearl-white in the blood-hued gloom.",
                        "The room itself has been badly damaged. Refuse and debris lay scattered about, along with piles of personal effects: whatever non-essential items the sleepers had stripped from their bodies before hastily clamboring within the statis pods to seal their doom.",
                        "Hull stresses and fractures have fissured the walls and ceiling, exposing pipes and electrical wires. One particularly damaged PIPE is rapidly venting a noxious green gas, caustic enough to make you sputter and gag. A nearby exposed service panel reveals two huge circular valves: a BRONZE VALVE and a STEEL VALVE.",
                        "The cover of the service panel looks as though it was torn off with some haste, almost as though someone was determined to access these valves but soon abandoned their task; you can only speculate as to why."
                    ]
                elif self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_SR_WEST:
                    self.cover = 1
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = 1


                    self.directional_dict["EAST"] = ENUM_DOOR_LOCKED
                    self.directional_dict["WEST"] = ENUM_DOOR_JAMMED

                    self.unpowered_room_desc = [
                        "The air smells foul and stuffy in this narrow corridor, and is suffused with the same ominous dim red light. The floor is metal grating and the walls are made up of panels of burnished steel.",
                        "A shadowed and inert form is slumped against the western bulkhead door, as if in peaceful repose. Upon closer inspection, you can see that the man is one of the security forces on board, if his military fatigues and body armor are any indication. You can also see that he is very dead: his eyes stare lifelessly at the jagged hole in his abdomen beneath his flak vest, admiring the great heap of coiled intestines that lay piled between his legs.",
                        "If your eyes aren't mistaken in the gloomy light, there's a strangely colored, green goo clinging to the edges of the gaping wound, and more of it dribbling from his mouth. The CORPSE is also clutching a pistol in a death grip. Judging by the gaping hole in the side of his head, it looks as though his last act was to use the weapon on himself.",
                        "The self-inflicted head wound, combined with the abyss where the man's stomach used to be, has certainly given you pause. Nonetheless, the CORPSE is carrying some useful looking gear, and there could be more in the pockets of his tactical vest. Is it wise to take a closer look?"
                    ]
                elif self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_SR_EAST:
                    self.cover = 1
                    self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = 1

                    self.directional_dict["EAST"] = ENUM_DOOR_LOCKED
                    self.directional_dict["WEST"] = ENUM_DOOR_JAMMED

                    self.unpowered_room_desc = [
                        "There's an NPC in this room."
                    ]

                else:
                    print(f"Constructor event for Room class: room_type_enum: {room_type_enum} not captured by if case for location_type_enum {location_type_enum}")

        def print_room_desc(self):
            if not self.powered_status_boolean:
                for i in self.unpowered_room_desc:
                    room_str = textwrap.fill(i, TOTAL_LINE_W)
                    print(room_str)
                    print("")

            else:
                for i in self.powered_room_desc:
                    room_str = textwrap.fill(i, TOTAL_LINE_W)
                    print(room_str)
                    print("")

        def collect_scavenge_from_room(self,scavenging_char_id):
            global food_total,ammo_total,basic_tech_total,advanced_tech_total,fuel_total, credits_total
            #This will cause our main loop to show any items on the floor in this room:
            self.scavenged_once_boolean = True

            output_str = f"{scavenging_char_id.name} has found the following items in this room:\n"

            for i in range(0,len(self.scavenge_resource_list)):
                if i == ENUM_SCAVENGE_RESOURCE_FOOD:
                    if self.scavenge_resource_list[i] > 0:
                        food_total += self.scavenge_resource_list[i]
                        output_str += f"+{self.scavenge_resource_list[i]} FOOD.\n"
                elif i == ENUM_SCAVENGE_RESOURCE_AMMO:
                    if self.scavenge_resource_list[i] > 0:
                        ammo_total += self.scavenge_resource_list[i]
                        output_str += f"+{self.scavenge_resource_list[i]} AMMUNITION.\n"
                elif i == ENUM_SCAVENGE_RESOURCE_TECH_BASIC:
                    if self.scavenge_resource_list[i] > 0:
                        basic_tech_total += self.scavenge_resource_list[i]
                        output_str += f"+{self.scavenge_resource_list[i]} BASIC TECHNOLOGY.\n"
                elif i == ENUM_SCAVENGE_RESOURCE_TECH_ADVANCED:
                    if self.scavenge_resource_list[i] > 0:
                        advanced_tech_total += self.scavenge_resource_list[i]
                        output_str += f"+{self.scavenge_resource_list[i]} ADVANCED TECHNOLOGY.\n"
                elif i == ENUM_SCAVENGE_RESOURCE_FUEL_ENGINE:
                    if self.scavenge_resource_list[i] > 0:
                        fuel_total += self.scavenge_resource_list[i]
                        plural_s = ""
                        if self.scavenge_resource_list[i] > 1:
                            plural_s = "S"
                        output_str += f"+{self.scavenge_resource_list[i]} NEUTRONIUM FUEL CELL{plural_s}.\n"
                elif i == ENUM_SCAVENGE_RESOURCE_CREDITS:
                    if self.scavenge_resource_list[i] > 0:
                        credits_total += self.scavenge_resource_list[i]
                        plural_s = ""
                        if self.scavenge_resource_list[i] > 1:
                            plural_s = "S"
                        output_str += f"+{self.scavenge_resource_list[i]} CREDIT{plural_s}.\n"
                elif i >= ENUM_SCAVENGE_TOTAL_RESOURCES:
                    #We are now adding items to the scavenging_char_id's inv_list:
                    if isinstance(self.scavenge_resource_list[i], Item):
                        scavenging_char_id.add_item_to_backpack(self.scavenge_resource_list[i])
                        output_str += f"+{self.scavenge_resource_list[i].item_name}.\n"

            #Actually print the massive string we just created:
            print(output_str)

            # Delete the list but keep the variable
            del self.scavenge_resource_list
            self.scavenge_resource_list = -1
            self.scavenge_resource_list = []
            #Initialize:
            for i in range(0,ENUM_SCAVENGE_TOTAL_RESOURCES+1):
                self.scavenge_resource_list.append(-1)

    #endregion

    #region global lists

    pc_char_list = [] #Used for the player's final chosen party
    total_chars_stats_list = [] #Used simply to display char stats
    total_chars_bio_list = [] #Used to display a char's biography

    #endregion

    # region Manually build our location grid for the niffy location:

    # location grid:
    location_grid_niffy = [[0 for _ in range(NIFFY_W)] for _ in range(NIFFY_H)]
    #Initialize each grid coordinate to -1
    for yy in range(0,len(location_grid_niffy)):
        for xx in range(0,len(location_grid_niffy[yy])):
            location_grid_niffy[yy][xx] = ENUM_ROOM_VACUUM

    origin_grid_y = len(location_grid_niffy) // 2
    origin_grid_x = len(location_grid_niffy[0]) // 2

    location_grid_niffy[origin_grid_y][origin_grid_x] = Room(ENUM_LOCATION_NIFFY, ENUM_ROOM_NIFFY_STASIS_CHAMBER,origin_grid_x,origin_grid_y)
    location_grid_niffy[origin_grid_y][origin_grid_x-1] = Room(ENUM_LOCATION_NIFFY,ENUM_ROOM_NIFFY_CORRIDOR_SR_WEST,origin_grid_x-1,origin_grid_y)
    location_grid_niffy[origin_grid_y][origin_grid_x+1] = Room(ENUM_LOCATION_NIFFY,ENUM_ROOM_NIFFY_CORRIDOR_SR_EAST,origin_grid_x+1,origin_grid_y)

    # endregion

    #region Create a temporary copy of each character, use their stats to fill a print list for convenience:

    for i in range(0,ENUM_CHARACTER_MAX_CHARS):
        temp_pc_char = Character(i,0,0,location_grid_niffy)
        primary_role_str = "Undefined"
        char_class_snippet = "Undefined"
        #Now define total_chars_bio_list:
        if i == ENUM_CHARACTER_OGRE:
            total_chars_bio_list.append("Cragos, 'The Ogre':\n\nCragos was intended to be just another of the millions of faceless clones born into servitude by the Kethas Corporation, but a power surge in his gestation vat caused an excessive amount of growth hormone to be released into his developmental stew. As a result, he emerged from his birthing chamber weeks before his brothers and sisters, a hulking giant of a man with the mind of a child, and a misshapen face that only a mother could love... If only he had one.\n\nThe scientists at Keth Corp. were bemused by this unanticipated variant, and rigorously tested his physical and mental capabilities to determine the viability of his strain. They called it 'testing,' but Cragos would come to know the euphimism for what it truly was: torture.\n\nHe was only six weeks old by the time they had subjected him to a battery of tests that included blunt force trauma, precision tissue damage, and unimaginable G-forces, all to determine the tolerances of his physical structure, and also the rate of his healing factor, which surpassed even that of his kin. He was at least spared the psychological conditioning, not by any act of mercy, but merely because he was overlooked and forgotten after the researchers grew bored of his screams, labeling his mutation as 'UNSATISFACTORY.' He was deemed too large and clumsy to be useful on the battlefield, and too hideous to serve as steward in the gilded homes of the elite back in the Core.\n\nHe would have been reprocessed and recycled, in fact, liquified and fed back to his fellow clones as essential nutrients, had the interstellar freighter that was his home not been attacked by raiders from the Fringe. It was of course Keth Corp. policy to never reveal the secrets of their proprietary technology, and so they reduced the massive hulk of their starship to ruins in the depths of space, rather than submit to the pirate's boarding party. The brigands did not leave empty handed, nonetheless.\n\nThey found Cragos still clinging to life in a small pressurized compartment in a field of floating debris, like a cockroach that refused to die, or a caterpillar cocooned in stasis, patiently awaiting chrysalis. Unlike the scientists at Keth Corp., they found good use for his muscle among their ranks, all right.\n\nBanditry was their trade, and his healing factor an invaluable asset. The absence of psychological conditioning had made it possible for Cragos to adjust to their nomadic lifestyle, to view himself as an invidual at last, as a person who could inspire respect--if never love.\n\nThey named him 'Cragos,' after the son of the stone god who ruled the mountains of their homeworld. And as the years passed he became well known as the most vicious and relentless of their clan. Eventually he outlived them all, and when the very last of their clan had been struck down by enforcers from the Core, Cragos struck out into the void to earn his own coin, plying his trade as a mercenary for hire, a dealer of death and punishment alike. Yet he never forgot the faces of his tormentors who had given him life, and always he hoarded the horror of his past as fuel for future conquests.\n\nIt was a kidnapping job gone sideways that found him in a stasis chamber aboard the Keth Corp. research vessel 'Niffy.' And there he remains: a caged animal once more, eyes closed, yet not sleeping--always dreaming of vengeance against the inexhaustible and inexorable corporation that made him... Always dreaming... And always promising pain.\n\nGameplay features: Cragos is a resilient tank who deals double damage with melee weapons and extra damage with his fists. He is very fond of wrestling opponents and dismembering them with his bare hands, often putting himself into compromised positions in order to do so. His RAGE meter builds while fighting and when it reaches 10, he becomes uncontrollable for 6-10 turns, smashing room features, items, or attacking friendly characters. He has poor accuracy when using ranged weapons, and therefore should rely upon weapons that offer multiple hits, such as the shotgun or flame thrower. He is also too large to be able to use the 'HIDE' command. Abilities: Healing Factor: automatically heals 1 hp and 1 infection point every 3-4 turns (passive); Thick Hide: +2 armor value (passive)")
            primary_role_str = "SECURITY"
            char_class_snippet = "This giant brute almost looks like the standard variant of the Keth Corporation clone, only... bigger. Much bigger. Uglier, too."
        elif i == ENUM_CHARACTER_SOLDIER:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGameplay features: As a security character, Cooper excels when buffing allies and pinning enemies down with suppressive fire. His starting kit is effective enough to give him an edge in combat for much of the early game. Abilities: Suppressing fire: 1 AP: For the next turn, any enemy that Cooper targets has a 100% chance of becoming suppressed; Focus Fire: 2 AP: For the next 2-3 turns, all friendly characters in the current battle receive +2 to their accuracy stat; Take Command: 5 AP: All friendly characters in the same room as Cooper reduce their sanity meter by 1.")
            primary_role_str = "SECURITY"
            char_class_snippet = "If the data on his identity tag is any indication, then this poor fellow's contract was nearly up. Judging by his flabby gullet, it looks like he hasn't seen the inside of a gym in years. At least he entered the stasis pod while wearing some decent equipment."
        elif i == ENUM_CHARACTER_PLAYBOY:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "Immediately identifiable is the handsome scion of the rival conglomerate Boros Incorporated, better known for his sexual conquests than his contributions to the family's sterling legacy. What is he doing here?"
        elif i == ENUM_CHARACTER_CRIMINAL:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "The barcode branded across this man's forehead displays his status as nothing more than chattle. It's not difficult to end up on the wrong side of the law as a citizen of any one of the thousands of worlds owned by Keth Corp. What is this man's crime?"
        elif i == ENUM_CHARACTER_GAMER:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGameplay features: Though frail and unable to use weapons, Kira abilities, when combined with her high stealth stat and starting items, can make her an effective scout. She is also the only character small enough to use the ventillation system to travel. The player will receive 10 extra victory points when completing any victory scenario with Kira. Abilties: Hide: 1 AP: Enemies have a 80% chance of ignoring Kira while this ability is active; Scurry: 2 AP: Move to an adjacent, accessible room through an open door without using move points or consuming food. This ability can only be used when Kira is moving alone.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "This unfortunate little girl must have been in the wrong place at the wrong time. Where are her parents?"
        elif i == ENUM_CHARACTER_ENGINEER:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGameplay features: ")
            primary_role_str = "ENGINEER"
            char_class_snippet = "The blue overcoat emblazoned with the Keth Corporation's sigil of a star cresting the shoulder of a shadowed planet all indicate that this is a company man. Someone from the engineering department, most likely."
        elif i == ENUM_CHARACTER_CEO:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "Oh how the mighty have fallen! This face has been seen by almost everyone with a video feed this side of the galaxy. It's Jens, Chief Executive Officer of the interstellar research and development corporation Zephyr Industries. One can only wonder how he lost his first-class seat."
        elif i == ENUM_CHARACTER_SERVICE_DROID:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "ENGINEER"
            char_class_snippet = "This standard service droid has been deactivated for reasons unknown. It is roughly the same size and shape as a man, with a burnished steel frame, articulated joints, and an expressionless face that sports two large mustaches engraved over a mouth slit. It sleeps in the corner of the stasis chamber with the camera lenses of its eyes wide open, seeing nothing. There is some blackened scoring around the junction box on its metal chest; the old scars of laser blasts, no doubt. Is it still operational?"
        elif i == ENUM_CHARACTER_MERCENARY_MECH:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGame play features: Torvald is a versatile fighter who relies heavily upon Ability Points to utilize his built-in weapons. Being cybernetic, he accumulates infection points half as quickly as organic characters, and requires twice as many before transforming. Abilities: 2 AP: Palm Laser (can WELD room features, does light damage to enemies); 4 AP: Hand Flamer (can BURN room features, and does medium damage to groups of enemies); 6 AP: Wrist Rocket (deals medium to high damage to groups of enemies); 1 AP + 1 basic_tech: Improvisational Repair: Heal 2 hp.")
            primary_role_str = "SECURITY"
            char_class_snippet = "Half of this man's face has been replaced by steel plating and electronics. A trans-humanist from the Fringe, then; such modifications are generally outlawed within the Core, especially in worlds owned by the Keth Corporation. Even in sleep he wears a malevolent grin."
        elif i == ENUM_CHARACTER_MECH_MAGICIAN:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "ENGINEER"
            char_class_snippet = "Another trans-humanist, this one more machine than woman. Her skin is deathly pale. Huge metal slits have been carved into the sides of her skull, presumably to vent the massive amount of heat generated by her cybernetically enhanced brain. A clear violation of the Keth Corporation's law against cybernetic enhancement, if ever there was one."
        elif i == ENUM_CHARACTER_BIOLOGIST:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "SCIENTIST"
            char_class_snippet = "This woman is wearing a white lab coat emblazoned with the Keth Corporation's sigil. It is disconcerting to know that she chose refuge here, in a stasis chamber, rather than face head-on whatever terrible crisis has clearly paralyzed this vessel. Surely she must know more about what happened here."
        elif i == ENUM_CHARACTER_JANITOR:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "An older man in the gray overalls of a technician. A company man, by his sigil. He has a nasty looking head wound. Perhaps he saw something before his sense of self-preservation brought him here?"
        elif i == ENUM_CHARACTER_SCIENTIST:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "SCIENTIST"
            char_class_snippet = "Another gray beard in a white lab coat, they seem to populate most star ships--especially those that operate well outside of the known regions of space. This one has an imperious look and a slight sneer, even in stasis."
        else:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
        #Add stats string to total_char_stats_list
        total_chars_stats_list.append(
            f"{i}.) {temp_pc_char.name}: Primary role: {primary_role_str}. {char_class_snippet} Security: {temp_pc_char.security}; Engineering: {temp_pc_char.engineering}; Science: {temp_pc_char.science}; Stealth: {temp_pc_char.stealth}")
        #De-reference (destroy) this instance:
        temp_pc_char = -1
    #endregion

    #region Define help text:

    help_instructions_str_list = [
        "The following is a list of available commands to be used outside of combat:\n",
        "'SCAVENGE': This command can only be used once per room, and will automatically collect any global resources and items that can be found within the room.\n",
        "'E' or 'EAST'; 'W' or 'WEST'; 'N' or 'NORTH'; 'S' or 'SOUTH': Costs 1 action point and 1 food per character. Directional commands to move between rooms. The corresponding direction must be accessible..\n"
        "'UNLOCK {DIRECTION}': Consumes one of your key cards to unlock the door in the corresponding direction.\n",
        "'JAM {DIRECTION}': Costs 1 action point per character. Uses random scrap items found in the room and your character(s) strength to attempt to jam a door in the corresponding direction. A strength-based skill test will ensue to determine if the action was successful.\n",
        "'HIDE': Costs 1 action point to hide the character in the current room, using whatever cover they can find. A stealth-based skill check ensues to determine if this action was successful. Note that the effectiveness of this action is dependent upon the level of cover in the current room, with 'low amounts of cover' providing a 30% chance to remain concealed in the room; 'medium amounts of cover' providing a 60% chance to remain concealed in the room; and 'large amounts of cover' providing a 90% chance to remain concealed in the room.",
        "'AMBUSH': Costs 1 action point to initiate combat against an enemy or enemies in the current room while a character is HIDDEN, giving you a full extra turn against the enemy. Initiating an ambush will also allow to add other currently hidden characters to the combat. If you choose not to add them, they will remain hidden and not participate in the battle.",
        "'INV' or 'INVENTORY': Access the inventory options for the current character",
        "'L' or 'LOOK': Describe the current character's room again and reassess their current status.",
        "'STAT' or 'STATS': Examine each of the current character's statistics.",
        "You will also notice that many rooms contain keywords that represent a feature of the room that the player can interact with. These features are displayed in ALL CAPS and simply entering them will allow you to fully interact with that feature."
    ]

    #endregion

    #region Print intro:
    print("")
    intro_str_list = [
        "Welcome to 'Sector 17', an interactive, science-fiction and horror story generator. Hopefully you enjoy a good read!",
        "In order to survive this scenario, you'll need to use your wits, utilize your party members' strengths, and mitigate their weaknesses.",
        "The ultimate goal is to either escape from section 17 with every party member, or utterly destroy the alien threat that has infested this sector of space.",
        "There are multiple endings and you'll be awarded points at the end of each run depending upon how much you accomplish.",
        "A word of advice: while it is technically possible to beat the game with any party combination, a party that includes a diverse set of skill sets will serve you best. That being said, there is no 'perfect party,' and it is useful to play with every character to learn their strengths and weaknesses--so don't bother deliberating over your first party composition too much!",
        "Good luck!",
    ]

    for i in intro_str_list:
        intro_line = textwrap.fill(i, TOTAL_LINE_W)
        print(intro_line)
        print("")

    any_key = input("Press enter to travel to Sector 17.")
    print("")

    statis_chamber_str_list = [
        "Klaxons blare deep within the metal womb of the spindle-ship 'K.C. Niffy,' adrift somewhere within the endless sea of stars...",
        "... Yet outside the vessel, in the vacuum of the void, there is only silence.",
        "We move closer toward the starship, a jagged splinter tumbling through the abyss...",
        "... Moving closer and closer still...",
        "... Moving through layers of steel hull, insulation, electronics, metal grating...",
        "... Emerging from a ceiling fan into an oval-shaped room, dimly lit with banks of red emergency lighting, recessed within the floor. Here the sound of the klaxons is deafening. The walls of the room have nearly been torn asunder and are shaking from the impact of some distant explosion. Wrent paneling and torn steel reveal the steaming and sparking guts of the ship's infrastructure.",
        "Near the center of the room, raised upon a wide dais, row upon row of stasis pods are gleaming in the gloom like white pearls with red bellies, beckoning us closer.",
        "Above the stasis pods, through glass casings filmed with frost, one can see that most of the sleepers wear placid expressions, totally at ease within their pale cribs, indifferent to the apparent chaos raging all around them.",
        "Three of the occupants, however, are stirring. They seem convinced that these glass cages with their white velvet cushions will not become their coffins. Sweat beads upon their brows. Their features twist and contort, fighting against the ephemeral pull of some discontented dream.",
        "In the shadow of the eerie purgatory light, it is difficult to make out their faces.",
        "Who among them will wake, shaken by the last gasp of a failing power system?...",
        "... And who among them will slip deeper still from slumber, into death?"
    ]

    for i in statis_chamber_str_list:
        intro_line = textwrap.fill(i, TOTAL_LINE_W)
        print(intro_line)
        print("")

    any_key = input("Press enter to peruse the stasis chamber.")
    print("")

    #endregion

    while game_end == False:

        #region Choose chars game state:

        if cur_game_state == GAME_STATE_CHOOSE_CHARS:

            print("Enter a character's number to add them to your party, or type '*' followed by a character's number to learn more about them.")
            print("You can revoke your most recent selection at any time by entering 'BACK'.")
            print("You can also enter '?' to learn more about stats, and the game in general.")
            print("Note: All commands in this game are case insensitive.")
            print("")
            for i in total_chars_stats_list:
                char_stats_str = textwrap.fill(i,TOTAL_LINE_W)
                print(char_stats_str)
                print("")

            user_input = input("Who will awaken?:").upper()
            print("")

            if user_input == "BACK":
                if len(pc_char_list) > 0:
                    removed_char_inst = pc_char_list.pop()
                    print(f"{removed_char_inst.name} has been removed from the party.")
                    print("")
                    del removed_char_inst
            else:
                print_bio = False
                char_select_str = ""

                if user_input.startswith("*"):
                    print_bio = True
                    char_select_str = user_input[1:]  # Everything after the "*"
                else:
                    char_select_str = user_input

                valid_char = False

                try:
                    int_char = int(char_select_str)
                    if int_char >= 0 and int_char < ENUM_CHARACTER_MAX_CHARS:
                        if print_bio == False:
                            duplicate_found = False
                            for i in range(0,len(pc_char_list)):
                                char_inst = pc_char_list[i]
                                if char_inst.char_type_enum == int_char:
                                    valid_char = False
                                    duplicate_found = True
                                    print("You've already added that character to your party, try again.\n")
                                    break
                            if duplicate_found == False:
                                valid_char = True
                        else:
                            valid_char = True
                    else:
                        print("That is not a valid character number.")
                except ValueError:
                    print("You must enter a valid integer.")

                if valid_char == True:
                    if print_bio:
                        cur_game_state = GAME_STATE_PRINT_BIO
                    else:
                        #Add to chosen_pc_chars_list, then check start condition
                        pc_char_list.append(Character(int_char,origin_grid_x,origin_grid_y,location_grid_niffy)) #instantiate char
                        print(f"You have added {pc_char_list[len(pc_char_list)-1].name} to the party.")
                        print("")
                        if len(pc_char_list) == 3:
                            print("... Three silhouettes shamble from the stasis pods in the light of the bloody gloaming, the room quaking all around them...")
                            print("")
                            print("Through bleary eyes, you find yourself in the middle of a chaotic scene:")
                            print("")
                            #Define cur_char and current_grid:
                            cur_char = pc_char_list[0]
                            #change game state:
                            cur_game_state = GAME_STATE_MAIN

        #endregion for game_state == choose_chars

        #region game_state == print_char_bio:

        elif cur_game_state == GAME_STATE_PRINT_BIO:
            #Manually separate string by '\n' escape key into list elements:
            lines_list = total_chars_bio_list[int_char].split('\n\n')
            #Then wrap each each string element within the lines_list if it exceeds the TOTAL_LINE_W by using textwrap.fill which adds \n where appropriate
            wrapped_lines = [textwrap.fill(line, TOTAL_LINE_W) for line in lines_list]
            #Then join the string elements again into a single string, wherever '\n' is found:
            bio_str = '\n\n'.join(wrapped_lines)

            #Finally, print:
            print(bio_str)
            print("")
            any_key = input("Press enter to return to the character selection screen.")

            #Return to character selection:
            cur_game_state = GAME_STATE_CHOOSE_CHARS

        #endregion

        #region game_state == main

        elif cur_game_state == GAME_STATE_MAIN:

            #define location_grid_to_use:
            cur_grid_to_use = cur_char.current_grid

            #Show room description - no need for another line break after this method, the for-loop witin it provides the necessary spaces:
            if print_room_recap:
                cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x].print_room_desc()

                #Print player what global resources the party is currently carrying: basic tech, advanced tech, food, fuel
                print(f"The party is carrying between them the following shared resources: Food: {food_total}, Basic Tech.: {basic_tech_total}, Advanced Tech: {advanced_tech_total}, Ammunition: {ammo_total}, Engine Fuel: {fuel_total}.")
                print("")

                #Tell player which character they are currently inhabiting, along with their primary stats (hp, stamina, sanity):
                print(f"You are {cur_char.name}. You have {cur_char.hp_cur} hit points, {cur_char.ability_points_cur} ability points, {cur_char.sanity_cur} sanity points, {cur_char.armor} armor, and {cur_char.evasion} evasion.")
                print_room_recap = False #Set to false so we don't see all of this again whenever the player performs a trivial action; is reset to True whenever the player moves to a different room, or uses the 'L'ook command:
                print("")

            input_str = input("What will you do?").upper().strip()
            print("")

            #Parse string for logic:
            if input_str == "EXIT":
                print("You have decided to quit the game.")
                game_end = True
            elif input_str == "AMBUSH":
                print("Ambush is not yet implemented.")
            elif input_str == "HIDE":
                print("Hide is not yet implemented.")
            elif input_str == "L" or input_str == "LOOK":
                print_room_recap = True
                print("You take another look around and assess your situation:")
                print("")
            elif input_str == "STAT" or input_str == "STATS":
                cur_char.print_char_stats()
            elif input_str == "SCAVENGE":
                #region Scavenge logic:
                room_scavenge_list = cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x].scavenge_resource_list
                if isinstance(room_scavenge_list, list) and len(room_scavenge_list) > 0:
                    has_resources_boolean = False
                    for i in range(0,len(room_scavenge_list)):
                        if room_scavenge_list[i] != -1:
                            has_resources_boolean = True
                            break

                    if has_resources_boolean:
                        cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x].collect_scavenge_from_room(cur_char)
                    else:
                        print("This room has already been picked clean.\n")
                else:
                    print("There is nothing of value to be found in this room.")
                #endregion
            elif input_str == "INV" or input_str == "INVENTORY":
                cur_game_state = GAME_STATE_ACCESS_INV
            else:
                print("Invalid command, try again.")

        #endregion

        #region access_inv game state

        elif cur_game_state == GAME_STATE_ACCESS_INV:

            cur_char.print_char_inv()

            inv_input_str = input().upper().strip()

            show_item_desc_boolean = False
            drop_item_boolean = False
            valid_selection = False
            item_index = -1

            if inv_input_str == "B" or inv_input_str == "BACK":
                cur_game_state = GAME_STATE_MAIN
                print_room_recap = True

            elif inv_input_str.startswith("L"):
                show_item_desc_boolean = True
                try:
                    item_index = int(inv_input_str[1:])  # Everything after the "L"
                    valid_selection = True
                except ValueError:
                    pass
            elif inv_input_str.startswith("D"):
                drop_item_boolean = True
                try:
                    item_index = int(inv_input_str[1:])  # Everything after the "D"
                    valid_selection = True
                except ValueError:
                    pass
            else:
                try:
                    item_index = int(inv_input_str)
                    valid_selection = True
                except ValueError:
                    pass

            if valid_selection:
                if item_index >= 0 and item_index < len(cur_char.inv_list):
                    #Store item instance id:
                    selected_item = cur_char.inv_list[item_index]
                    if isinstance(selected_item, Item):
                        #'L'ook at item:
                        if show_item_desc_boolean:
                            selected_item.print_item_desc()
                        #'D'rop item:
                        elif drop_item_boolean:
                            cur_char.drop_item_into_room(selected_item,item_index, cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x])
                        # Use item:
                        elif selected_item.usable_boolean == True:
                            selected_item.use_item()
                        else:
                            if selected_item.equippable_boolean == True:
                                #Determine if we need to unequip, equip, swap, or use item:
                                if item_index <= ENUM_EQUIP_SLOT_HANDS:
                                    #Unequip item, if it's already equipped as one of the equipment slots:
                                    cur_char.unequip_item(selected_item)
                                elif item_index > ENUM_EQUIP_SLOT_HANDS:
                                    #Store the index of where the item is supposed to be equipped on the char's equip slots:
                                    selected_item_equip_slot = selected_item.equip_slot_enum
                                    #If that position where this item is supposed to go is already occupied by another item, then swap the positions of the two:
                                    if cur_char.inv_list[selected_item_equip_slot] != -1 and isinstance(cur_char.inv_list[selected_item_equip_slot], Item):
                                        #swap equipped with unequipped item, then equip item:
                                        swapping_item_id = cur_char.inv_list[selected_item_equip_slot]
                                        swapping_item_index = cur_char.inv_list[selected_item_equip_slot].equip_slot_enum
                                        cur_char.swap_equip_item(swapping_item_id,swapping_item_index,selected_item,item_index)
                                    #If that position where this item is supposed to go is empty, then simply move the item to that position:
                                    elif cur_char.inv_list[selected_item_equip_slot] == -1:
                                        #Equip item to an empty slot:
                                        cur_char.equip_item(selected_item,item_index)
                            else:
                                print(f"The {selected_item.item_name} is not an equippable item.")
                    else:
                        print("You must select an item, try again.")
                else:
                    print("Invalid selection, try again.")
            else:
                if cur_game_state != GAME_STATE_MAIN:
                    print("Invalid selection, try again.")

        #endregion