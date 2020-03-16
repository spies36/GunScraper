from bs4 import BeautifulSoup
import requests 
#******************************#
# Author: Dylan Spies          #
# for Aero UpperRecieve Groups #
#******************************#

def scrape_aeroURG(site,inch,q):
    page_link = site
    #grab page 
    page_response = requests.get(page_link, timeout=5)

    #parse html
    page_content = BeautifulSoup(page_response.content, "lxml")
    ##############################
    descript=[]                 ## array of full descriptions
    upper_brand=[]              ## array of upper brands
    barrel_type=[]              ## array of upper type
    split_names=[]              ## descript but split into indexable pieces
    index=0                     ## count for loop
    color=[]                    ## array of color
    stock=[]                    ## array of stock
    price=[]                    ## array of prices
    cal=[]                      ## array of caliber
    barrel_length=[]            ## array of barrel length
    link=[]                     ## array of links 
    pic_links=[]                ## array of pics 
    ##############################
    for items in page_content.find_all( 'a', attrs={'class':'product-item-link'}):  #product-item-link
        link.append(items.get('href'))
        descript.append(items.text)
        split_names=(descript[index].lower()).split()
        descript[index]=" ".join(split_names)
        #stock.append("In Stock")              
        if("5.56" in split_names):
            cal.append("5.56")
        elif(".223" in split_names):
            cal.append(".223 wylde")
        elif(".224" in split_names):
            cal.append(".224")
        elif(".300" in split_names):
            cal.append(".300")
        elif("6.5" in split_names):
            cal.append("6.5 Grendel")
        else:
            cal.append("0")
        if("cerakote" in split_names):      #only cerakote in fde
            color.append("earth")
        elif("black" in split_names):                                   #black as place holder until checked for multi
            color.append("black")
        else:
            color.append("multi")

        if((items.find( 'span', attrs={'class':'price'}))):
            price.append(price.append((items.find( 'span', attrs={'class':'price'})).text))
            stock.append("In Stock")
        else:
            price.append("None")
            stock.append("Out of Stock")

        upper_brand.append("aero")            #get brand
        barrel_length.append(inch)            #barrell in inch is passed in
        barrel_type.append("gov")
        index+=1
    for items in page_content.find_all( 'span', attrs={'class':'product-image-container'}):
        pic_links.append(items.find("img").get("data-src"))
    for items in page_content.find_all( 'div', attrs={'class':'product details product-item-details'}):
        if((items.find( 'span', attrs={'class':'price'}))!= None):
            price.append(price.append((items.find( 'span', attrs={'class':'price'})).text))
            stock.append("In Stock")
        else:
           price.append("None")
           stock.append("Out of Stock")
    i=(len(descript))-1
    while(i>(len(descript))/2):
        if(descript[i]==""):
            descript.pop(i)
            i-=1

    q.put(descript)
    q.put(barrel_length)
    q.put(barrel_type)
    q.put(price)
    q.put(cal)
    q.put(upper_brand)
    q.put(link)
    q.put(pic_links)
    q.put(color)
    q.put(stock)
