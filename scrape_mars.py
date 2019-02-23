# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

# Initialize browser
def init_browser(): 
    # Replace the path with your actual path to the chromedriver
    #Mac Users
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)

    #Windows Users
    executable_path = {'executable_path': 'Mission-to-Mars'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # Create a mars dictionary to be inserted into Mongo
    mars_dict = {}

    # NASA Mars News--------------------------------------------------------------------------
    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_news_url)
    # Parse the html
    mars_news_html = browser.html
    mars_news_soup = bs(mars_news_html, "html.parser")
    # Grab the latest mars news title and text
    news_title = mars_news_soup.find('div', class_='content_title').text
    news_p = mars_news_soup.find('div', class_='article_teaser_body').text
    # Append NSA Mars News to dictionary
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p

    # JPL Mars Space Images------------------------------------------------------------------
    # URL of page to be scraped
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)
    # Parse the html
    mars_image_html = browser.html
    mars_image_soup = bs(mars_image_html, "html.parser")
    # Grab the featured mars image
    featured_image = mars_image_soup.find('article')['style'].replace("background-image: url('","").replace("');","")
    # Store the main mars image url
    main_mars_image_url = "https://www.jpl.nasa.gov"
    # Combine the main + featured image urls
    featured_image_url = main_mars_image_url + featured_image
    # Append JPL Mars Space Images to dictionary
    mars_dict["featured_image_url"] = featured_image_url

    # Mars Weather-----------------------------------------------------------------------------
    # URL of page to be scraped
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    # Parse the html
    mars_weather_html = browser.html
    mars_weather_soup = bs(mars_weather_html, "html.parser")
    # Grab the latest mars weather tweet
    mars_tweet = mars_weather_soup.find_all('div', class_='js-tweet-text-container')
    # Select only the tweets with weather information
    for tweet in mars_tweet:
        mars_weather = tweet.find('p').text
        if "sol" in mars_weather:
            print(mars_weather)
            break
    # Append Mars Weather to dictionary
    mars_dict["mars_weather"] = mars_weather

    # Mars Facts---------------------------------------------------------------------------------
    # URL of page to be scraped
    mars_facts_url = "https://space-facts.com/mars/"
    # Read the html using pandas
    mars_table = pd.read_html(mars_facts_url)
    # Convert the mars table into a DataFrame 
    mars_df = mars_table[0]
    # Fix the table to make it more presentable
    mars_df.columns = ['Measurements','Records']
    mars_df.set_index('Measurements', inplace=True)
    mars_df_html = mars_df.to_html()
    # Append Mars Facts to dictionary
    mars_dict["mars_facts"] = mars_df_html

    # Mars Hemispheres---------------------------------------------------------------------------
    # URL of page to be scraped
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)
    # Parse the html
    mars_hemisphere_html = browser.html
    mars_hemisphere_soup = bs(mars_hemisphere_html, "html.parser")
    # Store the main mars hemisphere url
    main_mars_hemisphere_url = 'https://astrogeology.usgs.gov'
    # Grab the featured mars image
    hemisphere_image_urls = []
    mars_hemisphere = mars_hemisphere_soup.find_all('div', class_='item')
    for hemisphere in mars_hemisphere:    
        # Collecting the mars hemisphere titles
        mars_hemisphere_title = hemisphere.find('h3').text
        # Collect the mars hemisphere img urls
        mars_hemisphere_url = hemisphere.find('a', class_='itemLink product-item')['href']
        mars_hemisphere_full_url = main_mars_hemisphere_url + mars_hemisphere_url       
        # Visit each individual hemisphere image url
        browser.visit(mars_hemisphere_full_url)
        mars_hemisphere_img_html = browser.html
        mars_hemisphere_img_soup = bs(mars_hemisphere_img_html, 'html.parser')
        # Collect the full mars hemisphere img urls
        mars_hemisphere_part_img_url = mars_hemisphere_img_soup.find('img', class_='wide-image')['src']
        mars_hemisphere_img_url = main_mars_hemisphere_url + mars_hemisphere_part_img_url
        # Create a title + url dictionary and append to variable hemisphere image url list
        hemisphere_image_urls.append({"title":mars_hemisphere_title, "img_url":mars_hemisphere_img_url})
    # Append Mars Hemispheres to dictionary
    mars_dict["hemisphere_img_urls"] = hemisphere_image_urls

    # Return Mars results---------------------------------------------------------------------------------------
    # Close browser after scraping
    browser.quit()
    # Return results
    return mars_dict
