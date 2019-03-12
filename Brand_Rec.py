
# coding: utf-8

# In[25]:

import pandas as pd
import numpy as np

userBrandData = pd.read_csv('C:/Users/Vinod Varma/Desktop/Python/brands_filtered_short.txt', sep='\t')
#userBrandData.head()

#Get list of unique Brands
itemList=list(set(userBrandData["brand_id"].tolist()))

#Get count of users
userCount=len(set(userBrandData["brand_id"].tolist()))


#Create an empty data frame to store Brand affinity scores for Brands.
BrandAffinity= pd.DataFrame(columns=('Brand1', 'Brand2', 'score'))
rowCount=0
BrandAffinity.head()
#For each item in the list, compare with other items.

for ind1 in range(len(itemList)):
    
    #Get list of users who bought this Brand 1.
    Brand1Users = userBrandData[userBrandData.brand_id==itemList[ind1]]["shopping_profile_id"].tolist()
    #print("Brand 1 ", Brand1Users)
    
   #Get Brand 2 - Brands that are not item 1 or those that are not analyzed already.
    for ind2 in range(ind1, len(itemList)):
        
        if ( ind1 == ind2):
            continue
       
        #Get list of users who bought Brand 2
        Brand2Users=userBrandData[userBrandData.brand_id==itemList[ind2]]["shopping_profile_id"].tolist()
        #print("Brand 2",Brand2Users)
        
        #Find score. Find the common list of shopping_profile_id's and divide it by the total users.
        commonUsers= len(set(Brand1Users).intersection(set(Brand2Users)))
        score=commonUsers / userCount
        
        #Add a score for Brand 1, Brand 2
        BrandAffinity.loc[rowCount] = [itemList[ind1],itemList[ind2],score]
        rowCount +=1
        
        #Add a score for Brand2, Brand 1. The same score would apply irrespective of the sequence.
        BrandAffinity.loc[rowCount] = [itemList[ind2],itemList[ind1],score]
        rowCount +=1
        
searchItem= 552
recoList=pd.DataFrame(BrandAffinity[BrandAffinity.Brand1==searchItem]        [["Brand2","score"]]        .sort_values("score", ascending=[0]))

#Transaformation of fields accordingly
recoList['Brand2'] = recoList['Brand2'].dropna().apply(np.int64)
recoList = recoList.iloc[0:10]
recoList = recoList[['Brand2','score']]

userBrandData1 = userBrandData[['brand_id','name']]
recoList.reset_index(inplace=True)
Final = pd.merge(recoList, userBrandData1, how='left', left_on='Brand2', right_on='brand_id')
Final1 = Final[['Brand2','score','name']]
Final_Affinity = Final1.drop_duplicates(['Brand2'])

print("Recommendations for item Steve Madden\n", Final_Affinity)

