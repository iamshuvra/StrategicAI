# AI Class
# by zax

# This is the main file you will edit. The run_ai function's job
# is to issue two types of commands (see command.py):
# - BuildUnitCommand: asks the game engine to build a specific type
#     of unit at a specific city if the faction has enough cash
#     available.
# - MoveUnitCommand: asks the game engine to move a specific unit
#     in a specific direction. The engine will only move a unit
#     if the destination cell is free. If it is occupied by a friendly
#     unit, nothing happens. If it is occupied by another faction,
#     combat ensues.

from command import *
import random
import unit
import vec2

class AI:
    # init:
    # Currently, the initializer adds nothing to the object.
    #
    # NOTE: AI objects are passed into the Faction initializer
    # when a faction is created (see the gen_factions() function
    # in the main.py file). 
    def __init__(self):
        self.unitCycle=['R', 'P', 'S']


    # run_ai
    # Parameters:
    # - faction_id: this is the faction_id of this AI object.
    #     Use it to access infomation in the other parameters.
    # - factions: dictionary of factions by faction_id.
    # - cities: dictionary of cities stored by faction_id.
    #     For example: cities[faction_id] would return all the
    #     the city objects owned by this faction.
    # - units: dictionary of all units by faction_id.
    #     Similar to the cities dictionary, units[faction_id]
    #     would return all unit objects belonging to the faction.
    # - gmap: the game map object.
    #
    # Return:
    # This function should return a list of commands to be processed
    # by the game engine this turn.
    #
    # NOTE: Every ai has access to ALL game objects.
    
    def run_ai(self, faction_id, factions, cities, units, gmap):

        # A list to hold our commands. This gets returned by
        # the function.
        cmds = []


        # random.shuffle(city_indexes)
        # for ci in city_indexes:
        #     cmd = BuildUnitCommand(faction_id,
        #                        my_cities[ci].ID, 
        #                        random.choice(['R', 'S', 'P']))
        #     cmds.append(cmd)
        # city_indexes = list(range(len(my_cities)))
        # # Overview: issue a move to every unit giving a random
        # # direction. Directions can be found in the vec2.py file.
        # # They are single char strings: 'N', 'E', 'W', 'S'.
        # my_units = units[faction_id]
        # for u in my_units:
        #     rand_dir = random.choice(list(vec2.MOVES.keys()))
        #     cmd = MoveUnitCommand(faction_id, u.ID, rand_dir)
        #     cmds.append(cmd)

        print("The game is running:: ", faction_id)
        my_cities = cities[faction_id]
        my_units = units[faction_id]
        # first build units
        for i, c in enumerate(my_cities):
            occupid = False
            for j in my_units:
                if j.pos == c.pos:
                    occupid=True
                    break
            if not occupid:
                if i%3==0:
                    unitType = 'R'
                elif i%3==1:
                    unitType = 'P'
                else:
                    unitType = 'S'
                print(f"building {unitType} at {c.ID} ({c.pos.x}, {c.pos.y})")
                cmds.append(BuildUnitCommand(faction_id, c.ID, unitType))
            else:
                print("city occupied to: ", c.ID)

        # print("Got here 1")
        # do some identification for enemies
        enemy_cities = []
        enemy_unit = []

        for id, lst in cities.items():
            if id != faction_id:
                enemy_cities.extend(lst)
        
        for id, lst in units.items():
            if id!=faction_id:
                enemy_unit.extend(lst)
        print(enemy_cities, enemy_unit)


        ################# implement some defender troops
        # print("Got here 2")
        defIDs = set()
        maxDef = min(2, len(my_units))
        for c in my_cities:
            if(len(defIDs)>=maxDef):
                break

            clsUnit = None
            clsDistance = float('inf')
            for u in my_units:
                if u.ID in defIDs:
                    continue

                dist = abs(u.pos.x-c.pos.x)+abs(u.pos.y-c.pos.y)
                if dist < clsDistance:
                    clsDistance=dist
                    clsUnit=u
            
            if clsUnit:
                defIDs.add(clsUnit.ID)
                if clsDistance >1:
                    dx=c.pos.x - clsUnit.pos.x
                    dy=c.pos.y-clsUnit.pos.y

                    if abs(dx)>abs(dy):
                        if dx>0:
                            dir = 'E' 
                        else:
                            dir = 'W'
                    else:
                        if dy > 0:
                            dir='S'
                        else:
                            dir='N'

                    cmds.append(MoveUnitCommand(faction_id, clsUnit.ID, dir))

        # print("Got here 3")
        #### lets attcak
        
        for u in my_units:
            if u.ID in defIDs:
                continue
            if not enemy_unit:
                if not enemy_cities:
                    continue


                nearstCity = None
                min_dist = float('inf')
                for c in enemy_cities:
                    dc = abs(c.pos.x-u.pos.x)+abs(c.pos.y-u.pos.y) # distance to city
                    if dc<min_dist:
                        min_dist=dc
                        nearstCity=c

                dx = nearstCity.pos.x - u.pos.x
                dy = nearstCity.pos.y - u.pos.y

                if abs(dx)>abs(dy):
                    if dx>0:
                        dir='E'
                    else:
                        dir='W'
                else:
                    if dx>0:
                        dir='S'
                    else:
                        dir='N'
                cmds.append(MoveUnitCommand(faction_id, u.ID, dir))
                continue

            # find nearest enemy unit
            nearest_enemy = None
            min_dist = float('inf')

            for eu in enemy_unit:
                dist = abs(eu.pos.x - u.pos.x) + abs(eu.pos.y - u.pos.y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_enemy = eu

            if nearest_enemy:
                dx = nearest_enemy.pos.x - u.pos.x
                dy = nearest_enemy.pos.y - u.pos.y

                if abs(dx)>abs(dy):
                    if dx>0:
                        dir='E'
                    else:
                        dir='W'
                else:
                    if dx>0:
                        dir='S'
                    else:
                        dir='N'

                cmds.append(MoveUnitCommand(faction_id, u.ID, dir))

            
       
        # return all the command objects.
        return cmds
