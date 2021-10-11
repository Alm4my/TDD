# Functional Test aka Acceptance Test aka End-to-End Test
# Tracks user story. Follows how the user might work with a particular feature
# and how the app should respond to them.
# They should contain the user story
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 5

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(.5)

    def test_layout_and_styling(self):
        # Mark goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # He starts a new list and sees the input nicely centered there too
        input_box.send_keys('Testing')
        self.wait_for_row_in_list_table('1: Testing')
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Mark has heard about a cool new online to-do app. He goes to check out
        # its homepage.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        # self.fail('Finish the test!')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy a Burger" into a text box
        input_box.send_keys('Buy a Burger')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy a Burger" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a Burger')

        # There is still a text box inviting him to add another item. He
        # enters "Use Burger's ketchup to make a soup"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys("Use Burger's ketchup to make a soup")
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy a Burger')
        self.wait_for_row_in_list_table("2: Use Burger's ketchup to make a soup")

        # Mark wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect
        self.fail('Finish the Test')
        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Mark starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy rooster tail')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy rooster tail')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Make a tail hat')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Make a tail hat')

        # He notices that her list has a unique URL
        mark_list_url = self.browser.current_url
        self.assertRegex(mark_list_url, r'/lists/.+')

        # Now a new user, Jane, comes along to the site
        # ->  We use a new browser session to make sure that no information
        # ->  of Mark's is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jane visits the home page. There is no sign of Mark's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy rooster tail', page_text)
        self.assertNotIn('Make a tail hat', page_text)

        # Jane starts a new list by entering a new item
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy Milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Milk')

        # Jane gets her own unique URL
        jane_list_url = self.browser.current_url
        self.assertRegex(jane_list_url, '/lists/.+')

        # Satisfied, they both go back to sleep
