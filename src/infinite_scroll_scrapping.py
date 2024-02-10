from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import pandas as pd
import psycopg2

def scrapping(driver):
    # # Initialize the Chrome WebDriver
    # driver = webdriver.Chrome()
    # driver.implicitly_wait(3)  # Wait up to 3 seconds for elements to appear
    # Scroll to the bottom of the page to load more items
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new items to load
        time.sleep(2)

        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract data from loaded items
    items = driver.find_elements(By.XPATH, "//div[contains(@class, 'post')]")
    data = []
    for item in items:
        # Get specific elements from each item
        title_element = item.find_element(By.XPATH, ".//h4/a")
        price_element = item.find_element(By.XPATH, ".//h5")

        title = title_element.text
        price = price_element.text
        data.append([title, price])
    
    return data  

def saveToDB(data):
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data, columns=['Title', 'Price'])
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="web_scrap",
        user="postgres",
        password="postgres"
    )

    # Create a cursor object
    cur = conn.cursor()

    # Create a table in PostgreSQL database
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scraped_data (
            id SERIAL PRIMARY KEY,
            title TEXT,
            price TEXT
        )
    """)

    # Insert the DataFrame into the PostgreSQL database
    for _, row in df.iterrows():
        cur.execute("INSERT INTO scraped_data (title, price) VALUES (%s, %s)", (row['Title'], row['Price']))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()  

# Create a Chrome WebDriver instance
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://scrapingclub.com/exercise/list_infinite_scroll/?page")

# Call the scrapping function to extract data
data = scrapping(driver)

# Save the extracted data to the database
saveToDB(data)

# Quit the WebDriver
driver.quit()
 
