import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color


driver = webdriver.Chrome()

driver.get('https://www.acehardware.com/thepaintstudio/colors#brand:clarkkensington|palette:clarkkensington|')

time.sleep(2.5)

driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()

time.sleep(2.5)


def _parseColorTile(element):
	element.click()	
	rgba = element.value_of_css_property('background-color')
	color = Color.from_string(rgba)
	name = element.find_element(By.CSS_SELECTOR, 'div.itemName').get_attribute('textContent')
	code = element.find_element(By.CSS_SELECTOR, 'div.itemCode').get_attribute('textContent')
	link = driver.current_url
	return { 
		'name': name,
		'code': code,
		'link': link,
		'source': 'clarkkensington',
		'color_hex': color.hex,
		'color_r': color.red,
		'color_g': color.green,
		'color_b': color.blue
	}


button_classes = [
	"classicwhite",
	"coolneutral",
	"warmneutral",
	"red",
	"orange",
	"yellow",
	"green",
	"blue",
	"purple"
]

colorTiles = []

for button_class in button_classes:
	driver.execute_script("window.scrollTo(0, 0)")
	button = driver.find_element(By.CSS_SELECTOR, f'button.{button_class}')
	button.click()
	time.sleep(0.5)
	elements = driver.find_elements(By.CSS_SELECTOR, "#gridItems button.item")
	colorTiles += [
		_parseColorTile(element) for element in elements
	]


driver.close()


with open('clarkkensington_paint_colors.csv', 'w', newline='', encoding='utf-8') as fh:
	fieldnames = list(colorTiles[0].keys())
	writer = csv.DictWriter(fh, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(colorTiles)