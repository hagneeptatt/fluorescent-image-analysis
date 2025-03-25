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

    print(f"Processing {filename}")


    # join function to combine strings and take care of slashes 
    from os.path import join

    filepath = join(dirpath, filename)

    #  Import the function 'imread' from the module 'skimage.io'.
    from skimage.io import imread

    # Use imread function to load image as ndarray 
    img = imread(filepath)
    


    ## Split image into seperate channels 
    # Subtract background found in image j 
    img_c0 = img[:, :, 0] 
    img_c1 = img[:, :, 1] 


    ## Guassian Smoothing

    # smoothing factor
    sigma = 1

    # perform smoothing
    img_c0_smooth = ndi.gaussian_filter(img_c0, sigma)
    img_c1_smooth = ndi.gaussian_filter(img_c1, sigma)


    ## Li Thresholding 

    # Import threshold function
    from skimage.filters.thresholding import threshold_li

    # Apply Threshold
    # Li
    # img_c0_thresh = threshold_li(img_c0_smooth)
    # img_c1_thresh = threshold_li(img_c1_smooth)
    # Manual
    img_c0_thresh = 130
    img_c1_thresh = 5000

    # Binarise the image 
    img_c0_mask = img_c0_smooth > img_c0_thresh
    img_c1_mask = img_c1_smooth > img_c0_thresh

    # Apply the mask to the original image to isolate the region of interest
    masked_img_c0 = img_c0_smooth * img_c0_mask
    masked_img_c1 = img_c1_smooth * img_c1_mask

    # Measure fluorescence intensity for each channel
    total_intensity_c0 = masked_img_c0.sum()
    total_intensity_c1 = masked_img_c1.sum()

    # Calculate the mask area (number of non-zero pixels in the mask)
    area_c0 = img_c0_mask.sum()
    area_c1 = img_c1_mask.sum()

    # Normalize intensity by mask area
    mfi_c0 = total_intensity_c0 / area_c0
    mfi_c1 = total_intensity_c1 / area_c1

    # Store results in a DataFrame
    results_df = pd.DataFrame({
        "filename": [filename],     
        "total_intensity_c0": [total_intensity_c0],
        "total_intensity_c1": [total_intensity_c1],
        "area_c0": [area_c0],
        "area_c1": [area_c1],
        "mfi_c0": [mfi_c0],
        "mfi_c1": [mfi_c1]
    })

    from matplotlib.pyplot import subplots, show
    # Display the masked images
    fig, axs = subplots(nrows=1, ncols=2, figsize=(20, 10))
    axs[0].imshow(masked_img_c0, interpolation='none', cmap='gray')
    axs[1].imshow(masked_img_c1, interpolation='none', cmap='gray')
    axs[0].set_title(f'{filename} C0 Masked Image')
    axs[1].set_title(f'{filename} C1 Masked Image')
    show()

    



    return results_df








