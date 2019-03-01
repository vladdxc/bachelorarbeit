import numpy as np
import glob
from skimage import io
import matplotlib.pyplot as plt

path = "D:\patches_S1B_IW_GRDH_20180823\*.tif"
fls = glob.glob(path)
len_path = len(fls)

params = {'dim': (128, 128, 2),
          'batch_size': 32,
          'n_classes': 1,
          'shuffle': True}

if __name__ == '__main__':
    img = io.imread("D:\patches_S1B_IW_GRDH_20180823\patch_1_1_counter_1.tif")
    img = img.astype(np.float32)
    img_r = np.reshape(img, (np.size(img), ))
    img_res = np.reshape(img, [-1, np.size(img)])

    if img_r.shape == img_res.shape:
        print('Yes')
    else:
        print('No')
        print(img_r.shape, img_res.shape, img.shape)


