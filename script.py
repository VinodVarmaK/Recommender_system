import pandas as pd
import numpy as np
userItemData = pd.read_csv('C:/Users/Vinod Varma/Desktop/Python/brands_filtered.csv')
#userItemData.head()

#Get list of unique Brands
itemList=list(set(userItemData["brand_id"].tolist()))

#Get count of users
userCount=len(set(userItemData["brand_id"].tolist()))

#Create an empty data frame to store Brand affinity scores for Brands.
BrandAffinity= pd.DataFrame(columns=('Brand1', 'Brand2', 'score'))
rowCount=0

#For each item in the list, compare with other items.

for ind1 in range(len(itemList)):
    
    #Get list of users who bought this Brand 1.
    Brand1Users = userItemData[userItemData.brand_id==itemList[ind1]]["shopping_profile_id"].tolist()
    #print("Brand 1 ", Brand1Users)
    
   #Get item 2 - items that are not item 1 or those that are not analyzed already.
    for ind2 in range(ind1, len(itemList)):
        
        if ( ind1 == ind2):
            continue
       
        #Get list of users who bought item 2
        Brand2Users=userItemData[userItemData.brand_id==itemList[ind2]]["shopping_profile_id"].tolist()
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
        
#Check final result
BrandAffinity.head()

searchItem=131.0
recoList=BrandAffinity[BrandAffinity.Brand1==searchItem]\
        [["Brand2","score"]]\
        .sort_values("score", ascending=[0])
        
print("Recommendations for item 131.0\n", recoList)
