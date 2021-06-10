from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask import Flask, render_template, redirect
import requests
from flask_pymongo import PyMongo

def init_browser(): 
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape(): 
    browser = init_browser()
    img_dict {}

    # URL of page to be scraped
    NASA_url = 'https://redplanetscience.com/'
    browser.visit(NASA_url)
    NASA_html = browser.html
    NASA_soup = bs(NASA_html, 'html.parser')

    # Retrieving and assigning latest news title
    news_title = NASA_soup.body.find_all('div', class_='content_title')[0].text

    # Retrieving and assigning latest news paragraph
    news_p = NASA_soup.body.find_all('div', class_='article_teaser_body')[0].text

    # Featured Mars image to be scraped
    jpl_space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_space_image_url)
    html = browser.html
    soup_image = bs(html, 'html.parser')

    # Retrieving the link of the feature image
    image_url = soup_image.find_all('img')[1]["src"]
    featured_image_url = jpl_space_image_url + image_url

    # Scraping Mars Facts
    url_mars_facts = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_mars_facts)
    mars_table_df = tables[0]
    # Creating the column names for the Mars table
    mars_table_df.columns = ["Description", "Mars", "Earth"]
    # Getting rid of the index numbers
    mars_table_df.set_index("Description", inplace=True)
    html_table_mars_facts = mars_table_df.to_html()
    html_table_mars_facts.replace('\n', '')

    # Scraping images of Mars hemispheres\
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    mars_hemispheres_html = browser.html
    mars_hemispheres_soup = bs(mars_hemispheres_html, 'html.parser')

    # Extracting the hemisphere elements
    mars_hemispheres_items = mars_hemispheres_soup.find_all('div', class_='item')

    # Creating an empty list
    hemispheres_url_image = []

    # Looping through each hemipshere item result for the title and image url
    for mars in mars_hemispheres_items:
    
        # Retrieving the title
        hem_descript = mars.find('div', class_="description")
        title = hem_descript.h3.text
    
        # Retrieving the hemispheres images 
        hem_image = mars.find('a', class_='itemLink product-item')['href']
    
        # Visiting the link with high resolution image
        browser.visit(hemispheres_url+hem_image)
    
        #HTML Object
        url_mars_image_html = browser.html
        url_mars_image_soup = bs(url_mars_image_html, 'html.parser')
    
        #Full image url
        img_url = hemispheres_url + url_mars_image_soup.find('img', class_='wide-image')['src']
    
        #Creating a dictionary
        img_dict = {
            'img_url':img_url,
            'title': title
        }
    
        #Append the dictionary with the image url string and the hemisphere title to a list
        hemispheres_url_image.append(img_dict)

        # Closing browser after scraping
        browser.quit()

        return img_dict

  


