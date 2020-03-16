from bs4 import BeautifulSoup
import requests 
#******************************#
# Author: Dylan Spies          #
# for BCM Lower Recieve Groups #
#******************************#

def scrape_bcmLower(site,q):
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
    stock_holder=[]             ## hold stock to change
    link=[]                     ## array of links
    pic_links=[]                ## array of pics
    ##############################
    for items in page_content.find_all( 'a', attrs={'class':'v-product__img'}):
        link.append(items.get('href'))
        pic_links.append(items.find("img").get("src"))
    for items in page_content.find_all( 'a', attrs={'class':'v-product__title productnamecolor colors_productname'}):
        descript.append(items.text)
        split_names=(descript[index].lower()).split()
        descript[index]=" ".join(split_names)
        lower_brand.append(split_names[0])      #get brand
        if "6-position" in split_names:         #rifle w/o included stock
            lower_type.append('rifle')
            butt_stock.append("none")
        elif "pistol" in split_names:           #pistol
            if "brace" in split_names:          #w/ brace
                lower_type.append("pistol")
                butt_stock.append("brace")
            else:                               #no brace
                lower_type.append("pistol")
                butt_stock.append("none")
        else:                                   #riflee with a buttstock
            lower_type.append("rifle")          
            butt_stock.append("included")
        cal.append("5.56")
        color.append((split_names[-1]).replace(")","").replace("(",""))     #grab the color and take out ()
        index+=1
    for items in page_content.find_all( 'b'):                               #grab all b items on the page
        stock_holder.append((items.text).replace("(","").replace(")",""))   #take out ()
    for items in page_content.find_all( 'div', attrs={'class':'product_productprice'}): #grab prices
        split_names=((items.text).split())
        price.append(split_names[2])
    stock_holder.pop(0)                     #filtering out the title and other b items not needed
    stock_holder.pop(0)
    stock_holder.pop(0)
    stock_holder.pop(0)
    stock_holder.pop(0)
    for items in stock_holder:
        if "Our" not in items:              #grab things that are not "Our Price"
            split_names=items.split()
            split_names="".join(split_names)    #fix format
            stock.append(split_names)
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
    