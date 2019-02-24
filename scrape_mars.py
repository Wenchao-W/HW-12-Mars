# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/WenchaoWang/Downloads/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def news():
    executable_path = {"executable_path": "C:/Users/WenchaoWang/Downloads/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    browser.visit(url)
    time.sleep(2)
    response = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')

    # Get the title and paragraphy
    news_title = soup.find(class_="content_title").text
    news_p=soup.find(class_="rollover_description_inner").text
    news={'title':news_title,'p':news_p}
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return news

def img():
    executable_path = {"executable_path": "C:/Users/WenchaoWang/Downloads/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html=browser.html
    soup2 = BeautifulSoup(html, 'html.parser')

    # Get the featured image link
    link=soup2.find(class_="carousel_item").get("style")
    featured_image_url ='https://www.jpl.nasa.gov'+link[23:][:-3]
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return featured_image_url

def weather():
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
   
    # Retrieve page with the requests module
    response = requests.get(url)
   
    # Create BeautifulSoup object; parse with 'html.parser'
    soup3 = BeautifulSoup(response.text, 'html.parser')

    # Get the mars weather
    weathertext=soup3.find(class_="content").p.text
    mars_weather=weathertext.split('\n')[0]
    
    # Return results
    return mars_weather

def fact():
    # URL of page to be scraped
    url = 'http://space-facts.com/mars/'
    
    # Scrape by pandas
    tables = pd.read_html(url)  
   
    # Get the mars fact
    df=tables[0]
    df.columns = ['Description', 'Data']
    mars_facts=df.set_index('Description')
    html_table = mars_facts.to_html()
    # Return results
    return html_table

def hemispheres():
    executable_path = {"executable_path": "C:/Users/WenchaoWang/Downloads/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html=browser.html
    soup4 = BeautifulSoup(html, 'html.parser')

    # Get the all hemispheres titles
    hem_titles=soup4.find_all('h3')

    # Click into further pages for the image link
    furtherurl=[]
    soup4.find_all(class_="item")[0].a.get('href')
    items=soup4.find_all(class_="item")
    for item in items:
        furtherurl.append('https://astrogeology.usgs.gov'+item.a.get('href'))
    
    # Get the hemispheres image links
    img_urls=[]
    for link in furtherurl:
        browser.visit(link)
        html2=browser.html
        soup5 = BeautifulSoup(html2, 'html.parser')
        img_urls.append(soup5.find(class_="downloads").li.a.get('href'))
    
    # Save hemispheres titles and links into a list of dictionaries 
    hemisphere_image_urls=[]
    for i in range(4):
        hemisphere_image_urls.append({"title": hem_titles[i].text, "img_url": img_urls[i]})
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return hemisphere_image_urls