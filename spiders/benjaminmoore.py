import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color


driver = webdriver.Chrome()

driver.get('https://www.benjaminmoore.com/en-us/paint-colors/color-families')


def _parseColorTile(element):
	rgba = element.value_of_css_property('background-color')
	color = Color.from_string(rgba)
	name = element.find_element(By.CSS_SELECTOR, 'div.colorInfoDiv p.colorName').get_attribute('textContent')
	code = element.find_element(By.CSS_SELECTOR, 'div.colorInfoDiv p.colorCode').get_attribute('textContent')
	link = element.find_element(By.CSS_SELECTOR, 'div.colorInfoLink a').get_attribute('href')
	# if not name or not code:
	# 	parts = link.split('/')[-2:]
	# 	code = parts[0]
	# 	name = parts[1].replace('-', ' ').title()
	return { 
		'name': name,
		'code': code,
		'link': link,
		'source': 'benjaminmoore',
		'color_hex': color.hex,
		'color_r': color.red,
		'color_g': color.green,
		'color_b': color.blue
	}


def _closeAllPopups():
	time.sleep(0.5)
	css_selectors = ['button.bx-button', 'button.onetrust-close-btn-handler', 'div._pi_closeButton', 'button..bx-close-link']
	for css_selector in css_selectors:
		try:
			driver.find_element(By.CSS_SELECTOR, css_selector).click()
		except:
			pass


# Get "Color By Family" page links
elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="ColorWallHeader_ViewAllLink"]')
pages = [element.get_attribute('href') for element in elements]

# Loop through page link
colorTiles = []
for page in pages:
	# Navigate to page
	driver.get(page)

	# Extract each color tile
	nextButtonElement = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="Pagination_NextPageButton"]')
	while True:
		elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="ColorTile"]')
		colorTiles += [
			_parseColorTile(element) for element in elements
		]
		if not nextButtonElement.is_enabled():
			break
		try:
			_closeAllPopups()
			nextButtonElement.click()
		except Exception as err:
			print(err)
			time.sleep(2.5)
			_closeAllPopups()
			nextButtonElement.click()



driver.close()


with open('benjaminmoore_paint_colors.csv', 'w', newline='', encoding='utf-8') as fh:
	fieldnames = list(colorTiles[0].keys())
	writer = csv.DictWriter(fh, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(colorTiles)