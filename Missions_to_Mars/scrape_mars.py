#!/usr/bin/env python
# coding: utf-8

# In[1]:


#dependencies
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pymongo


# ### NASA Mars News
# ##### Scrape the [Mars News Site](https://redplanetscience.com/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[2]:

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


    url = 'https://redplanetscience.com/'
    browser.visit(url)


# In[4]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find('div', class_='list_text')

    article_content = []

    article_title = article.find('div', class_='content_title').text
    print(f'Title: {article_title}')
    teaser_text = article.find('div', class_='article_teaser_body').text
    print(f'Text: {teaser_text}\n')
    content = dict({'Title':article_title, 'Text':teaser_text})
    article_content.append(content)


# ### JPL Mars Space Images - Featured Image
# ##### Visit the url for the Featured Space Image site [here](https://spaceimages-mars.com).
# 
# ##### Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# 
# ##### Make sure to find the image url to the full size `.jpg` image.
# 
# ##### Make sure to save a complete url string for this image.

# In[5]:


    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


# In[6]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_source = soup.find('img', class_='fade-in').get('src')
    img_url = url + img_source
    print(img_url)


# ### Mars Facts
# 
# ##### Visit the Mars Facts webpage [here](https://galaxyfacts-mars.com) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# ##### Use Pandas to convert the data to a HTML table string.

# In[7]:


    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)


# In[8]:


    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[1]
    mars_facts = mars_facts_df.to_html()


# ### Mars Hemispheres
# 
# ##### Visit the astrogeology site [here](https://marshemispheres.com/) to obtain high resolution images for each of Mar's hemispheres.
# 
# ##### You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# ##### Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# 
# ##### Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[9]:


    url = 'https://marshemispheres.com/'
    browser.visit(url)


# In[10]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    image_url_list = []
    title_list = []

    for item in items:
        img_title = item.find('h3').text
        print(img_title)
        item_url = url + item.find('a')['href']

        browser.visit(item_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        img_url = url + soup.find('img', class_='wide-image').get('src')
        print(img_url)

        url_insert = dict({'URL':img_url})
        image_url_list.append(url_insert)
        title_insert = dict({'Title':img_title})
        title_list.append(title_insert)

    mars_data = {
        'article_title': article_content[0]['Title'],
        'article_text': article_content[0]['Text'],
        'image': img_url,
        'facts': mars_facts,
        'hemisphere_urls': image_url_list,
        'hemisphere_title': title_list
    }
    
    browser.quit()
    
    return mars_data