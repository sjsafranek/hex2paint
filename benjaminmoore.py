import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color


driver = webdriver.Chrome()

driver.get('https://www.benjaminmoore.com/en-us/paint-colors/color-families')


# Get "Color By Family" page links
elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="ColorWallHeader_ViewAllLink"]')
pages = [element.get_attribute('href') for element in elements]

def _parseColorTile(element):
	rgba = element.value_of_css_property('background-color')
	color = Color.from_string(rgba)
	return { 
		'name': element.find_element(By.CSS_SELECTOR, 'div.colorInfoDiv p.colorName').text,
		'code': element.find_element(By.CSS_SELECTOR, 'div.colorInfoDiv p.colorCode').text,
		'link': element.find_element(By.CSS_SELECTOR, 'div.colorInfoLink a').get_attribute('href'),
		'source': 'benjaminmoore',
		'color_hex': color.hex,
		'color_r': color.red,
		'color_g': color.green,
		'color_b': color.blue
	}

def _closeAllPopups():
	css_selectors = ['button.onetrust-close-btn-handler', 'div._pi_closeButton', 'button..bx-close-link']
	for css_selector in css_selectors:
		try:
			driver.find_element(By.CSS_SELECTOR, css_selector).click()
		except:
			pass

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
			print('oops')
			input()




driver.close()


with open('data/paint_colors.csv', 'w', newline='', encoding='utf-8') as fh:
	fieldnames = list(colorTiles[0].keys())
	writer = csv.DictWriter(fh, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(colorTiles)