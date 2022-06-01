import os
import pandas as pd
from PIL import Image


def crop_cell(row):
    input_dir = 'BCCD\JPEGImages'
    output_dir = 'BCCD\cropped'
    # open image
    im = Image.open(f"{input_dir}\{row['filename']}")

    # size of the image in pixels
    width, height = im.size

    # setting the points for cropped image
    left = row['xmin']
    bottom = row['ymax']
    right = row['xmax']
    top = row['ymin']

    # cropped image
    im1 = im.crop((left, top, right, bottom))
    cropped_fname = f"BloodImage_{row['image_id']:03d}_{row['cell_id']:02d}.jpg"
    # shows the image in image viewer
    # im1.show()

    # save image
    try:
        im1.save(f"{output_dir}\{cropped_fname}")
    except:
        return 'error'

    return cropped_fname

if __name__ == "__main__":
    # load metadata
    task1_fp = r"task1.csv"
    task1_df = pd.read_csv(task1_fp)
    task2_fp = "BCCD\dataset2-master\labels.csv"
    task2_df = pd.read_csv(task2_fp)

    # drop first column
    task2_df = task2_df.iloc[:, 1:]

    # add cell_type
    task2_df['cell_type'] = 'WBC'

    # add WBC category to dataframe
    dataset_df = task1_df.merge(task2_df.rename({"Image": "image_id", "Category": "wbc_category"}, axis=1), on=['image_id', 'cell_type'], how='left')
    
    # crop each cell and save to file
    dataset_df['cell_filename'] = dataset_df.apply(crop_cell, axis=1)

    # drop errors
    dataset_df = dataset_df[dataset_df.cell_filename != 'error']

    # save to csv
    dataset_df[['cell_filename', 'image_id', 'cell_id', 'cell_type', 'wbc_category']].to_csv('both.csv', index=False)
