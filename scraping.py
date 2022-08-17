from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager as CDM
from config import chromeDriver
import pandas as pd
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

def scrape_all():
   data = dict()
  ## Red Planet Science
  ## Website Content Article Structure:
  ## - tag: div class="row"  :   Each article has it's own div class=row tag seperating them
  ##   - tag: div class = "list_text"        :       text side of the row, other side has an image
  ##     - tag: div class = "list_date"      :       location of article date
  ##     - tag: div class = "content_title"  :       location of article title
  ##     - tag: div class = "article_teaser_body" :  location of article summary
    url = "https://redplanetscience.com"
    browser = Browser("chrome", executable_path=chromeDriver, headless=False)    # Open an automated browser
    browser.visit(url)                                                           # Go to the first URL
    browser.is_element_present_by_css("div.list_text", wait_time=3)              # wait 3 seconds for the needed tag to appear 
    soup = bs(browser.html, "html.parser")                                       # parse the webpage to be searchable
    article = soup.find("div", attrs={"class":"row"})
    news_title = article.find('div', attrs={"class":"content_title"}).get_text()
    news_date = article.find("div", attrs={"class":"list_date"}).get_text()
    news_summary = article.find("div", attrs={"class":"article_teaser_body"}).get_text()
    post = {"title" : news_title, "date" : news_date, "summary" : news_summary}

  ## Space Images
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(3)
    browser.links.find_by_partial_text("FULL IMAGE").click()
    soup = bs(browser.html, "html.parser")
    image_url = soup.find("img", attrs={"class":"fancybox-image"}).get("src")
    new_url = url+image_url        # Save this image, it is the new one

  ## Mars Facts
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    soup = bs(browser.html, "html.parser")
    tables = pd.read_html(url)
    columns = tables[0].loc[0, :].to_list()
    columns[0] =  "Description"
    comparison_df = pd.DataFrame(tables[0].loc[1:, :])
    comparison_df.columns = columns
    comparison_df.set_index("Description", inplace=True)
    comparison_df
    stats = comparison_df.to_html()
    browser.quit()

    return data 