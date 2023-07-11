# shopify-scraper
(not a) Simple scraper to extract all products from shopify sites

Requirements:
```
undetected-chromedriver
selenium
selenium-stealth
curl_cffi
tldextract
```
Usage:
```
def main(random_site_list_path_maybe_csv="stores.csv"):
	find_shopify_sites(random_site_list_path_maybe_csv)  # -> shopify_sites.csv
	build_shopify_set("shopify_sites.csv",
					  export_dir="./data", parallel=True)  # -> data/xxx_shopify_products.json
```

Long story:
* Hava text file with many sites; typos don't matter.
* Don't worry about Cloudflare or less painful measurements; selenium-stealth and curl_cffi, which is a curl-impersonate wrapper will take care of them.
* What we do here may trigger DDOS filters, or the site may actually in trouble at that moment; in this case, the script will wait some (random) time for a few more trials. Works well so far.
* Of course, there is multiprocessing. 

Here how each site dump looks like:
```json
{
  "mybossfurniture": {
    "3-piece-reclining-sectional": [],
    "4-piece-reclining-sectional": [],
    "5-piece-reclining-sectional-with-chaise": [],
    "accent-tables": [],
    "ashley-furniture": [],
    "barstool-chairs": [],
    "bedroom-sets": [],
    "chair-side-tables": [],
    "chest-of-drawers": [],
    "coffee-tables": [],
    "consoles": [],
    "deals": [],
    "dining-room-chairs": [],
    "dresser-and-mirror": [],
    "dressers": [],
    "end-and-side-tables": [],
    "entertainment-center": [],
    "fireplace-insert": [],
    "full-foundation": [],
    "full-mattress": [],
    "home-page": [],
    "king-mattresses": [],
    "loveseat": [],
    "mattress-in-a-box": [],
    "nightstands": [],
    "ottomans": [],
    "power-sofas": [],
    "queen-foundation": [],
    "headboards": [],
    "queen-mattresses": [],
    "recliners": [
      {
        "Code": "",
        "Collection": "Recliners",
        "Category": "recliner",
        "Name": "Recliner",
        "Variant Name": "Default Title",
        "Price": "199.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/recliner",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_8547.jpg?v=1667752652",
        "Body": "Recliner Gray"
      }
    ],
    "reclining-loveseat": [],
    "reclining-power-loveseat": [],
    "reclining-sofas": [],
    "rugs": [],
    "sectionals-1": [],
    "sleeper-sofas": [],
    "sofa-table": [],
    "special-offers": [
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "recliner",
        "Name": "Recliner",
        "Variant Name": "Default Title",
        "Price": "199.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/recliner",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_8547.jpg?v=1667752652",
        "Body": "Recliner Gray"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Sectional",
        "Variant Name": "Default Title",
        "Price": "1799.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/sectional-2",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_8548.jpg?v=1667752518",
        "Body": "Sectional Gray"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Reclining Sofa & Loveseat",
        "Variant Name": "Default Title",
        "Price": "2499.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/reclining-sofa-loveseat",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_8550.jpg?v=1667752372",
        "Body": "Power Reclining Sofa &amp; Power Reclining Loveseat Black"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Sectional",
        "Variant Name": "Default Title",
        "Price": "1499.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/sectional-1",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_7748.jpg?v=1667688140",
        "Body": "Velvet Sectional Gray"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Queen Bed Dresser Mirror",
        "Variant Name": "Default Title",
        "Price": "899.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/queen-bed-dresser-mirror-1",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_7460.jpg?v=1667688042",
        "Body": "Queen Bed Dresser Mirror. Mattress Sold Sepratley"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Fireplace",
        "Variant Name": "Default Title",
        "Price": "799.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/fireplace",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_6225.jpg?v=1667687897",
        "Body": "Mirrored Fireplace"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Reclining Sofa & Reclining Loveseat",
        "Variant Name": "Default Title",
        "Price": "1099.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/reclining-sofa-reclining-loveseat",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/6D5708FF-F5A2-41AF-BBBA-54CC6FE600B4.jpg?v=1667687639",
        "Body": "Reclining Sofa &amp; Reclining Loveseat"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Sectional",
        "Variant Name": "Default Title",
        "Price": "699.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/sectional",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/CD2C527A-EBBA-4610-8CDF-358414708639.jpg?v=1667687545",
        "Body": "Sectional Black"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Queen Bed Dresser Mirror",
        "Variant Name": "Default Title",
        "Price": "799.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/queen-bed-dresser-mirror",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_8536.jpg?v=1667687216",
        "Body": "Queen Bed Dresser Mirror Gray ----Mattress Sold Separately"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "",
        "Name": "Queen Storage Bed",
        "Variant Name": "Default Title",
        "Price": "799.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/queen-storage-bed",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_7744.jpg?v=1667686902",
        "Body": "Queen Storage Bed Gray"
      },
      {
        "Code": "",
        "Collection": "Special Offers",
        "Category": "Queen Upholstered Bed",
        "Name": "Queen Bed",
        "Variant Name": "Default Title",
        "Price": "999.00",
        "In Stock": "Yes",
        "URL": "https://mybossfurniture.com/products/queen-bed",
        "Image URL": "https://cdn.shopify.com/s/files/1/0072/2609/7746/products/IMG_7953.jpg?v=1667686217",
        "Body": "Queen Storage Round Bed Black"
      }
    ],
    "tv-stands-and-media-centers": [],
    "twin-mattresses": [],
    "vanities": []
  }
}
```
