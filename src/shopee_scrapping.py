from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://google.com"
driver = webdriver.Chrome()
driver.get("https://shopee.co.id/")  # Open Shopee website
def loginShoope():
    # Wait for login to complete
    WebDriverWait(driver, 10).until(EC.url_contains("shopee.co.id/buyer/login"))
    # Simulate entering username and password
    username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "loginKey")))
    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))
    username.send_keys("your_username")  # Replace "your_username" with your actual Shopee username
    password.send_keys("your_password")  # Replace "your_password" with your actual Shopee password

    # Submit the login form
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log in')]")))
    login_button.click()

    # Verify if login was successful
    if "shopee.co.id" in driver.current_url:
        print("Login successful!")
    else:
        print("Login failed!")

# driver.find_element(By.CSS_SELECTOR,".shopee-popup__close-btn").click()
loginShoope()
# Start the timer
start_time = time.time()
while time.time() - start_time < 10000:
    pass


# Search for a product
search_box = driver.find_element(By.CSS_SELECTOR,".shopee-searchbar-input__input")
search_box.send_keys("Your Product Name")  # Replace "Your Product Name" with the name of the product you want to search for
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)  # Adjust the sleep time according to your internet speed

# Get the product details
product_elements = driver.find_element(By.CSS_SELECTOR,".col-xs-2-4") # Adjust the class name based on the HTML structure of Shopee search results
for product_element in product_elements:
    product_name = product_element.find_element(By.CSS_SELECTOR,".yQmmFK").text
    product_price = product_element.find_element(By.CSS_SELECTOR,"._1w9jLI").text
    
    print("Product:", product_name)
    print("Price:", product_price)

# Close the webdriver
while(True):
    pass

#i have to login with my real acc !