
# coding: utf-8

# In[2]:

import pandas as pd
from datetime import datetime
import pytz
import os
import requests
from bs4 import BeautifulSoup


# In[3]:

cereal_urls=["http://www.walmart.com/search/?query=cereal&page="+str(i)+"&cat_id=0" for i in range(1,51)]
# by observation, when searching "cold cereal", results stop making sense after page 33
# so we just discard the rest of the data
cold_cereal_urls=["http://www.walmart.com/search/?query=cold+cereal&page="+str(i)+"&cat_id=0" for i in range(1,34)]


# In[4]:

# for each item, return a [brand,star,numReviews] list
# if the item's brand is not among the specified ones, name it as "Other"
def parseSoup(soup):
    info=[""]*3
    brand_name=soup.find("a",{"class":"js-product-title"}).text.split()
    rating_and_review=soup.find("div",{"class":"stars stars-small tile-row"})
    if(rating_and_review==None):
        # missing data for star: NA
        # missing data for numReviews: by default, 0 reviews
        rating_and_review=["NA","stars","(0)","ratings"]
    else:
        rating_and_review=rating_and_review.text.split()
    for i in range(len(brand_name)):
        if brand_name[i]=="Cheerios" or brand_name[i]=="Kashi"or brand_name[i]=="Kellogg's" or brand_name[i]=="Post":
            info[0]=brand_name[i]
            break
    if(info[0]==""):
        info[0]="Other"
    info[1]=rating_and_review[0]
    info[2]=rating_and_review[2][1:-1]
    return info


# In[5]:

# create two lists of all items on Walmart.com using the search term "cold cereal" and "cereal"
# each sublist in the list is of the format [brand,star,numReviews]
time=datetime.now().replace(microsecond=0)
all_cold_cereal_list=[]
for url in cold_cereal_urls:
    cereal_soup=BeautifulSoup(requests.get(url).content,"lxml")
    g_data=cereal_soup.findAll("div",{"class":"tile-content-wrapper"})
    for i in range(len(g_data)):
        info=parseSoup(g_data[i])
        all_cold_cereal_list.append(info)

        
all_cereal_list=[]
for url in cereal_urls:
    cereal_soup=BeautifulSoup(requests.get(url).content,"lxml")
    g_data=cereal_soup.findAll("div",{"class":"tile-content-wrapper"})
    for i in range(len(g_data)):
        info=parseSoup(g_data[i])
        all_cereal_list.append(info)
        
# compute the total number of all/top3 results for each brand
cereal_total={"Kellogg's":0,"Post":0,"Kashi":0,"Cheerios":0,"Other":0}
cereal_top3={"Kellogg's":0,"Post":0,"Kashi":0,"Cheerios":0,"Other":0}
cold_cereal_total={"Kellogg's":0,"Post":0,"Kashi":0,"Cheerios":0,"Other":0}
cold_cereal_top3={"Kellogg's":0,"Post":0,"Kashi":0,"Cheerios":0,"Other":0}
for i in range(len(all_cereal_list)):
    cereal_total[all_cereal_list[i][0]]+=1
    if(i<3):
        cereal_top3[all_cereal_list[i][0]]+=1
for i in range(len(all_cold_cereal_list)):
    cold_cereal_total[all_cold_cereal_list[i][0]]+=1
    if(i<3):
        cold_cereal_top3[all_cold_cereal_list[i][0]]+=1


# In[6]:

# update the dataset
add_header=False
if(not os.path.exists("Cereal_Data.csv")):
    add_header=True
    
idx=["(cold_cereal, top3)","(cold_cereal, all)","(cereal, top3)","(cereal, all)"]
df=pd.DataFrame(0,index=idx,columns=["Cheerios","Kashi","Kellogg's","Other","Post"])

df.loc["(cold_cereal, top3)"]=[i[1] for i in sorted(cold_cereal_top3.items())]
df.loc["(cold_cereal, all)"]=[i[1] for i in sorted(cold_cereal_total.items())]
df.loc["(cereal, top3)"]=[i[1] for i in sorted(cereal_top3.items())]
df.loc["(cereal, all)"]=[i[1] for i in sorted(cereal_total.items())]
df["Time"]=time

# may encounter some formatting issue if the file has been modified outside this program
with open("Cereal_Data.csv","a") as f:
    df.to_csv(f,header=add_header)


# In[7]:

# generate a dataset of ranking and stars
ranking_for_star=[]
star=[]
# assume the correlation between ranking and star is independent of search word
# so combine data for the two search terms
for i in range(len(all_cold_cereal_list)):
    # discard items that has no stars
    if(all_cold_cereal_list[i][1]!="NA"):
        ranking_for_star.append(i+1)
        star.append(all_cold_cereal_list[i][1])
for i in range(len(all_cereal_list)):
    if(all_cereal_list[i][1]!="NA"):
        ranking_for_star.append(i+1)
        star.append(all_cereal_list[i][1])
        
df_star=pd.DataFrame()
df_star["ranking"]=ranking_for_star
df_star["star"]=star
with open("Ranking_and_Star.csv","w") as f:
    df_star.to_csv(f,index=False)

# generate a dataset of ranking and numReviews
ranking_for_review=[]
review=[]
for i in range(len(all_cold_cereal_list)):
        ranking_for_review.append(i+1)
        review.append(all_cold_cereal_list[i][2])
for i in range(len(all_cereal_list)):
        ranking_for_review.append(i+1)
        review.append(all_cereal_list[i][2])

df_review=pd.DataFrame()
df_review["ranking"]=ranking_for_review
df_review["numReviews"]=review
with open("Ranking_and_Reviews.csv","w") as f:
    df_review.to_csv(f,index=False)

