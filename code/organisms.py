import numpy as np


class Organism:
    def __init__(self, species, position, size, alive=True, parents=None):
        self.species = species
        self.position = position
        self.size = size  # Could make this between 0-1, 1 for biggest organism
        self.alive = alive
        # Set organism quality
        if parents is None:
            self.quality = np.random.normal(0.5, 0.95 / 6, 1)[0]
        elif len(parents) == 2:
            parents_quality = (parents[0].quality + parents[1].quality) / 2
            self.quality = np.random.normal(parents_quality, 0.95 / 6, 1)[0]
        self.age = 0
        self.energy = 0.5
        self.stress = 0
        self.food_value = self.size
        self.rot_amount = 0

    def die(self):
        # Kills an animal, but keeps corpse around
        self.alive = False

    def rot(self, rot_rate, object_set):
        # Decrease food value of animal after death
        if not self.alive:
            self.rot_amount += rot_rate
            self.food_value = self.size * (1-self.rot_amount)
        if self.rot_amount >= 100:
            object_set.pop(self)


class Animal(Organism):
    """
    Blueprint for animals.
    """
    def __init__(self, species, diet, position, size, alive=True, parents=None, sex_ratio=0.5):
        super().__init__(species, diet, position, size, alive, parents)
        # Set animal sex
        if np.random.uniform(0, 1) >= sex_ratio:
            self.sex = 'f'
        else:
            self.sex = 'm'
        self.diet = diet  # 'h'erbivore, 'c'arnivore, or 'o'mnivore
        self.food_type = 'meat'
        self.mated_recently = False
        self.pregnant = False
        self.reach = self.size/5

    def mate(self, target):
        if self.alive and target.alive and self.species == target.species:
            if self.sex != target.sex:
                quality_diff = np.abs(self.quality - target.quality)
                mate_chance = np.random.normal(1-quality_diff, 0.95/6, 1)
                if np.random.uniform(0, 1, 1) <= mate_chance:
                    self.socialise(target, intercourse=True)
                    if self.sex == 'f':
                        self.pregnant = True
                    else:
                        target.pregnant = True
            else:
                self.socialise(target, intercourse=True)

    def eat(self, target, object_set):
        # Eats the target food if it is a diet match and
        if self.diet == 'o':
            self.energy += target.food_value
            self.energy = min(1, self.energy)
            object_set.pop(target)
        elif self.diet == 'c' and target.food_type == 'meat':
            self.energy += target.food_value
            self.energy = min(1, self.energy)
            object_set.pop(target)
        elif self.diet == 'h' and target.food_type == 'plant':
            self.energy += target.food_value
            self.energy = min(1, self.energy)
            object_set.pop(target)

    def socialise(self, target, intercourse=False):
        # After a stress-proportional threshold is met, the stress levels of two intraspecific animals is reduced
        threshold = self.stress + target.stress
        if self.species == target.species and np.random.uniform(0, 2, 1) >= threshold:
            if intercourse:
                stress_heal = 0.5
            else:
                stress_heal = 0.2
            self.stress = max(self.stress - stress_heal, 0)
            target.stress = max(target.stress - stress_heal, 0)

    def move(self, target_loc, map_size, terrain_modifier):
        # Moves animal to target location, costing a certain amount of food in the process
        # Note: rework this to have species and quality modifiers to speed/food cost
        distance = np.linalg.norm(target_loc-self.position)
        self.energy -= (distance/map_size)*terrain_modifier


class Cat(Animal):
    def __init__(self, position, size, alive=True, parents=None, sex_ratio=0.5):
        super().__init__('Cat', 'c', position, size,  alive, parents, sex_ratio)


class Rat(Animal):
    def __init__(self, position, size, alive=True, parents=None, sex_ratio=0.5):
        super().__init__('Rat', 'o', position, size,  alive, parents, sex_ratio)


class Horse(Animal):
    def __init__(self, position, size, alive=True, parents=None, sex_ratio=0.5):
        super().__init__('Horse', 'h', position, size,  alive, parents, sex_ratio)
