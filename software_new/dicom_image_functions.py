import cv2
import os
from matplotlib import pyplot as plt

# Function: Read images
# path: Directory
# size: Size of images, size = (N, M)
# OS: Name of OS
# Return: List of image matrices (list of numpy arrays)
def read_images(path, size = (256, 256), OS = 'Windows'):
    I_plains = os.listdir(path)
    N_files = len(I_plains)
    kI = []
    str_Fnames = []

    for i in range(0, N_files):
        str = I_plains[i]
        str_Fnames.append(str)
        Ip = cv2.imread(path + '\\' + str if OS == 'Windows' else path + '/' + str)
        Ip_resized = cv2.resize(Ip, size, interpolation = cv2.INTER_AREA)
        kI.append(Ip_resized)
    return kI, str_Fnames


# Function: Show images
# kI: List of image matrices
# suptitle: Super title
# str_Fnames: List of image names
# size: Size of a image window
# rows: Number of rows presented
# cols: Number of columns presented
def show_images(kI, suptitle, str_Fnames, size = (10, 10), rows = 3, cols = 3):
    fig = plt.figure(figsize = size)

    for i in range(len(kI)):
        fig.add_subplot(rows, cols, i + 1)
        plt.imshow(kI[i])
        plt.title(str_Fnames[i])
    fig.suptitle(suptitle, size = 16)
    fig.tight_layout(pad=1.0)
    plt.show()


# Function: Merge images
def merge_images(kI, ID):
    kI_merge = []
    temp = []
    last_id_image = ID[0][1]
    for i in range(1, len(kI) + 1):
        new_id_image = ID[i][1] if i < len(kI) else 0
        if ((new_id_image == last_id_image) and (i != len(kI))):
            temp.append(kI[i-1])
            temp.append(kI[i])
        elif (len(temp)):
            merged_image = cv2.cvtColor(cv2.merge(temp), cv2.COLOR_BGRA2BGR)
            kI_merge.append(merged_image)
            temp.clear()
        else:
            kI_merge.append(kI[i-1])
        last_id_image = new_id_image
    return kI_merge


# Function: Save image into directory
def save_images(kC, folder_path, str_Fnames):
    for i in range(len(str_Fnames)):
        cv2.imwrite(os.path.join(folder_path, str_Fnames[i]), kC[i])
