import json
import csv
from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc
import psutil
from multiprocessing import Pool
import os
import json
from curl_cffi import requests
import random
import tldextract


def get_domain(url):
	try:
		parsed_url = tldextract.extract(url)
		if parsed_url.suffix == '':
			return parsed_url.domain
		return parsed_url.domain + '.' + parsed_url.suffix
	except:
		return url


def get_base_url(url):
	try:
		https = "https://" in url
		prefix = "https://" if https else "http://"
		parsed_url = tldextract.extract(url)
		if parsed_url.suffix == '':
			return prefix + parsed_url.domain
		return prefix + parsed_url.domain + '.' + parsed_url.suffix
	except:
		return url


def get_site_name(url):
	try:
		parsed_url = tldextract.extract(url)
		return parsed_url.domain
	except:
		return url


def get_page(url, page, collection_handle, printer=print, min_wait_time=30, max_wait_time=100):
	import time
	full_url = url
	if collection_handle:
		full_url += '/collections/{}'.format(collection_handle)
	full_url += '/products.json'
	page_url = full_url + '?page={}'.format(page)
	num_trials = 3
	while True:
		try:
			data = requests.get(page_url, impersonate="chrome101", timeout=10)
			if data.status_code == 200:
				data = data.text
				break
			elif data.status_code == 404:
				break
			else:
				raise EnvironmentError("get_page Error: ", data.status_code, "for:", page_url)
		except:
			wait_time = random.randint(min_wait_time, max_wait_time)
			printer('Does not work get_page for:' + page_url,
					"trying to sleep for", wait_time, "seconds")
			num_trials -= 1
			if not num_trials:
				return []
			printer('Will retry', num_trials, 'more times')
			time.sleep(wait_time)

	products = json.loads(data)['products']
	return products


def get_page_collections(url, printer=print, min_wait_time=30, max_wait_time=100):
	import time
	full_url = url + '/collections.json'
	page = 1
	page_url = full_url + '?page={}'.format(page)
	collections = []
	while True:
		page_url = full_url + '?page={}'.format(page)
		num_trials = 3
		while True:
			try:
				data = requests.get(page_url, impersonate="chrome101", timeout=10)
				if data.status_code == 200:
					data = data.text
					break
				elif data.status_code == 404:
					break
				else:
					raise EnvironmentError("get_page_collections Error: ", data.status_code, "for:", page_url)
			except:
				wait_time = random.randint(min_wait_time, max_wait_time)
				printer('Does not work get_page_collections for:' + page_url,
						"trying to sleep for", wait_time, "seconds")
				num_trials -= 1
				if not num_trials:
					break
				printer('Will retry', num_trials, 'more times')
				time.sleep(wait_time)

		if num_trials:
			try:
				cols = json.loads(data)['collections']
			except:
				break
			if not cols:
				break
			for col in cols:
				collections.append(col)
		page += 1
	return collections


def fix_url(url):
	fixed_url = url.strip()
	if not fixed_url.startswith('http://') and \
			not fixed_url.startswith('https://'):
		fixed_url = 'https://' + fixed_url

	return fixed_url.rstrip('/')


def extract_products_collection(url, col, printer=print):
	page = 1
	products = get_page(url, page, col, printer)
	parsed_products = []
	while products:
		for product in products:
			title = product['title']
			product_type = product['product_type']
			product_url = url + '/products/' + product['handle']
			product_handle = product['handle']

			def get_image(variant_id):
				if variant_id is None:
					return ''
				images = product['images']
				for i in images:
					k = [str(v) for v in i['variant_ids']]
					if str(variant_id) in k:
						return i['src']

				return ''

			for i, variant in enumerate(product['variants']):
				price = variant['price'] if variant["price"] is not None else ''
				option1_value = (variant['option1'] or '') if variant['option1'] is not None else ''
				option2_value = (variant['option2'] or '') if variant['option2'] is not None else ''
				option3_value = (variant['option3'] or '') if variant['option3'] is not None else ''
				option_value = ' '.join([option1_value, option2_value,
										 option3_value]).strip()
				sku = variant['sku'] if variant["sku"] is not None else ''
				main_image_src = ''
				if product['images']:
					main_image_src = product['images'][0]['src']

				image_src = get_image(variant['id']) or main_image_src
				stock = 'Yes'
				if not variant['available']:
					stock = 'No'

				row = {'sku': sku, 'product_type': product_type,
					   'title': title, 'option_value': option_value,
					   'price': price, 'stock': stock, 'body': str(product['body_html']),
					   'variant_id': product_handle + str(variant['id']),
					   'product_url': product_url, 'image_src': image_src}
				for k in row:
					row[k] = str(row[k].strip()) if row[k] else ''
				parsed_products.append(row)

		page += 1
		products = get_page(url, page, col, printer)
	return parsed_products


def extract_products(url, col, printer=print):
	inventory_of_collection = []
	seen_variants = set()

	handle = col['handle']
	title = col['title']
	products = extract_products_collection(url, handle, printer)

	for product in products:
		variant_id = product['variant_id']
		if variant_id in seen_variants:
			continue
		seen_variants.add(variant_id)

		inventory_of_collection.append(
			{
				"Code": product['sku'],
				"Collection": str(title),
				"Category": product['product_type'],
				"Name": product['title'],
				"Variant Name": product['option_value'],
				"Price": product['price'],
				"In Stock": product['stock'],
				"URL": product['product_url'],
				"Image URL": product['image_src'],
				"Body": product["body"]
			})
	return inventory_of_collection


def parse_inventory(url, printer):
	import time
	url = fix_url(url)
	time.sleep(random.randint(1, 10))
	collections = get_page_collections(url, printer)
	inventory = {}
	wait_pattern = 1
	for collection in collections:
		printer('Extracting collection: {}'.format(collection['handle']) + " from:" + url)
		inventory[collection['handle']] = extract_products(url, collection, printer)
		wait_time = int(wait_pattern / 10)
		time.sleep(wait_time)
		wait_pattern += 1
		if wait_pattern > 100:
			wait_pattern = 1

	return inventory


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=options)

stealth(browser,
		languages=["en-US", "en"],
		vendor="Google Inc.",
		platform="Win32",
		webgl_vendor="Intel Inc.",
		renderer="Intel Iris OpenGL Engine",
		fix_hairline=True,
		)


# uc_options = webdriver.ChromeOptions()
# uc_options.add_argument("--headless")
# uc_options.add_argument("start-maximized")
##uc_options.add_experimental_option("excludeSwitches", ["enable-automation"])
##uc_options.add_experimental_option('useAutomationExtension', False)
# uc_browser = uc.Chrome(options=uc_options)


def get_shopify_indexes(site_list_csv_path: str, export_dir="./data"):
	with open(site_list_csv_path, 'r') as file:
		reader = csv.reader(file)
		sites = [row[0] for row in reader]

	site_order = 0
	shopify_sites = []
	for site in sites:
		site_order += 1
		base_url = get_base_url(site)
		if base_url is None:
			continue
		try:
			response = requests.get(base_url, timeout=5)
			if response.status_code == 200:
				page = response.text
			else:
				print("Error: ", response.status_code, " at line:", site_order, "repeating with selenium", base_url)
				browser.get(base_url)
				page = str(browser.page_source)
		except:
			continue

		if "shopify" in str(page):
			shopify_sites.append([site_order, base_url])
			print(str(len(shopify_sites)) + ". shopify site found in initial at line:", site_order, base_url)

	with open(export_dir + "/" + 'shopify_sites.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['site_order', 'site_url'])
		for site in shopify_sites:
			writer.writerow(site)


def find_shopify_sites(site_list_csv_path: str, export_dir="./data"):
	sites = []
	with open(site_list_csv_path, 'r') as file:
		reader = csv.reader(file)
		sites = [row[0] for row in reader]

	site_order = 0
	shopify_sites = []
	for site in sites:
		site_order += 1
		base_url = get_base_url(site)
		thanks_selenium = False
		if base_url is None:
			continue
		try:
			response = requests.get(base_url, timeout=5)
			if response.status_code == 200:
				page = response.text
			else:
				print("Error: ", response.status_code, " at line:",
					  site_order, "repeating with selenium", base_url)
				browser.get(base_url)
				page = str(browser.page_source)
				thanks_selenium = True
		except:
			continue

		if "shopify" in str(page):
			if get_page(base_url, 1, None, print):
				shopify_sites.append([site_order, thanks_selenium, base_url])
				print(str(len(shopify_sites)) + ". shopify site found in initial csv at line:",
					  site_order, base_url)

	with open(export_dir + "/" + 'shopify_sites.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow(['site_order', 'needs_selenium', 'site_url'])
		for site in shopify_sites:
			writer.writerow(site)


def process_site(row, printer=print, export_dir="./data"):
	needs_selenium = row[1] == "True"
	url = row[2]
	key = get_site_name(url)
	inventory = parse_inventory(url, printer)
	with open(export_dir + "/" + key + '_shopify_products.json', 'w') \
			as site_products_json:
		json.dump({key: inventory}, site_products_json)


def build_shopify_set(sites_csv_path: str, export_dir="./data", parallel=True):
	file_list = os.listdir(export_dir)
	sites = []
	with open(sites_csv_path, 'r') as file:
		reader = csv.reader(file)
		row_index = 0
		for row in reader:
			if row_index == 0:
				row_index += 1
				continue

			url = row[2]
			key = get_site_name(url)
			if key + "_shopify_products.json" in file_list:
				print("Skipping", key)
				continue
			sites.append(row)
			row_index += 1

	if parallel:
		with Pool(len(sites)) as p:
			p.map(process_site, sites)
	else:
		for row in sites:
			process_site(row, export_dir=export_dir, printer=print)


def main(random_site_list_path_maybe_csv="stores.csv"):
	find_shopify_sites(random_site_list_path_maybe_csv)  # -> shopify_sites.csv
	build_shopify_set("shopify_sites.csv",
					  export_dir="./data", parallel=True)  # -> data/xxx_shopify_products.json


if __name__ == "__main__":
	main()
