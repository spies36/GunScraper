from bs4 import BeautifulSoup
import requests 
#******************************#
# Author: Dylan Spies          #
# for BCM Upper Reciever       #
#******************************#

def scrape_bcmUpper(site,q):
    page_link = site
    #grab page 
    page_response = requests.get(page_link, timeout=5)

    #parse html
    page_content = BeautifulSoup(page_response.content, "lxml")
    ##############################
    descript=[]                 ## array of full descriptions
    upper_brand=[]              ## array of upper_type
    split_names=[]              ## descript but split into indexable pieces
    index=0                     ## count for loop
    upper_bleme=[]              ## array of handguard length 
    stock=[]                    ## array of stock
    items_grabbed=[]            ## which items were used by number in loop
    final_descrip=[]            ## array of only used items    
    price=[]                    ## array of prices
    color=[]                    ## array of color
    ##############################
    for items in page_content.find_all( 'a', attrs={'class':'v-product__title productnamecolor colors_productname'}):
        descript.append(items.text)                         #grabs only the text items not html               
        split_names=descript[index].split()                 #split up the data so you can reference it by index: first item[0], second item[1]....
        descript[index]=" ".join(split_names)               #cleans up description
        if(split_names[1].lower()=="m4" or split_names[1].lower()=="upper"): #make sure its an upper
            upper_brand.append(split_names[0])              #grab the brand 
            items_grabbed.append(index)                     #whcih items (by index) were actually used
            index+=1                                  
            final_descrip.append(" ".join(split_names))     #description only of items used
            if(split_names[-1].lower()=="demo/scratched"):  #if blemished
                upper_bleme.append(1)                       #true
            else:
                upper_bleme.append(0)                       #if blemished false
        color.append("black")
    count=0 
    for items in page_content.find_all( 'span', attrs={'class':'stock-label'}):
        if(count in items_grabbed):                                         #if that number is in the used item array
            stock.append((items.text).replace("(","").replace(")",""))
        count+=1

    for items in page_content.find_all( 'div', attrs={'class':'product_productprice'}):
        split_names=((items.text).split())
        price.append(split_names[2])
    q.put(final_descrip)
    q.put(upper_brand)
    q.put(upper_bleme)
    q.put(stock)
    q.put(price)
    q.put(color)
