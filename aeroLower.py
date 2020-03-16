from bs4 import BeautifulSoup
import requests 
#******************************#
# Author: Dylan Spies          #
# for Aero LowerRecieve Groups #
#******************************#

def scrape_aeroLower(site,q):
    page_link = site
    #grab page 
    page_response = requests.get(page_link, timeout=5)

    #parse html
    page_content = BeautifulSoup(page_response.content, "lxml")
    ##############################
    descript=[]                 ## array of full descriptions
    lower_brand=[]              ## array of lower brands
    lower_type=[]               ## array of lower type
    split_names=[]              ## descript but split into indexable pieces
    index=0                     ## count for loop
    color=[]                    ## array of color
    stock=[]                    ## array of stock
    butt_stock=[]               ## array of butt stocks
    price=[]                    ## array of prices
    cal=[]                      ## array of caliber
    link=[]                     ## array of links
    pic_links=[]                ## array of links
    ##############################
    for items in page_content.find_all( 'a', attrs={'class':'product-item-link'}):
        link.append(items.get('href'))
        descript.append(items.text)
        split_names=(descript[index].lower()).split()
        descript[index]=" ".join(split_names)
        lower_brand.append("aero")      #get brand
        if "featureless" in split_names:         #rifle w/o included stock
            lower_type.append('CA')
            butt_stock.append("fixed")
        elif "pistol" in split_names:           #pistol
            if "brace" in split_names:          #w/ brace
                lower_type.append("pistol")
                butt_stock.append("brace")
            else:                               #no brace
                lower_type.append("pistol")
                butt_stock.append("none")
        else:                                   #rifle 
            if("no stock") in descript[index]:
                lower_type.append("rifle")
                butt_stock.append("none")       #no stock
            else:
                lower_type.append("rifle")          
                butt_stock.append("included")   #stock included
        if("cerakote" in split_names):      #only cerakote in fde
            color.append("earth")
        elif("black" in split_names):                                   #black as place holder until checked for multi
            color.append("black")
        else:
            color.append("multi")
        index+=1
        stock.append("In Stock")                #all items on page are in stock
        cal.append("5.56")                      # all items on page are 5.56
    for items in page_content.find_all( 'span', attrs={'class':'product-image-container'}):
        pic_links.append(items.find("img").get("data-src"))
    for items in page_content.find_all( 'span', attrs={'class':'price'}): #grab prices
        split_names=((items.text).split())
        price.append(split_names[0])
    q.put(descript)
    q.put(lower_brand)
    q.put(lower_type)
    q.put(color)
    q.put(stock)
    q.put(butt_stock)
    #q.put(cal)
    q.put(price)
    q.put(link)
    q.put(pic_links)
