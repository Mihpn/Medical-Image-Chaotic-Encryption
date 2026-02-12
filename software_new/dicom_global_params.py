import numpy as np

NumberUsers = 2 					# Number of users (Number of PCs)
K           = 8 					# Number of images
kP0         = np.array([[64 ], [154], [37], [73], [17], [56 ], [72], [68]], dtype=np.uint16) # Initial value
kC0         = np.array([[123], [11 ], [27], [88], [33], [211], [97], [63]], dtype=np.uint16) # Initial value
kP_MN       = np.array([[64 ], [154], [37], [73], [17], [56 ], [72], [68]], dtype=np.uint16) # Initial value
Ne          = 5     				# Ne = Number of encryption loops
Ne_max_bit  = 4                     # Maximum number of bits used to prsent Ne
NamePCM     = 'Cat' 				# Type of PCM to use
M_max       = 16    				# M max
N_max       = 16    				# N max
NB_max      = 16    				# Number of bits to present a pixel max
PK_base_len = 32    				# Base length of private key (default: 32 bits)
S_len       = PK_base_len * (K + 1) # Length of S
pk_len      = (K + 1) + PK_base_len # Length of each private key
phi_S_len   = pk_len * K            # Length of phi_S
