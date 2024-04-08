import math
import numpy
import pandas
import argparse


_df = pandas.read_csv('data/paint_colors.csv', encoding='utf-8')

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def calculate_color_distance(color1_hex, color2_hex, weighted=False):
	# https://en.wikipedia.org/wiki/Color_difference
	# https://stackoverflow.com/questions/1847092/given-an-rgb-value-what-would-be-the-best-way-to-find-the-closest-match-in-the-d
	color1 = hex_to_rgb(color1_hex)
	color2 = hex_to_rgb(color2_hex)
	# Euclidean Distance (Unweighted)
	if not weighted:
		return math.sqrt((color2[0]-color1[0])**2 + (color2[1]-color1[1])**2 + (color2[2]-color1[2])**2)
	# Euclidean Distance (Weighted)
	return math.sqrt(((color2[0]-color1[0])*0.30)**2 + ((color2[1]-color1[1])*0.59)**2 + ((color2[2]-color1[2])*0.11)**2)

def search(desired_color_hex, weighted=False, matches=1):
	df = _df.copy()
	results = df[df['color_hex'] == desired_color_hex]
	df['distance'] = df.apply(lambda row: calculate_color_distance(desired_color_hex, row['color_hex'], weighted=weighted), axis=1)
	df.sort_values('distance', inplace=True)
	return [row[1].to_dict() for row in df.head(matches).iterrows()]


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
                    prog='FindMePaint',
                    description='Converts hex color codes to paint colors',
                    epilog='Happy searching!!')
	parser.add_argument('-c', '--color', type=str, required=True, help="hex color code to search for")
	parser.add_argument('-m', '--matches', type=int, default=1, help="number of matches")
	parser.add_argument('-w', '--weighted', action='store_true', help="apply weighting to color distance algorithm")
	args = parser.parse_args()
	for color in search(args.color, weighted=args.weighted, matches=args.matches):
		print(color)


# colors = [
# 	'#ebe7ce',
# 	'#bfcc96',
# 	'#5c6b4c',
# 	'#2e3641',
# 	'#4a303d',
# 	'#af7180'
# ]
