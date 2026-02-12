import math
import numpy as np
import dicom_global_params
import dicom_cat_params
from fxpmath import Fxp

# Function: XOR two binary strings
# a, b: Operators (string)
# Return: a XOR b (string)
def xor(a, b):
    if (len(a) != len(b)):
        print("BIT XOR ERROR")
        return None
    
    ans = ""
     
    # Loop to iterate over the
    # Binary Strings
    for i in range(len(a)):
         
        # If the Character matches
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans

# Function: DICOM MIE Bit Manipulation
# s1: Sequence 1
# s2: Sequence 2
# output_size: Size of output list
# Return: Bit string after Bit Manipulation
def bit_manipulation(s1, s2, output_size = 1):
    # E1 = ''
    # E2 = ''
    
    # E1 = E1 + np.binary_repr(s1[0][0], width = math.ceil(math.log2(s1[0][0])))
    # E2 = E2 + np.binary_repr(s2[0][0], width = math.ceil(math.log2(s2[0][0])))

    E1 = str(s1)
    E2 = str(s2)
    
    if ((len(E1)) and (len(E2))):
        T = ''
        for i in range(len(E2)):
            T = T + E2[i] + E1[i]
    elif (len(E1)):
        T = str(E1)
    else:
        T = str(E2)

    times = math.ceil(len(T) * 1.0 / output_size)
    E = ''
    if times <= 1.0: # |E1| + |E2| < |E|
        m = math.ceil(output_size * 1.0 / len(T)) # (m-1) * |T'| < |E| < m * |T'|
        T = T * int(m) # T = T' * m

        # Split E into n bit sequences
        n = math.ceil(len(T) * 1.0 / output_size) # (n-1) * |E| < |T| < n * |E|

        # Number of bit 0 needed to padd to Tn = |E| - |Tn|
        if ((len(T) % output_size) != 0):
            zero_length_pad = output_size * math.ceil(len(T) * 1.0 / output_size) - len(T) * 1.0
            str_zeros = '0' * int(zero_length_pad)
            T = T + str_zeros

        E = T[0:output_size]
        for i in range(1, n):
            E = xor(E, T[i*output_size:(i+1)*output_size])
        
    else: # |E1| + |E2| > |E|
        # Split E into n bit sequences
        n = math.ceil(len(T) * 1.0 / output_size) # (n-1) * |E| < |T| < n * |E|

        # Number of bit 0 needed to padd to Tn = |E| - |Tn|
        if ((len(T) % output_size) != 0):
            zero_length_pad = output_size * math.ceil(len(T) * 1.0 / output_size) - len(T) * 1.0
            str_zeros = '0' * int(zero_length_pad)
            T = T + str_zeros

        E = T[0:output_size]
        for i in range(1, n):
            E = xor(E, T[i*output_size:(i+1)*output_size])
        
    return E

# Function: Bit arrangement 1D to nD - from 1D matrix to nD matrix
# Y: Rule of bit arrangement (list of numpy arrays)
# B: Source bit-string array (string array-list of strings)
# Return: Destination bit-string array (string array or list of strings)
def bit_arrangement_1d_to_nd(Y: list, B) -> list:
    # Flip left/right verison of B
    B_fliplr = B.copy()
    
    matrix_B = []
    for i in range(len(B_fliplr)):
        # matrix_B[i] = [*B_fliplr[i]] # Unpack string to a list
        matrix_B.append([*B_fliplr[i]]) # Unpack string to a list

    # Y.shape
    width_Y = Y[0].shape[1]
    depth_Y = len(Y)

    A1 = []
    temp_A1 = []

    for k in range(depth_Y):
        for j in range(width_Y):
            if ((Y[k][0][j] == 0) & (Y[k][1][j] == 0)):
                temp_A1.append('0')
            elif ((Y[k][0][j] == 100) & (Y[k][1][j] == 100)):
                temp_A1.append('1')
            else:
                temp_A1.append(str(matrix_B[Y[k][0][j]-1][Y[k][1][j]-1]))
        A1.append(temp_A1)
        temp_A1 = []

    # Result: New string array (list of string)
    A = []
    for k in range(depth_Y):
        A.append(''.join(A1[k]))

    return A


# Function: Bit arrangement MIE nD
# Y: Rule of bit arrangement (list of numpy arrays)
# B: Source bit-string array (string array or list of strings)
# Return: Destination bit-string array (string array or list of strings)
def bit_arrangement_nd(Y: list, B) -> list:
    #Size of B
    height_B = len(B)
    # matrix_B = [] * height_B # [[''], [''],..., ['']]
    matrix_B = []
    for i in range(height_B):
        # matrix_B[i] = [*B[i]] # List of bits
        matrix_B.append([*B[i]]) # List of bits
    
    # Y.shape
    width_Y = Y[0].shape[1]
    depth_Y = len(Y)

    A1 = []
    temp_A1 = []

    for k in range(depth_Y):
        for j in range(width_Y):
            if ((Y[k][0][j] == 0) & (Y[k][1][j] == 0)):
                temp_A1.append('0')
            elif ((Y[k][0][j] == 100) & (Y[k][1][j] == 100)):
                temp_A1.append('1')
            else:
                temp_A1.append(str(matrix_B[Y[k][0][j]-1][Y[k][1][j]-1]))
        A1.append(temp_A1)
        temp_A1 = []

    # Result: New string array (list of string)
    A = []
    for k in range(depth_Y):
        A.append(''.join(A1[k]))

    return A


# Function: Linear Constraint Function for Encryption process
# ID: List of User IDs and Image IDs ([[user_id_0, image_id_0], [user_id_0, image_id_0], [user_id_1, image_id_1], ...])
# I0: Key I0 (bit string)
# RV: Recover values for all images (see type in file ipynb)
# XY: Current i and j (just [i, j])
# kP_plus: Plain images' pixels (list of plain pixels matrices). If image k has c channels, kP_plus[k] is always [p_1]
# kC_minus: Cipher images' pixels (list of cipher pixels matrices). If image k has 3 channels, kC_minus[k] = [c_1, c_2, c_3]
# list_im_size: List of image sizes [(M_0, N_0), (M_1, N_1),..., (M_K, N_K)]
# Return: 1. LCF: I0 XOR point_choosen_bin (bit string)
#         2. RV: Recover values for all images
def linear_constraint_function_enc(ID, I0, RV, XY, kP_plus, kC_minus, list_im_size):
    i = XY[0]
    j = XY[1]

    k = 0
    last_id_image = ID[0][1]

    # Point chooosen
    point_choosen = 0
    for idx in range(len(ID)):
        new_id_image = ID[idx][1]
        if (new_id_image != last_id_image):
            k += 1
        if ((i < list_im_size[k][0]) and (j < list_im_size[k][1])): # In hardware, don't need to check this statement
                                                                    # because all image will be placed in cells of the same size
            if (kP_plus[idx][0] != 0):
                point_choosen = (kP_plus[idx][0].astype(np.uint8) ^ kC_minus[idx][0].astype(np.uint8)).astype(np.uint8)
                break
        last_id_image = new_id_image
    point_choosen_bin = np.binary_repr(point_choosen, width = 8)

    # LCF
    LCF = xor(I0[-8:], 
              point_choosen_bin[-8:])

    
    # RV
    k = 0
    last_id_image = ID[0][1]
    for idx in range(len(ID)):
        new_id_image = ID[idx][1]
        if (new_id_image != last_id_image):
            k += 1
        elif (idx != 0):
            last_id_image = new_id_image
            continue
        if ((i < list_im_size[k][0]) and (j < list_im_size[k][1])):
            kP_k_bin = np.binary_repr(kP_plus[idx][0], width = dicom_global_params.NB_max)
            rv = xor(kP_k_bin[-8:], 
                     I0[-8:])
            rv = xor(rv, LCF)
            RV[k][i][j] = rv
        last_id_image = new_id_image

    return LCF, RV


# Function: Linear Constraint Function for Decryption process of the kth image
# I0: Key I0 (bit string)
# p_plus: Plain images' pixel (just value of plain pixel)
# Return: LCF: I0 XOR point_choosen_bin (bit string)
def linear_constraint_function_dec_k(I0, rv, p_plus):
    # p_plus_bin
    p_plus_bin = np.binary_repr(p_plus[0][0], width = dicom_global_params.NB_max)

    # LCF
    LCF = xor(I0[-8:], 
              rv      )
    LCF = xor(LCF            , 
              p_plus_bin[-8:] )

    return LCF


# Function: Linear Constraint Function for Decryption process of all images
# ID: List of User IDs and Image IDs ([[user_id_0, image_id_0], [user_id_0, image_id_0], [user_id_1, image_id_1], ...])
# I0: Key I0 (bit string)
# XY: Current i and j (just [i, j])
# RV: Recover values for all images (see type in file ipynb)
# kP_plus: Plain images' pixels (list of plain pixels matrices). If image k has c channels, kP_plus[k] is always [p_1]
# list_im_size: List of image sizes [(M_0, N_0), (M_1, N_1),..., (M_K, N_K)]
# Return: LCF: I0 XOR point_choosen_bin (bit string)
def linear_constraint_function_dec(ID, I0, XY, RV, kP_plus, list_im_size):
    i = XY[0]
    j = XY[1]

    k = 0
    last_id_image = ID[0][1]
    for idx in range(len(ID)):
        new_id_image = ID[idx][1]
        if (new_id_image != last_id_image):
            k += 1
        if ((i < list_im_size[k][0]) and (j < list_im_size[k][1])):
            kP_k_bin = np.binary_repr(kP_plus[idx][0], width = dicom_global_params.NB_max)
            LCF = xor(kP_k_bin[-8:], 
                      I0[-8:])
            LCF = xor(LCF, RV[k][i][j])
            break
        last_id_image = new_id_image

    return LCF


# Function: Cat chaotic map
# gamma: gamma (fixed-point numbers array)
# xy: X_R (fixed-point numbers array - numpy array with dtype = Fxp)
# N: Number of bits to present xy (float)
# Return: Numpy array with dtype = Fxp
def cat_fi(gamma, xy: np.ndarray, N):
    xy_out = np.copy(xy)
    xy_out[0][0] = Fxp(xy[0][0] + gamma[0][0]*xy[1][0] - math.floor(xy[0][0] + gamma[0][0]*xy[1][0]), False, N, N-1)
    xy_out[1][0] = Fxp(gamma[1][0]*xy[0][0] + (gamma[0][0]*gamma[1][0] + 1)*xy[1][0] - math.floor(gamma[1][0]*xy[0][0]+(gamma[0][0]*gamma[1][0] + 1)*xy[1][0]), False, N, N-1)
    return xy_out


# Function: PCM Cat map
# E: Result after Bit Manipulation (string)
# Y1_FAST_Cat: Rule of bit arrangement (list of numpy arrays)
# Y2_FAST_Cat: Rule of bit arrangement (list of numpy arrays)
# Y3_FAST_Cat: Rule of bit arrangement (list of numpy arrays)
# Y4_FAST_Cat: Rule of bit arrangement (list of numpy arrays)
# R: Number of iterations (integer)
# Return: X_R (Numpy array with dtype = Fxp)
def pcm_cat(E: str, Y1_FAST_Cat, Y2_FAST_Cat, Y3_FAST_Cat, Y4_FAST_Cat, R):
    delta_gamma = bit_arrangement_1d_to_nd(Y1_FAST_Cat, [E])
    gamma_tmp = np.copy(dicom_cat_params.Gamma0_Cat)
    for i in range(len(gamma_tmp)):
        gamma_tmp_bin = xor(gamma_tmp[i][0].bin(), delta_gamma[i])
        gamma_tmp[i][0] = Fxp('0b' + gamma_tmp_bin, False, dicom_cat_params.m2_cat, dicom_cat_params.m2_cat - 6)

    delta_X = bit_arrangement_1d_to_nd(Y3_FAST_Cat, [E])
    X_R_tmp = np.copy(dicom_cat_params.IV0_Cat)
    for i in range(len(X_R_tmp)):
        X_R_tmp_bin = xor(X_R_tmp[i][0].bin(), delta_X[i])
        X_R_tmp[i][0] = Fxp('0b' + X_R_tmp_bin, False, dicom_cat_params.m1_cat, dicom_cat_params.m1_cat - 1)

    for r in range(R):
        X_R = cat_fi(gamma_tmp, X_R_tmp, dicom_cat_params.m1_cat)

        delta_gamma = bit_arrangement_nd(Y2_FAST_Cat, [X_R[0][0].bin(), X_R[1][0].bin()])
        for i in range(len(gamma_tmp)):
            gamma_tmp_bin = xor(gamma_tmp[i][0].bin(), delta_gamma[i])
            gamma_tmp[i][0] = Fxp('0b' + gamma_tmp_bin, False, dicom_cat_params.m2_cat, dicom_cat_params.m2_cat - 6)

        delta_X = bit_arrangement_nd(Y4_FAST_Cat, [X_R[0][0].bin(), X_R[1][0].bin()])
        for i in range(len(X_R)):
            X_R_bin = xor(X_R[i][0].bin(), delta_X[i])
            X_R[i][0] = Fxp('0b' +X_R_bin, False, dicom_cat_params.m1_cat, dicom_cat_params.m1_cat - 1)
    
    return X_R


# Function: Find new XY and phi_source, phi_dest to pass to Permutation and Diffusion (XYk for k = 1...K)
# X_R: X_R (numpy array with dtype = Fxp)
# Yp_MN: To find the next i and j (to find XY_new) (list of numpy arrays)
# Yd_C: To find phi_source (list of strings)
# Yd_Cx: To find phi_dest (list of strings)
# Return: 1. XY_new: New position [(i', j'), (i'', j''),...]
#         2. phi_source: After permutation, source plain pixel is XORed with phi_source
#         3. phi_dest: After permutation, destination plain pixel is XORed with phi_dest
def xy_phi_generation(X_R, Yp_MN, Y_phi_source, Y_phi_dest):
    # Generate new phi_source and phi_dest
    phi_source = bit_arrangement_nd(Y_phi_source, [X_R[0][0].bin(), X_R[1][0].bin()])
    phi_dest   = bit_arrangement_nd(Y_phi_dest, [X_R[0][0].bin(), X_R[1][0].bin()])

    # X_R.shape
    height_X_R = X_R.shape[0]
    # matrix_X_R = [['']] * height_X_R # [[''], [''],..., ['']]
    matrix_X_R = []
    for i in range(height_X_R):
        matrix_X_R.append([*X_R[i][0].bin()]) # List of bits

    # Yp_MN.shape
    width_Yp_MN = Yp_MN[0].shape[1]

    # XY_choose = [[''] * width_Yp_MN] * global_params.K # size = (global_params.K, width_Yp_MN): # [['', '',..., ''], ['', '',..., ''],..., ['', '',..., '']]
    XY_choose = []
    temp_XY_choose = []

    for k in range(dicom_global_params.K):
        for j in range(width_Yp_MN):
            temp_XY_choose.append(str(matrix_X_R[Yp_MN[k][0][j]-1][Yp_MN[k][1][j]-1]))
        XY_choose.append(temp_XY_choose)
        temp_XY_choose = []

    # XYnew
    XY_new  = []
    X_new   = Fxp(0, False, math.ceil(math.log2(dicom_global_params.M_max)), 0)
    Y_new   = Fxp(0, False, math.ceil(math.log2(dicom_global_params.N_max)), 0)

    for k in range(dicom_global_params.K):
        # X_new
        X_new.set_val('0b' + ''.join(XY_choose[k][0:int(math.log2(dicom_global_params.M_max))]))
        # X_new.set_val(X_new.get_val() % global_params.M_max)

        # Y_new
        Y_new.set_val('0b' + ''.join(XY_choose[k][int(math.log2(dicom_global_params.M_max)):]))
        # Y_new.set_val(Y_new.get_val() % global_params.N_max)

        XY_new.append([np.uint16(X_new), np.uint16(Y_new)])

    return XY_new, phi_source, phi_dest


# Function: Find new XY and phi_source, phi_dest to pass to Permutation and Diffusion for the kth image (XYk for k = 1...K)
# k: Order of the image
# X_R: X_R (numpy array with dtype = Fxp)
# Yp_MN: To find the next i and j (to find XY_new) (list of numpy arrays)
# Yd_C: To find phi_source (list of strings)
# Yd_Cx: To find phi_dest (list of strings)
# Return: 1. XY_new_k: New position (i', j')
#         2. phi_source_k: After permutation, source plain pixel is XORed with phi_source
#         3. phi_dest_k: After permutation, destination plain pixel is XORed with phi_dest
def xy_phi_generation_k(k, X_R, Yp_MN, Y_phi_source, Y_phi_dest):
    # Generate new phi_source and phi_dest
    phi_source_k = bit_arrangement_nd(Y_phi_source, [X_R[0][0].bin(), X_R[1][0].bin()])[k]
    phi_dest_k   = bit_arrangement_nd(Y_phi_dest, [X_R[0][0].bin(), X_R[1][0].bin()])[k]

    # X_R.shape
    height_X_R = X_R.shape[0]
    # matrix_X_R = [['']] * height_X_R # [[''], [''],..., ['']]
    matrix_X_R = []
    for i in range(height_X_R):
        matrix_X_R.append([*X_R[i][0].bin()]) # List of bits

    # Yp_MN.shape
    width_Yp_MN = Yp_MN[0].shape[1]

    # XY_choose = [[''] * width_Yp_MN] * global_params.K # size = (global_params.K, width_Yp_MN): # [['', '',..., ''], ['', '',..., ''],..., ['', '',..., '']]
    XY_choose = []
    temp_XY_choose = []

    for j in range(width_Yp_MN):
        temp_XY_choose.append(str(matrix_X_R[Yp_MN[k][0][j]-1][Yp_MN[k][1][j]-1]))
    XY_choose.append(temp_XY_choose)
    print("XY_choose: ", XY_choose)

    # XY_new_k
    XY_new_k  = []
    X_new_k   = Fxp(0, False, math.ceil(math.log2(dicom_global_params.M_max)), 0)
    Y_new_k   = Fxp(0, False, math.ceil(math.log2(dicom_global_params.N_max)), 0)

    # X_new_k
    X_new_k.set_val('0b' + ''.join(XY_choose[0][0:int(math.log2(dicom_global_params.M_max))]))

    # Y_new_k
    Y_new_k.set_val('0b' + ''.join(XY_choose[0][int(math.log2(dicom_global_params.M_max)):]))

    XY_new_k.append(np.uint16(X_new_k))
    XY_new_k.append(np.uint16(Y_new_k))

    return XY_new_k, phi_source_k, phi_dest_k


# Function: Bit Pre-processing of the kth image
# XY_k: Current position i, j of kth image (type: [i, j])
# XY_new_k: New position (i, j) of kth image (type: [i, j])
# phi_source_k: After permutation, source plain pixel of kth image is XORed with phi_source_k
# phi_dest_k: After permutation, destination plain pixel of kth image is XORed with phi_dest_k
# Mk: Height of kth image
# Nk: Width of kth image
# num_bits_pre_k: Number of bits to present a pixel of a channel of the kth image
# Return: 1. XY_Pk: New [i, j] of the kth image
#         2. phi_source_Pk: phi_source_k after moding
#         3. phi_dest_Pk: phi_dest_k after moding
def bit_pre_processing_k(XY_k, XY_new_k, phi_source_k, phi_dest_k, M_k, N_k, num_bits_pre_k):
    # Bit presentation of e_k1 and e_k2
    # e_k1_bin = np.binary_repr(e_k1, width = dicom_global_params.NB_max)
    # e_k2_bin = np.binary_repr(e_k2, width = dicom_global_params.NB_max)

    # ek
    # ek = bit_manipulation(s1          = e_k1_bin,
    #                       s2          = e_k2_bin,
    #                       output_size = math.ceil(math.log2(dicom_global_params.M_max)) + 
    #                                     math.ceil(math.log2(dicom_global_params.N_max))  )
    
    # Split XY_new_k
    Y_new_k = XY_new_k[1]
    Y_new_k_bin = np.binary_repr(Y_new_k, width = math.ceil(math.log2(dicom_global_params.N_max)))

    X_new_k = XY_new_k[0]
    X_new_k_bin = np.binary_repr(X_new_k, width = math.ceil(math.log2(dicom_global_params.M_max)))

    # Find Y_Pk and X_Pk
    # Y_Pk_bin = xor(Y_new_k_bin, ek[int(math.log2(dicom_global_params.M_max)):])
    Y_Pk = Fxp(0, False, math.ceil(math.log2(dicom_global_params.N_max)), 0)
    # Y_Pk.set_val('0b' + Y_Pk_bin)
    Y_Pk.set_val('0b' + Y_new_k_bin)
    Y_Pk.set_val(Y_Pk.get_val() % N_k)

    # X_Pk_bin = xor(X_new_k_bin, ek[0:int(math.log2(dicom_global_params.M_max))])
    X_Pk = Fxp(0, False, math.ceil(math.log2(dicom_global_params.M_max)), 0)
    # X_Pk.set_val('0b' + X_Pk_bin)
    X_Pk.set_val('0b' + X_new_k_bin)
    X_Pk.set_val(X_Pk.get_val() % M_k)

    # Check conditions
    XY_new_in_front_of_XY_1_pixel  = (((X_Pk == XY_k[0]) & (Y_Pk == XY_k[1] - 1))  | 
                                      ((X_Pk == XY_k[0] - 1) & (Y_Pk == N_k - 1) & (XY_k[1] == 0)) | 
                                      ((X_Pk == M_k - 1) & (Y_Pk == N_k - 1) & (XY_k[0] == 0) & (XY_k[1] == 0)))
    XY_new_after_XY_1_pixel        = (((X_Pk == XY_k[0]) & (Y_Pk == XY_k[1] + 1))  | 
                                      ((X_Pk == XY_k[0] + 1) & (Y_Pk == 0) & (XY_k[1] == N_k - 1)) | 
                                      ((X_Pk == 0) & (Y_Pk == 0) & (XY_k[0] == M_k - 1) & (XY_k[1] == N_k - 1)))
    XY_new_is_XY                   = ((X_Pk  == XY_k[0]) & (Y_Pk == XY_k[1]     ))
    XY_new_in_front_of_XY_2_pixels = (((X_Pk == XY_k[0]) & (Y_Pk == XY_k[1] - 2 )) | 
                                      ((X_Pk == XY_k[0] - 1) & (Y_Pk == N_k - 1) & (XY_k[1] == 1)) | 
                                      ((X_Pk == XY_k[0] - 1) & (Y_Pk == N_k - 2) & (XY_k[1] == 0)) | 
                                      ((X_Pk == M_k - 1) & (Y_Pk == N_k - 2) & (XY_k[0] == 0) & (XY_k[1] == 0)) | 
                                      ((X_Pk == M_k - 1) & (Y_Pk == N_k - 1) & (XY_k[0] == 0) & (XY_k[1] == 1)))
    XY_new_after_XY_2_pixels       = (((X_Pk == XY_k[0]) & (Y_Pk == XY_k[1] + 2 )) | 
                                      ((X_Pk == XY_k[0] + 1) & (Y_Pk == 0) & (XY_k[1] == N_k - 2)) | 
                                      ((X_Pk == XY_k[0] + 1) & (Y_Pk == 1) & (XY_k[1] == N_k - 1)) | 
                                      ((X_Pk == 0) & (Y_Pk == 0) & (XY_k[0] == M_k - 1) & (XY_k[1] == N_k - 2)) | 
                                      ((X_Pk == 0) & (Y_Pk == 1) & (XY_k[0] == M_k - 1) & (XY_k[1] == N_k - 1)))
    
    if ((XY_new_in_front_of_XY_1_pixel | XY_new_after_XY_1_pixel | XY_new_is_XY | XY_new_in_front_of_XY_2_pixels | XY_new_after_XY_2_pixels)):
        if (X_Pk < M_k - 1):
            X_Pk = X_Pk + 1
        else:
            X_Pk = X_Pk - 1
    
    # XY_Pk
    XY_Pk = [np.uint16(X_Pk), np.uint16(Y_Pk)]

    # phi_source_Pk
    phi_source_Pk = phi_source_k[-num_bits_pre_k:]
    phi_source_Pk = phi_source_k.zfill(dicom_global_params.NB_max)

    # phi_dest_Pk
    phi_dest_Pk = phi_dest_k[-num_bits_pre_k:]
    phi_dest_Pk = phi_dest_Pk.zfill(dicom_global_params.NB_max)

    return XY_Pk, phi_source_Pk, phi_dest_Pk


# Function: Bit Pre-processing of all image
# ID: List of User IDs and Image IDs ([[user_id_1, image_id_0], [user_id_1, image_id_1], [user_id_1, image_id_2], ...])
# XY: Current i and j ([(i', j'), (i'', j''),...])
# XY_new: New position [(i_new', j_new'), (i_new'', j_new''),...]
# phi_source: After permutation, source plain pixels are XORed with phi_source
# phi_dest: After permutation, destination plain pixels are XORed with phi_dest
# e_1: e1 (Type: The same as kP0)
# e_2: e2 (Type: The same as kC0)
# list_im_size: List of image sizes [(M_0, N_0), (M_1, N_1),..., (M_K, N_K)]
# list_num_bits_pre: List of number of bits to present a pixel of a channel
# Return: 1. XY_P: New (i, j) after moding ([[i_new_0, j_new_0], [i_new_1, j_new_1], ...])
#         2. phi_source_P: phi_source after moding
#         3. phi_dest_P: phi_dest after moding
def bit_pre_processing(XY, XY_new, phi_source, phi_dest, list_im_size, list_num_bits_pre):
    XY_P = []
    phi_source_P = []
    phi_dest_P = []
    for k in range(dicom_global_params.K):
        XY_Pk, phi_source_Pk, phi_dest_Pk = bit_pre_processing_k(XY_k           = [XY[0]       , XY[1]       ], 
                                                                 XY_new_k       = [XY_new[k][0], XY_new[k][1]], 
                                                                 phi_source_k   = phi_source[k]               , 
                                                                 phi_dest_k     = phi_dest[k]                 , 
                                                                 M_k            = list_im_size[k][0]          , 
                                                                 N_k            = list_im_size[k][1]          , 
                                                                 num_bits_pre_k = list_num_bits_pre[k]         )
        XY_P.append(XY_Pk)
        phi_source_P.append(phi_source_Pk)
        phi_dest_P.append(phi_dest_Pk)

    return XY_P, phi_source_P, phi_dest_P


# Function: DICOM MIE Permutation and Diffusion of Encryption processing
# ID: List of User IDs and Image IDs ([[user_id_1, image_id_0], [user_id_1, image_id_1], [user_id_1, image_id_2], ...])
# kI: Images (list of image matrices)
# XY: Current i and j ([(i', j'), (i'', j''),...])
# XY_P: New position [(i_new', j_new'), (i_new'', j_new''),...]
# phi_source_P: After permutation, source plain pixel is XORed with phi_source_P
# phi_dest_P: After permutation, destination plain pixel is XORed with phi_dest_P
# prev_kP_plus: Previous kP+
# kC_minus: kC- (the same type as kC0 = np.asarray([[123], [11 ], [27], [88], [33], [211], [97], [63]]))
# list_im_size: List of image sizes [(M_0, N_0), (M_1, N_1),..., (M_K, N_K)]
# n: Current iteration's order
# Return: 1. kC_to_pcm: Pixel's value used to impact chaotic map (the same type as kC_minus)
#         2. kP_plus: kP+
#         3. kI: Images after Permutation and Diffusion (list of image matrices)
def dicom_mie_perm_diff_enc(ID, kI, XY, XY_P, phi_source_P, phi_dest_P, prev_kP_plus, kC_minus, list_im_size, n):
    i = XY[0]
    j = XY[1]

    # For the next pixel: Pass the diffused pixel's value to chaotic map
    kC_to_pcm = np.zeros_like(kC_minus, dtype=np.uint16)

    # Find kP_plus for the next pixel
    kP_plus = np.zeros((len(ID), 1), dtype=np.uint16)

    k = 0
    last_id_image = ID[0][1]
    for idx in range(len(ID)):
        new_id_image = ID[idx][1]
        if (new_id_image != last_id_image):
            k += 1
        if ((i < list_im_size[k][0]) and (j < list_im_size[k][1])):
            # Permutation
            temp = kI[idx][i][j]
            kI[idx][i][j] = kI[idx][XY_P[k][0]][XY_P[k][1]]
            kI[idx][XY_P[k][0]][XY_P[k][1]] = temp
            
            # Diffusion
            temp = kI[idx][i][j] # Current pixel after Permutation
            temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), np.binary_repr(kC_minus[idx][0], width = dicom_global_params.NB_max)) # temp_value = I[i][j] XOR C[i-1][j]
            temp_str = xor(temp_str, phi_source_P[k]) # temp_value XOR phi_source_P (result of chaotic map)
            kI[idx][i][j] = np.uint16(int(temp_str, 2))
            
            # The pixel permuted with current pixel is also diffused
            temp = kI[idx][XY_P[k][0]][XY_P[k][1]]
            temp = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), phi_dest_P[k])
            kI[idx][XY_P[k][0]][XY_P[k][1]] = np.uint16(int(temp, 2))


            # For the next pixel: Pass the diffused pixel's value (kC_minus) to chaotic map
            kC_to_pcm[idx][0] = kI[idx][i][j]


            # Find kP_plus for the next pixel
            if (i < list_im_size[k][0] - 1): # This means i + 1 is not out of range (i + 1 <= M_k - 1)
                if (j < list_im_size[k][1] - 2): # This means k[i][j+2] is inside image because j + 2 is not out of range (j + 2 <= N_k - 1)
                    kP_plus[idx][0] = np.uint16(kI[idx][i][j+2])
                else: # This means j + 2 is out of range (j + 2 > N_k - 1) - gradually to the end of the line
                    kP_plus[idx][0] = np.uint16(kI[idx][i+1][j-(list_im_size[k][1]-1)+1]) # Go to the (j-(N_k-1)+1)th pixel of the next rows
            else: # This means i + 1 is out of range (i + 1 > M_k - 1)
                if (j < list_im_size[k][1] - 2): # This means j + 2 is not out of range (j + 2 <= N_k - 1)
                    kP_plus[idx][0] = np.uint16(kI[idx][i][j+2])
                elif(j == list_im_size[k][1] - 2): # This mean j + 2 == N_k
                    if (n == dicom_global_params.Ne - 1): # The last iteration
                        kP_plus[idx][0] = np.uint16(dicom_global_params.kP0[k][0])
                    else: # Not the last iteration
                        kP_plus[idx][0] = np.uint16(kI[idx][0][0])
                else: # This means j == N_k - 1
                    if (n < dicom_global_params.Ne - 1): # Not the last iteration
                        kP_plus[idx][0] = np.uint16(kI[idx][0][1])
        else:
            kP_plus[idx][0] = prev_kP_plus[idx][0]
            kC_to_pcm[idx][0] = kC_minus[idx][0]
        last_id_image = new_id_image

    return kC_to_pcm, kP_plus, kI


# Function: MIE Permutation and Diffusion of Decryption processing
# ID: List of User IDs and Image IDs ([[user_id_1, image_id_0], [user_id_1, image_id_1], [user_id_1, image_id_2], ...])
# kC: Cipher images (list of image matrices)
# XY: Current i and j (list [i, j])
# XY_P: New position [(i', j'), (i'', j''),...]
# phi_source_P: After permutation, source plain pixel is XORed with phi_source_P
# phi_dest_P: After permutation, destination plain pixel is XORed with phi_dest_P
# prev_kP_plus: Previous kP+
# kC_minus: kC- (the same type as kC0 = np.asarray([[123], [11 ], [27], [88], [33], [211], [97], [63]]))
# list_im_size: List of image sizes [(M_0, N_0), (M_1, N_1),..., (M_K, N_K)]
# n: Current iteration's order
# Return: 1. kC_minus_next: kC- for the next pixel
#         2. kP_to_pcm: Pixel's value used to impact chaotic map (the same type as kC_minus)
#         3. kC: kC
def dicom_mie_perm_diff_dec(ID, kC, XY, XY_P, phi_source_P, phi_dest_P, prev_kP_plus, kC_minus, list_im_size, n):
    i = XY[0]
    j = XY[1]

    # For the next pixel: Pass the diffused pixel's value to chaotic map
    kP_to_pcm = np.zeros_like(kC_minus, dtype=np.uint16)

    # Find kC_minus for the next pixel
    kC_minus_next = np.zeros((len(ID), 1), dtype=np.uint16)

    k = dicom_global_params.K - 1
    last_id_image = ID[len(ID) - 1][1]
    for idx in range(len(ID) - 1, -1, -1):
        new_id_image = ID[idx][1]
        if (new_id_image != last_id_image):
            k -= 1
        if ((i < list_im_size[k][0]) and (j < list_im_size[k][1])):
            # First, decrypt for the lastest pixel
            # Diffusion
            temp = kC[idx][XY_P[k][0]][XY_P[k][1]]
            temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), phi_dest_P[k])
            kC[idx][XY_P[k][0]][XY_P[k][1]] = np.uint16(int(temp_str, 2))
            
            # Diffusion
            temp = kC[idx][i][j] # Current pixel after Permutations
            temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), np.binary_repr(kC_minus[idx][0], width = dicom_global_params.NB_max)) # temp_value = I[i][j] XOR C[i-1][j]
            temp_str = xor(temp_str, phi_source_P[k]) # temp_value XOR phi_source_P (result of chaotic map)
            kC[idx][i][j] = np.uint16(int(temp_str, 2))
            
            # Permutation
            temp = kC[idx][i][j]
            kC[idx][i][j] = kC[idx][XY_P[k][0]][XY_P[k][1]]
            kC[idx][XY_P[k][0]][XY_P[k][1]] = temp


            # For the next pixel: Pass the diffused pixel's value to chaotic map
            kP_to_pcm[idx][0] = kC[idx][i][j]


            # Find kC_minus for the next pixel
            if (i > 0): # This means i - 1 is not out of range (i - 1 >= 0)
                if (j > 1): # This means k[i][j-2] is inside image because j - 2 is not out of range (j - 2 > 0)
                    kC_minus_next[idx][0] = np.uint16(kC[idx][i][j-2])
                else: # This means j - 2 is out of range (j - 2 < 0)
                    kC_minus_next[idx][0] = np.uint16(kC[idx][i-1][list_im_size[k][1]-(2-j)]) # Go to the (N_k-(2-j))th pixel of the previous rows
            else: # This means i - 1 is out of range (i - 1 < 0)
                if (j > 1): # This means j - 2 is not out of range (j - 2 >= 0)
                    kC_minus_next[idx][0] = np.uint16(kC[idx][i][j-2])
                elif(j == 1): # This mean j - 2 == -1 and the next pixels is the first pixels of all the images
                    if (n > 0):
                        kC_minus_next[idx][0] = np.uint16(kC[idx][list_im_size[k][0]-1][list_im_size[k][1]-1])
                    else: # The last iteration
                        kC_minus_next[idx][0] = np.uint16(dicom_global_params.kC0[k][0])
                else: # This means j == 0
                    if (n > 0):
                        kC_minus_next[idx][0] = np.uint16(kC[idx][list_im_size[k][0]-1][list_im_size[k][1]-2])
        else:
            kP_to_pcm[idx][0] = prev_kP_plus[idx][0]
            kC_minus_next[idx][0] = kC_minus[idx][0]
        last_id_image = new_id_image

    return kC_minus_next, kP_to_pcm, kC


# Function: MIE Permutation and Diffusion of Decryption processing for the kth image
# k: Order of the image
# kC: Cipher image (just one image)
# XY: Current i and j (list [i, j])
# XY_P: New position [i', j']
# phi_source_Pk: After permutation, source plain pixel is XORed with phi_source_Pk
# phi_dest_Pk: After permutation, destination plain pixel is XORed with phi_dest_Pk
# c_minus: c- (just [[c[i][j-1]]])
# M_k: M_k
# N_k: N_k
# num_bits_pre: Number of bits to present a pixel
# n: Current iteration's order
# Return: 1. c_minus_next: c- for the next pixel
#         2. kP_to_pcm: Pixel's value used to impact chaotic map (the same type as kC_minus)
#         3. kC: kC
def dicom_mie_perm_diff_dec_k(k, kC, XY, XY_Pk, phi_source_Pk, phi_dest_Pk, c_minus, M_k, N_k, n):
    i = XY[0]
    j = XY[1]

    # For the next pixel: Pass the diffused pixel's value to chaotic map
    p_to_pcm = np.zeros_like(c_minus, dtype=np.uint16)

    # Find kC_minus for the next pixel
    c_minus_next = np.zeros((1, 1), dtype=np.uint16)

    # First, decrypt for the lastest pixel
    # Diffusion
    temp = kC[XY_Pk[0]][XY_Pk[1]]
    temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), phi_dest_Pk)
    kC[XY_Pk[0]][XY_Pk[1]] = np.uint16(int(temp_str, 2))
    
    # Diffusion
    temp = kC[i][j] # Current pixel after Permutations
    temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), np.binary_repr(c_minus[0][0], width = dicom_global_params.NB_max)) # temp_value = I[i][j] XOR C[i-1][j]
    temp_str = xor(temp_str, phi_source_Pk) # temp_value XOR phi_source_P (result of chaotic map)
    kC[i][j] = np.uint16(int(temp_str, 2))
    
    # Permutation
    temp = kC[i][j]
    kC[i][j] = kC[XY_Pk[0]][XY_Pk[1]]
    kC[XY_Pk[0]][XY_Pk[1]] = temp


    # For the next pixel: Pass the diffused pixel's value to chaotic map
    p_to_pcm[0] = kC[i][j]


    # Find kC_minus for the next pixel
    if (i > 0): # This means i - 1 is not out of range (i - 1 >= 0)
        if (j > 1): # This means k[i][j-2] is inside image because j - 2 is not out of range (j - 2 > 0)
            c_minus_next[0][0] = np.uint16(kC[i][j-2])
        else: # This means j - 2 is out of range (j - 2 < 0)
            c_minus_next[0][0] = np.uint16(kC[i-1][N_k-(2-j)]) # Go to the (N_k-(2-j))th pixel of the previous rows
    else: # This means i - 1 is out of range (i - 1 < 0)
        if (j > 1): # This means j - 2 is not out of range (j - 2 >= 0)
            c_minus_next[0][0] = np.uint16(kC[i][j-2])
        elif(j == 1): # This mean j - 2 == -1 and the next pixels is the first pixels of all the images
            if (n > 0):
                c_minus_next[0][0] = np.uint16(kC[M_k-1][N_k-1])
            else: # The last iteration
                c_minus_next[0][0] = np.uint16(dicom_global_params.kC0[k][0])
        else: # This means j == 0
            if (n > 0):
                c_minus_next[0][0] = np.uint16(kC[M_k-1][N_k-2])

    return c_minus_next, p_to_pcm, kC


# Function: MIE Permutation and Diffusion of Decryption processing for the kth multi-channel image
# k: Order of the image
# kC: Cipher image (just one image)
# XY: Current i and j (list [i, j])
# XY_P: New position [i', j']
# phi_source_Pk: After permutation, source plain pixel is XORed with phi_source_Pk
# phi_dest_Pk: After permutation, destination plain pixel is XORed with phi_dest_Pk
# c_minus: c- (just [[c[i][j-1]]])
# M_k: M_k
# N_k: N_k
# num_bits_pre: Number of bits to present a pixel
# n: Current iteration's order
# Return: 1. c_minus_next: c- for the next pixel
#         2. kP_to_pcm: Pixel's value used to impact chaotic map (the same type as kC_minus)
#         3. kC: kC
def dicom_mie_perm_diff_dec_mc_k(k, kC, XY, XY_Pk, phi_source_Pk, phi_dest_Pk, kC_minus, M_k, N_k, n):
    i = XY[0]
    j = XY[1]

    # For the next pixel: Pass the diffused pixel's value to chaotic map
    kP_to_pcm = np.zeros_like(kC_minus, dtype=np.uint16)

    # Find kC_minus for the next pixel
    kC_minus_next = np.zeros((len(kC_minus), 1), dtype=np.uint16)


    for idx in range(len(kC_minus)):
        # First, decrypt for the lastest pixel
        # Diffusion
        temp = kC[idx][XY_Pk[0]][XY_Pk[1]]
        temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), phi_dest_Pk)
        kC[idx][XY_Pk[0]][XY_Pk[1]] = np.uint16(int(temp_str, 2))
        
        # Diffusion
        temp = kC[idx][i][j] # Current pixel after Permutations
        temp_str = xor(np.binary_repr(temp, width = dicom_global_params.NB_max), np.binary_repr(kC_minus[idx][0], width = dicom_global_params.NB_max)) # temp_value = I[i][j] XOR C[i-1][j]
        temp_str = xor(temp_str, phi_source_Pk) # temp_value XOR phi_source_P (result of chaotic map)
        kC[idx][i][j] = np.uint16(int(temp_str, 2))
        
        # Permutation
        temp = kC[idx][i][j]
        kC[idx][i][j] = kC[idx][XY_Pk[0]][XY_Pk[1]]
        kC[idx][XY_Pk[0]][XY_Pk[1]] = temp


        # For the next pixel: Pass the diffused pixel's value to chaotic map
        kP_to_pcm[idx][0] = kC[idx][i][j]


        # Find kC_minus for the next pixel
        if (i > 0): # This means i - 1 is not out of range (i - 1 >= 0)
            if (j > 1): # This means k[i][j-2] is inside image because j - 2 is not out of range (j - 2 > 0)
                kC_minus_next[idx][0] = np.uint16(kC[idx][i][j-2])
            else: # This means j - 2 is out of range (j - 2 < 0)
                kC_minus_next[idx][0] = np.uint16(kC[idx][i-1][N_k-(2-j)]) # Go to the (N_k-(2-j))th pixel of the previous rows
        else: # This means i - 1 is out of range (i - 1 < 0)
            if (j > 1): # This means j - 2 is not out of range (j - 2 >= 0)
                kC_minus_next[idx][0] = np.uint16(kC[idx][i][j-2])
            elif(j == 1): # This mean j - 2 == -1 and the next pixels is the first pixels of all the images
                if (n > 0):
                    kC_minus_next[idx][0] = np.uint16(kC[idx][M_k-1][N_k-1])
                else: # The last iteration
                    kC_minus_next[idx][0] = np.uint16(dicom_global_params.kC0[k][0])
            else: # This means j == 0
                if (n > 0):
                    kC_minus_next[idx][0] = np.uint16(kC[idx][M_k-1][N_k-2])

    return kC_minus_next, kP_to_pcm, kC
