from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_login(self):
        # url = '%s' % ('http://127.0.0.1:8000/pages/about/')
        url = '%s%s' % (self.live_server_url, '/pages/about/')
        r = self.selenium.get(url)
        print("R", url, r)
        #username_input = self.selenium.find_element_by_name("username")
        #username_input.send_keys('myuser')
        #password_input = self.selenium.find_element_by_name("password")
        #password_input.send_keys('secret')
        #self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
