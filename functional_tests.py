# Functional Test aka Acceptance Test aka End-to-End Test
# Tracks user story. Follows how the user might work with a particular feature
# and how the app should respond to them.
# They should contain the user story
import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Mark has heard about a cool new online to-do app. He goes to check out
        # its homepage.
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        # self.fail('Finish the test!')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # he is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # he types "Buy a Burger" into a text box
        input_box.send_keys('Buy a Burger')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy a Burger" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)       # Explicit wait to make sure the browser has finish loading

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy a Burger' for row in rows),
            "New to-do item did not appear in table"
        )

        # There is still a text box inviting him to add another item. He
        # enters "Use Burger's ketchup to make a soup"
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on his list

        # Mark wonders whether the site will remember his list. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect

        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
