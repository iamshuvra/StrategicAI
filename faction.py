# Faction class

import unit


class Faction:
    def __init__(self, ID, money, ai, color):
        self.ID = ID
        self.money = money
        self.ai = ai
        self.next_unit_id = 0
        self.color = color

    def get_next_unit_id(self):
        uid = self.next_unit_id
        self.next_unit_id += 1
        return uid

    def can_build_unit(self, cost):
        return cost <= self.money
        
    # ################################################################
    def run_ai(self, factions, cities, units, gmap):
        return self.ai.run_ai(self.ID, factions, cities, units, gmap)
