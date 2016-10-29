from selenium import webdriver
import _data

def before_all(context):
    context.browser = webdriver.Firefox()

def after_all(context):
    context.browser.quit()


def before_scenario(context, scenario):
    _data.create()

