# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data   

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try and except to catch errors
    try:    
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    # JPL Space Images Featured Image

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try and except to catch errors
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url 

def mars_facts():
    # Add try and except to catch errors
    try:
        # Use 'read_html' to scrape the facts table into a DataFrame   
    df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Create columns and set index to DataFrame
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert DataFrame into HTML format and add Bootstrap
    return df.to_html()

def hemisphere_data(browser):

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

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
            try:
                image_url = item.find('a').get('href')
                image_Name = item.find('h3').get_text()
                
                image_url_rel = base_url + image_url
                
                browser.visit(image_url_rel)
                
                # Parse the resulting html with soup
                html = browser.html
                image_soup = soup(htmln, 'html.parser')
                downloads = full_soup.find('div', class_='downloads')
                hyperLink = downloads.find('a').get('href')
                
                hemispheres = {'img_url': hyperLink,
                        'title': tmpName}
                hemisphere_image_urls.append(hemispheres)
            
            except AttributeError:
                return None

        # 4. Print the list that holds the dictionary of each image url and title.
        return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())