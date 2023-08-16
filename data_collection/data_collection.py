from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from bs4 import BeautifulSoup

days = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
website = 'http://webapps.daff.gov.za/amis/amis_price_search.jsp'

driver_path = r'/Users/semihozer/Desktop/ds_agriculture_project/data_collection/chromedriver'

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.implicitly_wait(20)

# Find the select element with id 'cbSearchMarket'
market_select = Select(driver.find_element(By.ID, 'cbSearchMarket'))

# Extract the visible text for each market
markets = [market.get_attribute('innerHTML') for market in market_select.options]

# Find the select element with id 'cbSearchProduct'
product_select = Select(driver.find_element(By.ID, 'cbSearchProduct'))

# Extract the values for each product
products = [product.get_attribute('value') for product in product_select.options][1:]



def collect_data(market, product,sleep_time):
    # Select the desired options
    period_select = Select(driver.find_element(By.ID, 'cbPeriod'))
    period_select.select_by_visible_text('Last 90 Days')

    # Select the market and product
    market_select = Select(driver.find_element(By.ID, 'cbSearchMarket'))
    market_select.select_by_visible_text(market)
    product_select = Select(driver.find_element(By.ID, 'cbSearchProduct'))
    product_select.select_by_value(product)

    # Select the default options for other filters
    variety_select = Select(driver.find_element(By.ID, 'cbSearchVariety'))
    variety_select.select_by_visible_text('All Varieties')
    class_select = Select(driver.find_element(By.ID, 'cbSearchClass'))
    class_select.select_by_visible_text('All Classes')
    size_select = Select(driver.find_element(By.ID, 'cbSearchSize'))
    size_select.select_by_visible_text('All Sizes')
    package_select = Select(driver.find_element(By.ID, 'cbSearchContainer'))
    package_select.select_by_visible_text('All Packages')

    # Find and click the "View Prices" button
    view_prices_button = driver.find_element(By.ID, 'btnDBSearch')
    view_prices_button.click()

    # Wait for the results to load
    # You may need to change sleep time up to number of result
    time.sleep(sleep_time)

    # Check if "No price available!" text exists in the page source
    if 'NO PRICES AVAILABLE!' in driver.page_source:
        return None

    # Get html code of table and convert it to dataframe
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.select_one(".displayscroll")
    if div:
        children = div.findChildren()
    else:
        print(f"{market} could not uploaded")
        return None
    tables = pd.read_html(str(children[0]))

    # Pre-cleaning of dataset
    if tables:
        df = tables[0]
        df = df.rename(columns=df.iloc[0]).drop(df.index[0]).drop(df.index[1]).drop(df.index[2]).reset_index(drop=True)
        mask = df['Product'].str.contains('|'.join(days), case=False)
        df = df[~mask]
        df['Product'] = df['Product'].str.replace(r'^\d+\.\s*', '')
        df['Market'] = market
        dataframes.append(df)
        print(df)


print(products)
print(markets)


# Add product codes that you want to get data
products = ['0030','0086','0061','0189','0072']

for product in products:
    dataframes = []
    for market in markets:
        collect_data(market,product,45)
    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df.to_csv(f"{merged_df['Product'][0]}.csv", index=False)