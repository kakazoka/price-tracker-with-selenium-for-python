from datetime import datetime
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


service = Service(SERVICE_PATH)

browser_options = Options()
browser_options.add_argument('--headless')

driver = webdriver.Edge(service=service, options=browser_options)

urls = {
    'graphics_card': 'https://www.kabum.com.br/produto/472671/placa-de-video-galax-nvidia-geforce-rtx-4060-ti-click-oc-8gb-gddr6-dlss-ray-tracing-46isl8md8coc',
    'motherboard': 'https://www.kabum.com.br/produto/114338/placa-mae-msi-b550m-pro-vdh-wifi-amd-am4-matx',
    'processor': 'https://www.kabum.com.br/produto/129459/processador-amd-ryzen-7-5800x-3-8ghz-4-7ghz-max-turbo-cache-36mb-octa-core-16-threads-am4-100-100000063wof'
}

price_thresholds = {
    'graphics_card': 2499.99,
    'motherboard': 799.99,
    'processor': 1457.99
}

products = []
for product, url in urls.items():
    try:
        driver.get(url)
        title = driver.find_element(By.CLASS_NAME, 'brTtKt').text.strip()
        price = driver.find_element(By.CLASS_NAME, 'finalPrice').text.strip()
        cleaned_price = float(price.replace('R$', '').replace('.', '').replace(',', '.'))
        link = url
        products.append({'Product': product, 'Title': title, 'Price': cleaned_price, 'Link': link})
    except Exception as error:
        print(f'An error occurred: {error}.')

driver.quit()

df = pd.DataFrame(products)

low_price_products = df[df.apply(lambda row: row['Price'] <= price_thresholds[row['Product']], axis=1)]

if not low_price_products.empty:
    current_date = datetime.now().strftime('%d-%m-%Y')
    save_path = SAVE_PATH
    os.makedirs(save_path, exist_ok=True)
    csv_file = os.path.join(save_path, f'prices_{current_date}.csv')
    low_price_products.to_csv(csv_file, index=False)
    print(f'Products within the price range saved to {csv_file}.')
else:
    print('No products within the price range.')