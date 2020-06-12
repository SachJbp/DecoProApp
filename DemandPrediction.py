import math
import pandas as pd
import os


def clean(prod):
    ###Cleaning script
    #list_prod=prod.split(" ")
    #data=pd.read_excel("SellerCloud Product Export 2_18_20.xlsx")
    prod.ProductType=prod.ProductType.str.replace('â€º','-')
    prod.ProductType=prod.ProductType.str.replace('DÃ©cor','Dacor')
    prod.ProductName=prod.ProductName.str.replace('â„¢','')
    prod.ProductType=prod.ProductType.str.replace('Â\xa0',' ')
    return prod





def demandpred(data,data1):
        #filename="SellerCloud Product Export 2_18_20.xlsx"
        #return "grt"
        #app.config['UPLOD_FOLDER'] = '/tmp'
        #return "grt"
        #filepath=os.path.join(app.config['UPLOD_FOLDER'], filename)
        #data=pd.read_excel("./tmp/SellerCloud Product Export 2_18_20.xlsx")
        #return "grt"
        data=clean(data)
        data['Sales-Month1']=data['QtySold90']-data['QtySold60']
        data['Sales-Month2']=data['QtySold60']-data['QtySold30']
        data['Sales-Month3']=data['QtySold30']
        data=data[data['ID'].notna()]
        data.shape


        #Open the child product sheet
        #data1=pd.read_excel("Products with demand and Inv Replenishment.xlsx")

        data.shape
        id2=data1['Product ID']
        data1=data1.set_index('Product ID')
        data=data.set_index('ID')
        id2.shape
        id2=id2.values

        sales1=[None]*data1.shape[0]
        sales2=[None]*data1.shape[0]
        sales3=[None]*data1.shape[0]
        id2=data.index
        i=0
        for id1 in data1.index:
            if id1 in id2:
                #print("s")
                sales1[i]=data.loc[id1]['Sales-Month1']
                sales2[i]=data.loc[id1]['Sales-Month2']
                sales3[i]=data.loc[id1]['Sales-Month3']
            i+=1
            

        data1['Sales-Month1']=sales1
        data1['Sales-Month2']=sales2
        data1['Sales-Month3']=sales3

        #exponential weighted average
        import math
        num_months=3
        d=3
        for i in range(1,num_months+1):
            beta=(d-1)/d
            data1['v1']=data1['Sales-Month1']
            data1['v2']=beta*data1['v1']+(1-beta)*data1['Sales-Month2']
            data['PredDemand'+str(i)]=beta*data1['v2']+(1-beta)*data1['Sales-Month3']
            data['PredDemand'+str(i)]=data1['PredDemand'+str(i)].apply(lambda x: math.ceil(x))
            median=data1.groupby(by='Style')['PredDemand'+str(i)].median()
            median1=data1.groupby(by='Type')['PredDemand'+str(i)].median()
            d+=2

        median=median.to_dict()
        median1=median1.to_dict()

        for j in range(1,num_months+1):
            AdjustedDemand=[]
            AdjustedDemand1=[]
            for i in range(data1.shape[0]):
                try:
                    col1='PredDemand'+str(j)
                    if data.iloc[i][col1]!=0:
                        AdjustedDemand.append(data1.iloc[i][col1])
                        AdjustedDemand1.append(data1.iloc[i][col1])
                    else:
                        AdjustedDemand.append(median[data1.iloc[i]['Style']])
                        AdjustedDemand1.append(median1[data1.iloc[i]['Type']])
                except:
                    AdjustedDemand.append(0)
                    AdjustedDemand1.append(0)
            
            col1='Adjusted Demand(using median demand groupby Style)'+str(j)
            col2='Adjusted Demand(using median demand groupby Type)'+str(j)
            data1[col1]=AdjustedDemand
            data1[col1]=data1[col1].apply(lambda x: math.ceil(x))
            data1[col2]=AdjustedDemand1
            data1[col2]=data1[col2].apply(lambda x: math.ceil(x))

        return data1
        #data1.to_excel("Products with demand (using EXP WEIGHTED AVG)-test.xlsx")
        

