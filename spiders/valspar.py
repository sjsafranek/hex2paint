import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color


driver = webdriver.Chrome()

driver.get('https://www.valspar.com/en/colors/browse-colors')
time.sleep(2.5)

def _parseColorTile(element):
	rgba = element.find_element(By.CSS_SELECTOR, 'div.cbg-color-swatch').value_of_css_property('background-color')
	color = Color.from_string(rgba)
	name = element.get_attribute('data-color-name')
	code = element.get_attribute('data-color-id')
	link = element.get_attribute('href')
	return { 
		'name': name,
		'code': code,
		'link': link,
		'source': 'valspar',
		'color_hex': color.hex,
		'color_r': color.red,
		'color_g': color.green,
		'color_b': color.blue
	}


# Accept cookies
driver.find_element(By.CSS_SELECTOR, 'button#ensAcceptBanner').click()

colorsCaptured = set()
colorTiles = []

# Load all color tiles
button = driver.find_element(By.CSS_SELECTOR, 'div.button-container__load-more button')
while True:
	elements = driver.find_elements(By.CSS_SELECTOR, 'div.grid--wall.grid--wall__color a.color-anchor')
	
	for element in elements:
		cid = element.get_attribute('data-color-id') 
		if cid and cid not in colorsCaptured:
			colorsCaptured.add(cid)
			colorTiles.append(_parseColorTile(element))
	
	print(len(colorTiles))

	break

	if not button.is_displayed:
		break

	button.click()
	time.sleep(0.25)


driver.close()


with open('valspar_paint_colors.csv', 'w', newline='', encoding='utf-8') as fh:
	fieldnames = list(colorTiles[0].keys())
	writer = csv.DictWriter(fh, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(colorTiles)