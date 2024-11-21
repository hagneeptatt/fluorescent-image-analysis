# Image Analysis Function for Batch Processing
# Created 15/11/24 by Fraser Shields

## Workflow:
# 1. Import modules & packages
# 2. Loading image data 
# 3. Smoothing
# 4. Adaptive Thresholding
# 5. Optimising mask
# 6. ROI selection
# 7. Quantification of fluorescence 

## Import Modules & Packages 
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import pandas as pd 


def img_analysis_pipeline(dirpath, filename):
    """_summary_

    Parameters
    ----------
    dirpath : _type_
        _description_
    filename : _type_
        _description_
    """

    ## Loading Image Data

    # join function to combine strings and take care of slashes 
    from os.path import join

    filepath = join(dirpath, filename)

    #  Import the function 'imread' from the module 'skimage.io'.
    from skimage.io import imread

    # Use imread function to load image as ndarray 
    img = imread(filepath)
    print(f"Image shape for {filename}: {img.shape}")
    


    ## Split image into seperate channels 
    img_c0 = img[0, :, :]
    img_c1 = img[1, :, :]


    ## Guassian Smoothing

    # smoothing factor
    sigma = 1

    # perform smoothing
    img_c0_smooth = ndi.gaussian_filter(img_c0, sigma)
    img_c1_smooth = ndi.gaussian_filter(img_c1, sigma)


    ## Li Thresholding 

    # Import threshold function
    from skimage.filters.thresholding import threshold_li

    # Apply Li Threshold
    img_c0_thresh = threshold_li(img_c0_smooth)
    img_c1_thresh = threshold_li(img_c1_smooth)


    # Binarise the image 
    img_c0_mask = img_c0_smooth > img_c0_thresh
    img_c1_mask = img_c1_smooth > img_c0_thresh

    # Apply the mask to the original image to isolate the region of interest
    masked_img_c0 = img_c0_smooth * img_c0_mask
    masked_img_c1 = img_c1_smooth * img_c1_mask

    # Measure fluorescence intensity for each channel
    intensity_c0 = masked_img_c0.sum()
    intensity_c1 = masked_img_c1.sum()

    # Calculate the mask area (number of non-zero pixels in the mask)
    area_c0 = img_c0_mask.sum()
    area_c1 = img_c1_mask.sum()

    # Normalize intensity by mask area
    intensity_per_area_c0 = intensity_c0 / area_c0
    intensity_per_area_c1 = intensity_c1 / area_c1

    # Store results in a DataFrame
    results_df = pd.DataFrame({
        "filename": [filename],
        "intensity_c0": [intensity_c0],
        "intensity_c1": [intensity_c1],
        "area_c0": [area_c0],
        "area_c1": [area_c1],
        "intensity_per_area_c0": [intensity_per_area_c0],
        "intensity_per_area_c1": [intensity_per_area_c1]
    })

    print(f"Processing {filename}: intensity_c0={intensity_c0}, intensity_c1={intensity_c1}")




    return results_df







