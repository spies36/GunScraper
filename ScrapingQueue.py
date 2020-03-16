from ballisticScrape import *
from bcmURG import *
from bcmUpper import *
from bcmLower import *
from aeroLower import *
from aeroURG import *
from SQLSubmit import *
import multiprocessing as mp
from multiprocessing import Process, Queue
import time


MakeRoom()

if __name__=='__main__':

    #****************************#
    #  LIST FOR SITES TO SCRAPE  #
    ballistic=['https://ballisticadvantage.com/ar15-barrels?barrel_muzzle=58&limit=all','https://ballisticadvantage.com/ar15-barrels?barrel_muzzle=59&limit=all','https://ballisticadvantage.com/ar15-barrels?barrel_muzzle=89&limit=all']
    bcmURG=['https://www.bravocompanyusa.com/BCM-Upper-Receiver-Groups-with-BFH-Barrels-s/128.htm,','https://www.bravocompanyusa.com/BCM-Upper-Receiver-Groups-with-Standard-Barrels-s/126.htm','https://www.bravocompanyusa.com/BCM-Upper-Receiver-Groups-with-SS410-Barrels-s/127.htm']
    bcmUpper=['https://www.bravocompanyusa.com/AR-15-Upper-Receiver-s/33.htm']
    bcmLower=['http://shop.bravocompanymfg.com/BravoCompanyMFG-BCM-AR15-M4-Lower-Receiver-Group-s/120.htm']
    #aeroLower=['https://www.aeroprecisionusa.com/ar15/lower-receivers/complete-lowers?product_list_limit=all']
    #aeroURG=['https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=35&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=39&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=40&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=36&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=31&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=32&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=37&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=126&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=34&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=33&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=38&product_list_limit=all','https://www.aeroprecisionusa.com/ar15/upper-receivers/complete-uppers?barrel_length=140&product_list_limit=all']
    #sizes=['7.5"','8"','10"','10.5"','11.5"','12.5"','14.5"','14.7"','16"','18"','20"','22"']
    

    #****************************#
    q=Queue()           #work queue
    start= time.time()  #timer for testing
    #****************************#
    for pages in ballistic:
        p=Process(target=scrape_ball, args=(pages,q))
        p.start()
    for items in ballistic:  
        print(q.get())     #barrel length
        print(q.get())     #caliber
        print(q.get())     #price
        print(q.get())     #stock
        print(q.get())     #links
        print(q.get())     #pic links
    #****************************#
    for pages in bcmURG:   #BCM Upper Reciever Group Scrape
        p=Process(target=scrape_bcmURG, args=(pages,q))
        p.start()
    for items in bcmURG:
        submitURG(q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get())
    #****************************#
    for pages in bcmUpper:   #BCM Upper Reciever Scrape
        p=Process(target=scrape_bcmUpper, args=(pages,q))
        p.start()
    for items in bcmUpper:
        print(q.get())       #description
        print(q.get())       #upper brand
        print(q.get())       #upper blemished
        print(q.get())       #stock/available
        print(q.get())       #price
        print(q.get())       #color
    #****************************#
    for pages in bcmLower:   #BCM Lower Reciever Scrape
        p=Process(target=scrape_bcmLower, args=(pages,q))
        p.start()
    for items in bcmLower:
        submitLowerGroup(q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get())
    #****************************#
    #for pages in aeroLower:   #aero Lower Reciever Scrape
     #   p=Process(target=scrape_aeroLower, args=(pages,q))
     #   p.start()
    #for items in aeroLower:
     #   submitLowerGroup(q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get())
    #****************************#
    #count=0 #index which barrel size to go in
    #for pages in aeroURG:   #aero Upper Reciever Group Scrape
     #   p=Process(target=scrape_aeroURG, args=(pages,sizes[count],q))
     #   p.start()
     #   count+=1
    #for items in aeroURG:
       #  submitURG(q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get(),q.get())
    #** TIMER **#
    end= time.time()
    print(end-start)