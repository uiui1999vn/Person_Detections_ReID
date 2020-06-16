from random import randrange

import numpy as np
colours = np.random.randint(0, 256, size=(32, 3))
print(colours)
color = colours[randrange(256) % 32].tolist()
print(color)