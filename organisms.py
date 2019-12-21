import numpy as np

class Animal:
    """
    Blueprint for animals.
    """
    def __init__(self, species, position, size, parents=None, sex_ratio=0.5 ):
        self.species = species
        self.position = position
        self.size = size
        if np.random.uniform(0, 1) >= sex_ratio:
            self.sex = 'f'
        else:
            self.sex = 'm'
        if parents is None:
            self.quality = np.random.normal(0.5, 0.95/6, 1)
        elif len(parents) == 2:
            parents_quality = (parents[0].quality + parents[1].quality)/2
            self.quality = np.random.normal(parents_quality, 0.95/6, 1)
        # Quality will have a minor impact on all functions (movement etc) and a major influence on mating sucess

        self.age = 0
        self.food = 0.5
        self.stress = 0
        self.mated_recently = False

    def mate(target):
        # them-me as center of normal dist?
        pass

    def eat(target):
        pass

    def die(self):
        # keep corpse around until it fully 'rots' and disappears

    def socialise(self, target):
        # lowers stress of both. A low sucess threshold must be passed


