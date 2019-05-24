#Web Scrape Homework: 
# Marie Wothe

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests


#function to search the browser
def init_browser():
    executable_path = {"executable_path" : "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    html = browser.html

#visit the url for the news
    url = "https://mars.nasa.gov/news/"

#Retrieve the page with the requests and then use Soup to parse on 'lxml'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    #News paragraph
    news_p = soup.find(class_= 'rollover_description_inner').text
    #News Title
    news_title = soup.find(class_= 'content_title').text

    #Make it pause
    time.sleep(1)

    #Collect the image
    img_url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #get the image. 
    image_resp = requests.get(img_url)
    image_soup = bs(image_resp.text, 'lxml')
    image = image_soup.find('li', class_ = 'slide')
    featured_img_url = "https://www.jpl.nasa.gov" + image.a['data-fancybox-href']

    #Make it pause
    time.sleep(1)

    #Scrape a table of facts from the spacefacts website
    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)
    facts_df = tables[0]
    facts_df.columns = ["Feature", "Description"]
    html_table = facts_df.to_html()

    #Hemisphere pictures. 

    #visit the site using splinter for the hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #list of hemi names
    h_list = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    #List for Hemi urls
    hemisphere_img_urls = []

    #open browser
    browser.visit(hemi_url)

    #for loop to grab the hemisphere stuff
    for hemi in h_list:
        browser.click_link_by_partial_text(hemi)
        h_html = browser.html
        hemi_soup = bs(h_html, 'html.parser')
        url = hemi_soup.find('div', class_='downloads').ul.li.a['href']
        name = hemi_soup.title.text.partition(' Enhanced')[0]
        hemisphere_img_urls.append({'title':name, "img_url": url})
        browser.back() 

    time.sleep(1)

    #store the scraped info into a dictionary
    mars_variables = {
        "News_title": news_title,
        "News_paragraph": news_p,
        "JPL_featured_img": featured_img_url,
        "mars_facts": html_table,
        "Cerberus": hemisphere_img_urls[0]["img_url"],
        "Schiaparelli": hemisphere_img_urls[1]["img_url"],
        "Syrtis_Major": hemisphere_img_urls[2]["img_url"],
        "Valles_Marineris": hemisphere_img_urls[3]["img_url"]
        }

    #close the browser
    browser.quit()

    return mars_variables

if __name__ == "__main__":
    scrape()