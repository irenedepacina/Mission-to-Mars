#!/usr/bin/env python
# coding: utf-8

# In[49]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd


# In[50]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[51]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[52]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[53]:


slide_elem.find("div", class_='content_title')


# In[54]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[55]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[56]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[57]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[58]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[59]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[60]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[61]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[62]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[63]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[64]:


df.to_html()


# ### Mars Weather

# In[65]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[66]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[67]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[68]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[69]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
base_url = 'https://astrogeology.usgs.gov'

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemispheres_soup = soup(html, 'html.parser')

# Find all divs with class item then find all div with class description. 
# Find the div with class downloads, retrieve the a and its href attribute for full link of the image.
# Build a dictionary and append the item to the list
for hemispheres_url in hemispheres_soup.find_all('div', class_='item'):
    for image in hemispheres_url.find_all('div', class_='description'):
        image_url = image.find('a').get('href')
        image_Name = image.find('h3').get_text()
        
        image_url_rel = base_url + image_url
        
        browser.visit(image_url_rel)
        
        # Parse the resulting html with soup
        html = browser.html
        image_soup = soup(html, 'html.parser')
        downloads = image_soup.find('div', class_='downloads')
        hyperLink = downloads.find('a').get('href')
        
        hemispheres = {'img_url': hyperLink,
                 'title': image_Name}
        hemisphere_image_urls.append(hemispheres)
        browser.back()


# In[70]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[71]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




