from bs4 import BeautifulSoup
import requests 
#******************************#
# Author: Dylan Spies          #
# for BCM Upper Recieve Groups #
#******************************#

def scrape_bcmURG(site,q):
    page_link = site
    #grab page 
    page_response = requests.get(page_link, timeout=5)

    #parse html
    page_content = BeautifulSoup(page_response.content, "lxml")
    ##############################
    descript=[]                 ## array of full descriptions
    brand=[]                    ## array of brands
    barrel_len=[]               ## array of barrel len
    barrel_type=[]              ## array of barrel type
    split_names=[]              ## descript but split into indexable pieces
    index=0                     ## count for loop
    handguard_len=[]            ## array of handguard length 
    stock=[]                    ## array of stock
    price=[]                    ## array of prices
    cal=[]                      ## array of caliber
    color=[]                    ## array of color
    links=[]                    ## array of links
    pic_links=[]                ## array of pic links
    ##############################
    for items in page_content.find_all( 'a', attrs={'class':'v-product__img'}):
        pic_links.append(items.find("img").get("src"))
    for items in page_content.find_all( 'a', attrs={'class':'v-product__title productnamecolor colors_productname'}):
        descript.append(items.text)
        split_names=descript[index].split()
        descript[index]=" ".join(split_names)
        barrel_type.append(split_names[1])
        if(split_names[2].lower()=="spec"):
            barrel_len.append('16"')
        else:
            barrel_len.append(split_names[2])
        if "300" in descript[index]:
            cal.append(".300")
        else:
            cal.append("5.56")
        brand.append("BCM")
        index+=1
        color.append("black")
    for items in page_content.find_all( 'a', attrs={'class':'v-product__title productnamecolor colors_productname'}):
        links.append(items.get('href'))
    for items in page_content.find_all( 'span', attrs={'class':'stock-label'}):
        stock.append((items.text).replace("(","").replace(")",""))
    for items in page_content.find_all( 'div', attrs={'class':'product_productprice'}):
        split_names=((items.text).split())
        price.append(split_names[2])
    q.put(descript)
    q.put(barrel_len)
    q.put(barrel_type)
    q.put(price)
    q.put(cal)
    q.put(brand)
    q.put(links)
    q.put(pic_links)
    q.put(color)
    q.put(stock)
