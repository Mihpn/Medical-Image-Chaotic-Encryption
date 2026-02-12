import numpy as np

NumberUsers = 2 # Number of users (Number of PCs)
K           = 8 # Number of images
kP0         = np.array([[64 ], [154], [37], [73], [17], [56 ], [72], [68]], dtype=np.uint16) # Initial value
kC0         = np.array([[123], [11 ], [27], [88], [33], [211], [97], [63]], dtype=np.uint16) # Initial value
kP_MN       = np.array([[64 ], [154], [37], [73], [17], [56 ], [72], [68]], dtype=np.uint16) # Initial value
Ne          = 5
NamePCM     = 'Cat' # Type of PCM to use
M_max       = 16    # M max
N_max       = 16    # N max
NB_max      = 16    # Number of bits to present a pixel max
