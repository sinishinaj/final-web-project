import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def do_login(driver, base_url):
    """Perform login and wait until #app is visible."""
    driver.get(base_url)
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("@Dm1n")
    driver.find_element(By.CSS_SELECTOR, "#loginPage button").click()
    WebDriverWait(driver, 5).until(
        lambda d: "hidden" not in d.find_element(By.ID, "app").get_attribute("class")
    )


def test_login_reveals_app(driver, local_server):
    do_login(driver, local_server)

    app_classes = driver.find_element(By.ID, "app").get_attribute("class")
    assert "hidden" not in app_classes


def test_contact_form(driver, local_server):
    do_login(driver, local_server)

    # Navigate to the Contact page via the nav inside #app
    driver.find_element(By.CSS_SELECTOR, "#app .nav button:nth-child(3)").click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "contact"))
    )

    # Fill in the contact form
    driver.find_element(By.ID, "name").send_keys("Alex")
    driver.find_element(By.ID, "email").send_keys("alex@gmail.com")
    driver.find_element(By.ID, "phone").send_keys("0000000")
    driver.find_element(By.ID, "message").send_keys("Hello world.")

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "#contact button[type='submit']").click()

    # Assert success message
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "formSuccess"), "Message sent successfully!")
    )
    success_text = driver.find_element(By.ID, "formSuccess").text
    assert success_text == "Message sent successfully!"


def test_logout_hides_app(driver, local_server):
    do_login(driver, local_server)

    # Click the logout button inside #app
    driver.find_element(By.CSS_SELECTOR, "#app .logout").click()

    # Page reloads on logout — wait for #app to have the 'hidden' class again
    WebDriverWait(driver, 5).until(
        lambda d: "hidden" in d.find_element(By.ID, "app").get_attribute("class")
    )

    app_classes = driver.find_element(By.ID, "app").get_attribute("class")
    assert "hidden" in app_classes
