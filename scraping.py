#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data
# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': 'chromedriver'}
# browser = Browser('chrome', **executable_path)

# ## Visit the mars nasa news site
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # ## Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # ### Get only text from content title
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # ## Scraping for the summary
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None
    return news_title, news_p
# ## Featured Images
# ### Set up URL for space image
# Visit URL
def featured_image(browser):
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)

    # ### Find and click the full image button
    full_image_elem = browser.find_by_id('wide-image-toggle')[0]
    full_image_elem.click()

    # ### Find the more info button and click that
    #browser.is_element_present_by_text('more info', wait_time=1)
    #more_info_elem = browser.links.find_by_partial_text('more info')
    #more_info_elem.click()

    # ### Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # ### Find the relative image url
        img_url_rel = img_soup.select_one('figure.wide-image a img').get("src")
    except AttributeError:
        return None    

    # ### Add the base URL to code
    # Use the base URL to create an absolute URL
    img_url = f'https://astrogeology.usgs.gov{img_url_rel}'
    return img_url

# ## Scrape Mars Data: Mars Facts
# ### Scraping whole table of Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


