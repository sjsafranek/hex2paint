import os
import glob
import math
import pandas
import argparse

import numpy
import skimage.color

# https://en.wikipedia.org/wiki/Color_difference
# https://stackoverflow.com/questions/1847092/given-an-rgb-value-what-would-be-the-best-way-to-find-the-closest-match-in-the-d
# https://www.baeldung.com/cs/compute-similarity-of-colours


files = glob.glob(os.path.join('data', '*.csv'))
_df = pandas.concat(
    (pandas.read_csv(file, encoding='utf-8') for file in files), 
    ignore_index=True
)

def getBrands():
    return list(_df['source'].unique())

def getColorSpaces():
    return ['RGB', 'LAB']

def hex_to_rgb(value):
    h = value.lstrip('#')
    lv = len(h)
    return tuple(int(h[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def euclidean_distance(color1, color2):
    return math.sqrt((color2[0]-color1[0])**2 + (color2[1]-color1[1])**2 + (color2[2]-color1[2])**2)
    # # Euclidean Distance (Weighted)
    # return math.sqrt(((color2[0]-color1[0])*0.30)**2 + ((color2[1]-color1[1])*0.59)**2 + ((color2[2]-color1[2])*0.11)**2)


def calculate_color_distance(color1_hex, color2_hex, algorithm='euclidean', color_space='RGB'):
    color1 = None
    color2 = None
    
    # Convert hex color to desired color space
    if 'RGB' == color_space.upper():
        color1 = hex_to_rgb(color1_hex)
        color2 = hex_to_rgb(color2_hex)
    elif 'LAB' == color_space.upper():
        color1 = skimage.color.rgb2lab([i/255 for i in hex_to_rgb(color1_hex)])
        color2 = skimage.color.rgb2lab([i/255 for i in hex_to_rgb(color2_hex)])
    else:
        raise ValueError(f"Unsupported Color Space = '{color_space}'")

    # Run distance calculation algorithm
    if 'euclidean' == algorithm:
        return euclidean_distance(color1, color2)
    else:
        raise ValueError(f"Unsupported Algorithm = '{algorithm}'")


def search(desired_color_hex, matches=1, brands=[], algorithm='euclidean', color_space='RGB', **kwargs):
    df = _df.copy()
    if brands and len(brands):
        df = df[df['source'].isin(brands)]
    df['distance'] = df.apply(lambda row: calculate_color_distance(desired_color_hex, row['color_hex'], algorithm=algorithm, color_space=color_space), axis=1)
    return [row[1].to_dict() for row in df.sort_values('distance').head(matches).iterrows()]




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='FindMePaint',
                    description='Converts hex color codes to paint colors',
                    epilog='Happy searching!!')
    parser.add_argument('-c', '--color', type=str, required=True, help="hex color code to search for")
    parser.add_argument('-m', '--matches', type=int, default=1, help="number of matches")
    parser.add_argument('-s', '--space', type=str, default="RGB", help="color space to use")
    args = parser.parse_args()
    for color in search(args.color, space=args.space, matches=args.matches):
        print(color)

