from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import urllib.request
from urllib.request import urlopen

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit Mars Nasa website
    url_nasa_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest/"
    browser.visit(url_nasa_news)

    time.sleep(1)

    # Scrape page into Soup
    html_nasa = browser.html
    soup_nasa = bs(html_nasa, "html.parser")

    # Geting headline
    news_full = soup_nasa.select("#page a")

    news_title = [x.text for x in news_full][1]

    # Getting paragraph
    news_t = soup_nasa.select(".article_teaser_body")

    news_paragraph = [x.text for x in news_t][0]

    
    # Close the browser after scraping
    browser.quit()

    # Visit JPL Nasa Website
    browser = init_browser()

    url_jpl_original = "https://www.jpl.nasa.gov"

    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url_jpl)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    relative_image_path = soup.select('.thumb')[0]["src"]

    nasa_img = url_jpl_original + relative_image_path

    urllib.request.urlretrieve(nasa_img, "images/Mars_image.jpg")

    # Close the browser after scraping
    browser.quit()

    # Visit Twitter Mars Page Website
    browser = init_browser()

    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    time.sleep(1)

    # Scrape page into Soup
    html_twitter = browser.html
    soup_twitter = bs(html_twitter, "html.parser")

    # Geting last tweet
    tweet = soup_twitter.select(".tweet-text")

    last_tweet = [x.text for x in tweet][0]

    # Close the browser after scraping
    browser.quit()

    browser = init_browser()

    url_facts = 'https://space-facts.com/mars/'
    page_facts = urlopen(url_facts)
    soup_facts = bs(page_facts, 'html.parser')
    
    table = soup_facts.find('table',id="tablepress-mars")

    final_table = "{table}"

    # Close the browser after scraping
    browser.quit()

    # Visit Hemisphere Page Website
    browser = init_browser()

    url_hemisphere_original = "https://astrogeology.usgs.gov"

    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    time.sleep(1)

    hemisphere_names  = []
    hemisphere_images = []

    for i in [0,1,2,3]:
        # Scrape page into Soup
        html_hemisphere = browser.html
        soup = bs(html_hemisphere, "html.parser")
        
        # For loop for the name of the Hemispheres and appending to list
        hemis_name = soup.select("h3")
        hemis_string = [x.text for x in hemis_name][i]
        hemisphere_names.append(hemis_string)
        
        # For loop for theimages of the Hemispheres and appending to list
        image_path_hemisphere = soup.select('.thumb')[i]["src"]    
        hemisphere_img = url_hemisphere_original + image_path_hemisphere
        hemisphere_images.append(hemisphere_img)
        
        # Savings images in folder
        urllib.request.urlretrieve(hemisphere_img, f"images/hemisphere{i}_img.jpg")


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "nasa_img": nasa_img,
        "last_tweet": last_tweet,
        "final_table": final_table,
        "hemisphere_name1": hemisphere_names[0],
        "hemisphere_name2": hemisphere_names[1],
        "hemisphere_name3": hemisphere_names[2],
        "hemisphere_name4": hemisphere_names[3],
        "hemisphere_image1": hemisphere_images[0],
        "hemisphere_image2": hemisphere_images[1],
        "hemisphere_image3": hemisphere_images[2],
        "hemisphere_image4": hemisphere_images[3]
    }


    
    # Return results
    return mars_data
