from bs4 import BeautifulSoup
import requests 
#******************************#
# Author: Dylan Spies          #
# for Ballistic Advantage      #
#******************************#
def scrape_ball(site,q):
    page_link = site
    #grab page 
    page_response = requests.get(page_link, timeout=5)

    #parse html
    page_content = BeautifulSoup(page_response.content, "lxml")
##############################
    barrels=[]              ## array of full descriptions
    cal=[]                  ## array of caliber
    split_names=[]          ## barrels but split into indexable pieces
    index=0                 ## count for loop
    length=[]               ## array of barrel length 
    price=[]                ## array of prices
    stock=[]                ## array of availability
    link=[]                 ## array of links
    pic_link=[]             ## array of pics
##############################

    for items in page_content.find_all('a',attrs={'class':'product-image'}):
        link.append(items.get('href'))
        pic_link.append(items.find("img").get("src"))
    for items in page_content.find_all('h2'):       #where they store items
        barrels.append(items.text)
        split_names=barrels[index].split()          #split titles so we can index them, in example, first part =[0], second =[1]...etc
        length.append(split_names[0])               #length in inches
        index+=1
        if(split_names[1]==".223"):                 #check for variation of .223
            if(split_names[2].lower()=="wylde"):    
                cal.append(".223 wylde")
            else:
                cal.append(split_names[1])
        else:                                       #if not a .223 type just put cal, (300blk) just shows up as 300 right now
            cal.append(split_names[1])
    for items in page_content.find_all( 'span', attrs={'class':'price'}):       #grab price
        split_names=((items.text).split())
        split_names="".join(split_names)            #format the price
        price.append(split_names)
    for items in page_content.find_all( 'div', attrs={'class':'actions clearer'}):  #grab the section where they store "add to cart" and "out of stock"
        split_names=(items.text).split()
        if "Out" not in split_names:                #if it doesnt say out of  stock, mark as in
            stock.append('In stock')
        else:                                       #mark as out of stock
            stock.append('Out of stock')
##############################
    del length[-1]          ## remove last piece of list
    del barrels[-1]         ##
                            ##
##############################
    q.put(length)
    q.put(cal)
    q.put(price)
    q.put(stock)
    q.put(link)
    q.put(pic_link)
