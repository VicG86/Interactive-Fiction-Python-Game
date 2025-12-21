
# Import user made modules
from constants import *
from models.character import Character
from models.item import Item
from models.room import Room

#Import built-in python modules:
import random
import textwrap
import keyboard

print("Imports successful!")

if __name__ == '__main__':

    escape_was_pressed = False

    def handle_escape_release(event):
        global escape_was_pressed
        escape_was_pressed = True

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
                        found_food, found_ammo, found_basic_tech, found_advanced_tech, found_fuel_total, found_credits_total = cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x].collect_scavenge_from_room(cur_char)
                        food_total += found_food
                        ammo_total += found_ammo
                        basic_tech_total += found_basic_tech
                        advanced_tech_total += found_advanced_tech
                        fuel_total += found_fuel_total
                        credits_total += found_credits_total
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