import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color


driver = webdriver.Chrome()

driver.get('https://www.glidden.com/color/color-families/browse-all-colors')


def _parseColorTile(element):
	rgba = element.value_of_css_property('background-color')
	color = Color.from_string(rgba)
	name = element.find_element(By.CSS_SELECTOR, 'div.color-rect-tip div.color-rect-text h3').get_attribute('textContent')
	code = element.find_element(By.CSS_SELECTOR, 'div.color-rect-tip div.color-rect-text span.color-rect-code').get_attribute('textContent')
	link = element.get_attribute('href')
	return { 
		'name': name,
		'code': code,
		'link': link,
		'source': 'glidden',
		'color_hex': color.hex,
		'color_r': color.red,
		'color_g': color.green,
		'color_b': color.blue
	}


elements = driver.find_elements(By.CSS_SELECTOR, 'a.color-rect')

colorTiles = [
	_parseColorTile(element) for element in elements
]

driver.close()


with open('glidden_paint_colors.csv', 'w', newline='', encoding='utf-8') as fh:
	fieldnames = list(colorTiles[0].keys())
	writer = csv.DictWriter(fh, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(colorTiles)