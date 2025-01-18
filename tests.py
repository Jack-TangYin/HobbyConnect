from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Global credentials for testing.
TEST_CREDENTIALS = {
    'prefix': '01',
    'username': 'TestUser2',
    'email': 'testuser2@example.com',
    'new_password': 'StrongPassword123!',
    'password': '12345678!',
    'date_of_birth': '01/01/2021',
    'hobbies': 'Football, Coding, Reading',
    'new_hobby': 'Cycling',
    'new_hobbies': 'Swimming, Eating'
}


class SignUpFormTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def testForm(self):
        driver = self.driver
        
        # Visit the signup page (adjust the URL if needed)
        driver.get("http://localhost:8000/register")
        time.sleep(2)  # Wait for the page to load
        
        # Locate fields in the signup form.
        username_field = driver.find_element(By.NAME, 'username')
        email_field = driver.find_element(By.NAME, 'email')
        date_of_birth_field = driver.find_element(By.NAME, 'date_of_birth')
        password1_field = driver.find_element(By.NAME, 'password1')
        password2_field = driver.find_element(By.NAME, 'password2')
        hobbies_field = driver.find_element(By.NAME, 'hobbies')
        submit_button = driver.find_element(By.ID, 'submit')
        
        # Fill in the form with data from the global variable.
        username_field.send_keys(TEST_CREDENTIALS['username'])
        email_field.send_keys(TEST_CREDENTIALS['email'])
        date_of_birth_field.send_keys(TEST_CREDENTIALS['date_of_birth'])
        password1_field.send_keys(TEST_CREDENTIALS['password'])
        password2_field.send_keys(TEST_CREDENTIALS['password'])
        hobbies_field.send_keys(TEST_CREDENTIALS['hobbies'])
        time.sleep(1)
        
        # Submit the form.
        submit_button.click()
        time.sleep(5)  # Wait for response or potential redirect
        
        # Verify that signup was successful.
        self.assertIn(TEST_CREDENTIALS['username'], driver.page_source)


class LoginFormTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def testForm(self):
        driver = self.driver
        # Navigate to the login page.
        driver.get("http://localhost:8000/login")
        time.sleep(1)
        
        # Locate the form fields and button.
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.ID, 'submit')
        time.sleep(1)

        # Use the global variable for test data.
        username_field.send_keys(TEST_CREDENTIALS['username'])
        password_field.send_keys(TEST_CREDENTIALS['password'])
        time.sleep(2)
        
        # Submit the form.
        submit_button.click()
        time.sleep(1)
        
        # Verify that login was successful.
        self.assertIn(TEST_CREDENTIALS['username'], driver.page_source)
        
        
class EditUserProfileTest(LiveServerTestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        # Set a larger viewport size so that the profile link is visible.
        # Adjust the width and height as needed.
        self.driver.set_window_size(1280, 800)

    def tearDown(self):
        # Quit the browser after each test.
        self.driver.quit()

    def testForm(self):
        driver = self.driver
        
        # Navigate to the login page.
        driver.get("http://localhost:8000/login")
        time.sleep(1)
        
        # Locate the form fields and button.
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.ID, 'submit')
        time.sleep(1)

        # Use the global variable for test data.
        username_field.send_keys(TEST_CREDENTIALS['username'])
        password_field.send_keys(TEST_CREDENTIALS['password'])
        time.sleep(1)
        
        # Submit the form.
        submit_button.click()
        time.sleep(1)
        
        # If the profile link is inside a dropdown that only shows on hover or click,
        # you might need to open the dropdown first.
        # Here, it's assumed that the profile link is directly accessible.
        menu_dropdown_button = driver.find_element(By.ID, 'menu-dropdown')
        menu_dropdown_button.click()
        profile_link = driver.find_element(By.ID, 'profile')
        profile_link.click()
        edit_profile_link = driver.find_element(By.ID, 'edit-profile')
        edit_profile_link.click()
        time.sleep(3)
        
        # Update Profile Details
        profile_username_field = driver.find_element(By.ID, 'username')
        profile_email_field = driver.find_element(By.ID, 'email')
        profile_date_of_birth_field = driver.find_element(By.ID, 'dateOfBirth')
        update_profile_button = driver.find_element(By.ID, 'update-profile')
        
        profile_username_field.send_keys(TEST_CREDENTIALS['prefix'] + TEST_CREDENTIALS['username'])
        profile_email_field.send_keys(TEST_CREDENTIALS['prefix'] + TEST_CREDENTIALS['email'])
        profile_date_of_birth_field.send_keys(TEST_CREDENTIALS['date_of_birth'])
        update_profile_button.click()
        time.sleep(1)
        
        return_button = driver.find_element(By.ID, 'return-button')
        return_button.click()
        
        time.sleep(3)
        
        # Verify that the profile was updated.
        self.assertIn(TEST_CREDENTIALS['prefix'] + TEST_CREDENTIALS['username'], driver.page_source)
        self.assertIn(TEST_CREDENTIALS['prefix'] + TEST_CREDENTIALS['email'], driver.page_source)
        self.assertIn(TEST_CREDENTIALS['date_of_birth'], driver.page_source)
        

class EditUserPasswordTest(LiveServerTestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        # Set a larger viewport size so that the profile link is visible.
        # Adjust the width and height as needed.
        self.driver.set_window_size(1280, 800)

    def tearDown(self):
        # Quit the browser after each test.
        self.driver.quit()

    def testForm(self):
        driver = self.driver
        
        # Navigate to the login page.
        driver.get("http://localhost:8000/login")
        time.sleep(1)
        
        # Locate the form fields and button.
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.ID, 'submit')
        time.sleep(1)

        # Use the global variable for test data.
        username_field.send_keys(TEST_CREDENTIALS['username'])
        password_field.send_keys(TEST_CREDENTIALS['password'])
        time.sleep(1)
        
        # Submit the form.
        submit_button.click()
        time.sleep(1)
        
        # If the profile link is inside a dropdown that only shows on hover or click,
        # you might need to open the dropdown first.
        # Here, it's assumed that the profile link is directly accessible.
        menu_dropdown_button = driver.find_element(By.ID, 'menu-dropdown')
        menu_dropdown_button.click()
        profile_link = driver.find_element(By.ID, 'profile')
        profile_link.click()
        edit_profile_link = driver.find_element(By.ID, 'edit-profile')
        edit_profile_link.click()
        time.sleep(3)
        
        
        # Update password fields
        profile_old_password_field = driver.find_element(By.ID, 'old_password')
        profile_new_password_field = driver.find_element(By.ID, 'new_password')
        profile_confirm_password_field = driver.find_element(By.ID, 'confirm_password')
        update_password_button = driver.find_element(By.ID, 'update-password')
                
        # Update the password fields.
        profile_old_password_field.send_keys(TEST_CREDENTIALS['password'])
        profile_new_password_field.send_keys(TEST_CREDENTIALS['new_password'])
        profile_confirm_password_field.send_keys(TEST_CREDENTIALS['new_password'])
        
        # Wait for the update password button to be clickable
        actions = ActionChains(driver)
        actions.move_to_element(update_password_button).click().perform()
        time.sleep(3)
        
        # Sign out
        actions.move_to_element(menu_dropdown_button).click().perform()
        sign_out_link = driver.find_element(By.ID, 'logout')
        sign_out_link.click()        
        time.sleep(1)
        
        # Log back in with the new password.
        login_username_field = driver.find_element(By.NAME, 'username')
        login_password_field = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.ID, 'submit')
        time.sleep(1)

        # Use the global variable for test data.
        login_username_field.send_keys(TEST_CREDENTIALS['username'])
        login_password_field.send_keys(TEST_CREDENTIALS['new_password'])
        time.sleep(2)
        login_button.click()
        time.sleep(1)
        
        # Verify that login was successful.
        self.assertIn(TEST_CREDENTIALS['username'], driver.page_source)
        

class AddAndRemoveHobbiesTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1280, 800)

    def tearDown(self):
        self.driver.quit()

    def login(self):
        """Helper method to log in the test user."""
        driver = self.driver
        driver.get("http://localhost:8000/login")
        # Wait until the username field is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.ID, 'submit')
        username_field.send_keys(TEST_CREDENTIALS['username'])
        password_field.send_keys(TEST_CREDENTIALS['password'])
        time.sleep(1)
        submit_button.click()
        # Wait until login processing is complete.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'menu-dropdown'))
        )

    def navigate_to_edit_profile(self):
        """Helper method to navigate to the edit profile page."""
        driver = self.driver
        menu_dropdown_button = driver.find_element(By.ID, 'menu-dropdown')
        menu_dropdown_button.click()
        time.sleep(1)
        profile_link = driver.find_element(By.ID, 'profile')
        profile_link.click()
        time.sleep(1)
        edit_profile_link = driver.find_element(By.ID, 'edit-profile')
        edit_profile_link.click()
        # Wait until the edit profile page is loaded.
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'new_hobby'))
        )

    def scroll_into_view(self, element):
        """Scrolls the element into view using JavaScript."""
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(1)

    def add_hobby(self, hobby_text):
        """
        Helper method to add a hobby.
        Assumes a text input with id 'new_hobby' and a button with id 'add-hobby'.
        """
        driver = self.driver
        # Wait for the add hobby input field to be visible.
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'new_hobby'))
        )
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'add-hobby'))
        )
        return_button = driver.find_element(By.ID, 'return-button')
        self.scroll_into_view(return_button)
        time.sleep(1)
        # Clear and send the hobby text.
        input_field.clear()
        input_field.send_keys(hobby_text)
        
        # Remove the dropdown menu from blocking the add button
        click_elsewhere = driver.find_element(By.ID, 'clear-password')
        click_elsewhere.click()
        time.sleep(1)
        
        add_button.click()
        time.sleep(1)
        # Allow some time for the UI to update.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"span#{hobby_text}"))
        )

    def remove_hobby(self, hobby_text):
        """
        Helper method to remove a hobby.
        Assumes the delete button has an id formatted as 'delete-<hobby_text>'.
        """
        driver = self.driver
        # Wait for the delete button to be clickable.
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"delete-{hobby_text}"))
        )
        self.scroll_into_view(delete_button)
        delete_button.click()
        # Wait until the element with the hobby id disappears.
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, f"span#{hobby_text}"))
        )

    def test_add_and_remove_hobbies(self):
        driver = self.driver

        # Step 1: Log in and navigate to the hobbies section.
        self.login()
        self.navigate_to_edit_profile()

        # Step 2: Test adding a single hobby.
        single_hobby = TEST_CREDENTIALS['new_hobby']  # e.g., "Cycling"
        self.add_hobby(single_hobby)

        # Assert that the span with id equal to the hobby exists and contains expected text.
        hobby_span = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"span#{single_hobby}"))
        )
        self.assertIsNotNone(hobby_span, f"Hobby span with id '{single_hobby}' was not found.")
        self.assertIn(single_hobby, hobby_span.text, f"Expected hobby '{single_hobby}' not found in span text.")

        # Step 3: Test removing the newly added hobby.
        self.remove_hobby(single_hobby)
        # Verify that the span is no longer present.
        self.assertTrue(
            WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, f"span#{single_hobby}"))),
            f"Hobby span with id '{single_hobby}' is still visible after deletion."
        )

        # Step 4: Test adding multiple hobbies.
        multiple_hobbies = TEST_CREDENTIALS['new_hobbies']  # e.g., "Swimming, Eating"
        self.add_hobby(multiple_hobbies)
        
        multiple_hobbies_split = [h.strip() for h in multiple_hobbies.split(',')]
        for hobby in multiple_hobbies_split:
            multi_hobby_span = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f"span#{hobby}"))
            )
            self.assertIn(hobby, multi_hobby_span.text)

        # Optionally remove each hobby separately.
        for hobby in multiple_hobbies_split:
            self.remove_hobby(hobby)
            # Verify that the element for that hobby is removed.
            self.assertTrue(
                WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, f"span#{hobby}"))),
                f"Hobby span with id '{hobby}' is still visible after deletion."
            )