import sys
import os

# Get the current directory of the test script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the path to the parent directory (containing 'src') to sys.path
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# Now you should be able to import from 'src'
from src.infinite_scroll_scrapping import scrapping
import pytest
from selenium import webdriver
from src.infinite_scroll_scrapping import scrapping
from src.infinite_scroll_scrapping import saveToDB


# Define a fixture to initialize the WebDriver
@pytest.fixture(scope="module")
def driver():
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)  # Wait up to 3 seconds for elements to appear
    yield driver
    # Close the WebDriver
    driver.quit()

# Define the pytest test function
def test_scrapping(driver):
    # Call the scrapping function with the initialized WebDriver
    scraped_data = scrapping(driver)
    saveToDB(scraped_data)
    

    # Print the scraped data (for demonstration)
    # Assert title and price for each scraped item
    for item in scraped_data:
        assert len(item) == 2, "Each scraped item should contain title and price"
        assert item[0], "Title should not be empty"
        assert item[1], "Price should not be empty"

    # Print the scraped data (for demonstration)
    print("Scraped Data:")
    for title, price in scraped_data:
        print(f"Title: {title}, Price: {price}")

if __name__ == "__main__":
    pytest.main()