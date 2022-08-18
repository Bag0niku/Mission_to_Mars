from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager as CDM
from config import chromeDriver
import pandas as pd
import datetime as dt
import time

### Red Planet Science
   ## - URL: https://redplanetscience.com/
   ## - Pull recent news stories about Mars
### Space Images
  ## - URL https://spaceimages-mars.com/
  ## - Pull recent images of Mars
### Mars Facts
  ## - URL:  https://galaxyfacts-mars.com/
  ## - Pull statistical information for the web app

def mars_news(browser):
    ## Red Planet Science
    ## Website Content Article Structure:  (incase of future change)
    ## - tag: div class="row"  :   Each article has it's own div class=row tag seperating them
    ##   - tag: div class = "list_text"        :       text side of the row, other side has an image
    ##     - tag: div class = "list_date"      :       location of article date
    ##     - tag: div class = "content_title"  :       location of article title
    ##     - tag: div class = "article_teaser_body" :  location of article summary
    url = "https://redplanetscience.com"    
    browser.visit(url)                                                           # Open an automated browser and visit the url
    browser.is_element_present_by_css("div.list_text", wait_time=1)              # wait 3 seconds for the needed tag to appear 
    soup = bs(browser.html, "html.parser")                                       # parse the webpage to be searchable
    try:
      article = soup.find("div", attrs={"class":"row"})
      news_title = article.find('div', attrs={"class":"content_title"}).get_text()
      news_date = article.find("div", attrs={"class":"list_date"}).get_text()
      news_summary = article.find("div", attrs={"class":"article_teaser_body"}).get_text()
      post = {"news_title" : news_title, "date" : news_date, "news_summary" : news_summary}
      return post
    except AttributeError:
      return None
    except Exception as e:
      print(e) 
      raise f"Browser Error : {e}"
    

def mars_images(browser):
    ## Space Images
    url = "https://spaceimages-mars.com/"
    browser.visit(url)                    
    browser.is_element_present_by_text("FULL IMAGE", wait_time=1)                
    browser.links.find_by_partial_text("FULL IMAGE").click()
    soup = bs(browser.html, "html.parser")
    try:
      image_url = soup.find("img", attrs={"class":"fancybox-image"}).get("src")
      new_url = url+image_url        # Save this image, it is the new one
      return new_url
    except AttributeError:
      return None
    except Exception as e:
      print(e)  
      raise f"Browser Error : {e}"


def mars_facts():
    ## Mars Facts
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    try: 
      columns =  ["Description", "Information"]
      comparison_df = pd.DataFrame(tables[1])
      comparison_df.columns = columns
    #   comparison_df.set_index("Description", inplace=True)
    #   comparison_df.rename_axis(None, axis=0, inplace=True)
      stats = comparison_df.to_html(index=False)
      return stats
    except AttributeError:
      return None
    except Exception as e:
      print(e)
      raise f"Import Error: {e}"

def mars_hemispheres(browser):
    url = "https://astrogeology.usgs.gov" 
    search = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url+search)
    time.sleep(1)
    soup = bs(browser.html, "html.parser")
    div = soup.find_all('div', attrs={"class":"item"})
    ## sm_img = [item.find("a", attrs={"class":"thumb"}).get("href")  for item in div]
    face = [item.find("h3").find_parent().get("href") for item in div]
    mars_imgs = list()
    for item in face:
        d = dict()
        browser.visit(url+item)
        browser.is_element_present_by_text("OPEN", wait_time=1)
        soup = bs(browser.html, "html.parser")
        div = soup.find("div", attrs={"class":"downloads"})
        img = div.find_all("a")
        div = soup.find("div", attrs={"class":"content"})
        d["title"] = div.find("h2", attrs={"class":"title"}).text
        d["lg_hemisphere_img"] = img[1].get("href")  # 21 MB .tif file, not website friendly
        d["sm_hemisphere_img"] = img[0].get("href")  # large .jpg,  website friendly

        mars_imgs.append(d)
    return mars_imgs



def scrape_all():
    browser = Browser("chrome", executable_path=chromeDriver, headless=True)
    news = mars_news(browser)
    news['featured_image'] = mars_images(browser)
    news['facts'] = mars_facts()
    news['last_modified'] = dt.datetime.now()
    news["hemispheres"] = mars_hemispheres(browser)
    browser.quit()
    return news



if __name__ == "__main__":
    print(scrape_all())
