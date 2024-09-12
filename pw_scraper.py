from playwright.sync_api import sync_playwright, Playwright
import time
import pandas as pd


data_list= []
for i in range(1,3):
    start_url = f'https://www.bhphotovideo.com/c/buy/rebates-promotions/N/4019732813/ci/22144/Photography/ci/989/N/4294538916/pn/{i}'
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    # page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
    page.goto(start_url)
    time.sleep(1)

    if i:
        for link in page.locator('a[data-selenium="miniProductPageDetailsGridViewNameLink"]').all()[:2]:
            p = browser.new_page(base_url="https://www.bhphotovideo.com/")
            # p.route("**/*.{png,jpg,jpeg}",lambda route: route.abort())
            url = link.get_attribute('href')
            if url is not None:
                p.goto(url)
                time.sleep(.5)
            else:
                p.close()
                
            # name = p.locator('h1[data-selenium="productTitle"]').text_content() 
            # name = p.query_selector('h1[data-selenium="productTitle"]').text_content()
            name = p.query_selector('//h1[@data-selenium="productTitle"]').text_content() #using xpath
            price = p.locator('div[data-selenium="pricingPrice"]').text_content()
            reviews= p.locator('span[data-selenium="reviewsNumber"]').text_content().split(' ')[0]
            features = p.locator('ul[class="list_OMS5rN7R1Z"]').text_content()
            print(f'page no. {i}')
            print(name)
            print(price)
            print(reviews) 
            print(features)
            data_list.append([name, price,reviews, features])
            # p.close()
    page.close()
    browser.close()
    pw.stop()  
df = pd.DataFrame(data_list, columns=["Name", "Price","reviews", "Features"])

print(df)
df.to_excel("data2.xlsx",index=False) 
df.to_csv("data2.xlsx",index=False)  
 
           
    
