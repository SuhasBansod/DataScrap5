from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from Function import Wait
import pandas as pd
Glassurl='https://www.glassdoor.co.uk/index.htm'

if __name__ == '__main__':
    with sync_playwright() as sp :
        Mail='*****@gmail.com'
        Password= '*******'
        Browser = sp.chromium.launch(headless = False)
        page = Browser.new_page()
        page.goto(Glassurl)
        
        Wait(page)
        PageHtml=page.inner_html('body')
        Pagedata= HTMLParser(PageHtml)

        page.locator('input[id="inlineUserEmail"]').fill(Mail)
        Wait(page,5000)

        page.locator('button[data-test="email-form-button"]').click()
        Wait(page,5000)

        page.locator('input[id="inlineUserPassword"]').fill(Password)
        Wait(page,5000)
        
        page.locator('button[type="submit"]').click()
        Wait(page,5000)

        page.locator('ul[class="BIga_X94gP4PBwDEAGGZ "] > li[data-test="site-header-companies"]').click()
        Wait(page,5000)

        page.locator('div[class="d-flex flex-wrap"] > a[data-test="marketing-link-work-life"]').click()
        Wait(page,5000)

        Companylist =[]
        for n in range(1,9732):
            for i in Pagedata.css('div[class="mt-0 mb-std p-std css-mdw3bo css-errlgf"]'):
                COMName=i.css_first('h2[data-test="employer-short-name"]').text()
                Location= i.css_first('span[data-test="employer-location"]').text()
                RatingOv= i.css_first('div[class="pr-xsm employerInfo__EmployerInfoStyles__ratingSeparator"] > div > span[data-test="rating"]').text()
                Ratingworklife= i.css_first('div[class="pl-md-xsm"] > div > span[data-test="rating"]').text()
                Emplyoersize=i.css_first('span[data-test="employer-size"]').text()
                Industrywork=i.css_first('span[data-test="employer-industry"]').text()
                
                Description=i.css_first('p[class="css-1sj9xzx css-56kyx5"]')
                
                if Description:
                    Detail=Description.text()
                
                else:
                    Detail= None
                
                
                Review=i.css_first('h3[data-test="cell-Reviews-count"]').text()
                Salaries=i.css_first('h3[data-test="cell-Salaries-count"]').text()
                Jobs=i.css_first('h3[data-test="cell-Jobs-count"]').text()
                image=i.css_first('img[data-test="employer-logo"]')
                IMg={'Src': image.attrs['src'] , 'Alt': image.attrs['alt'] }
                Companylist.append({
                    'CommpanyName':COMName,
                    'Number_of_location':Location,
                    'Rating_Overall': RatingOv,
                    'Rating_worklife': Ratingworklife,
                    'Number_of_Employee': Emplyoersize,
                    'Industry_Work': Industrywork,
                    'Description': Detail,
                    'Review': Review,
                    'Salaries': Salaries,
                    'Jobs': Jobs,
                    'Image': IMg,
                })

            PageButton= page.locator(f'"button[data-test="pagination-link-{n}"]")
            
            if PageButton.is_visible():
                PageButton.click()
                Wait(page,5000)
            
            else:
                break
              
        CompData= pd.DataFrame(Companylist)            
        CompData.to_csv('GlassDOOR.csv')





        
        


