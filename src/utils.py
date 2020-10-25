import random


def sorted_random_sample(population_size: int, k: int):
    return sorted(random.sample(list(range(population_size)), k))