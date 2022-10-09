from bs4 import BeautifulSoup
import requests
#---------------------გვერდის სქრაფინგი
pg=1
hh=[]
while pg<=10:
    url=f"https://www.myhome.ge/ka/s/iyideba-bina-rusTavi?Keyword=%E1%83%A0%E1%83%A3%E1%83%A1%E1%83%97%E1%83%90%E1%83%95%E1%83%98&AdTypeID=1&PrTypeID=1&Page={pg}&mapC=41.54309%2C45.01128&mapZ=12&mapOp=1&EnableMap=0&cities=5997314&GID=5997314"
    page=requests.get(url)
    pg = pg + 1
    hh.append(page)
print(hh)
souplist=[]
for pa in hh:
    soup=BeautifulSoup(pa.content, 'html.parser')#mtliani gverdis html
    souplist.append(soup)
counter=0
floor = []
rooms=[]
price = []
area = []
for i in range(0,len(souplist)):
    for a in souplist[i].find_all('a',href=True, attrs={'class':"card-container"}):
        m=a['href']
        pagee=requests.get(m)
        soup = BeautifulSoup(pagee.content, 'html.parser')
        f=soup.find("div",attrs={"class": "d-flex options"}).find("div")
        floor.append(f.text)
        r = soup.find("div", attrs={"class": "main-features"}).find("div")
        rooms.append(r.text)
        ar = soup.find('div', class_="item-size")
        area.append(ar.get_text())
        p = soup.find("b")
        price.append(p.get_text())
        if counter == 200:
            break
# print(floor)
# print(rooms)
# print(price)
# print(area)

#=========================================მონაცემების გაწმენდა
#------------------------------------------------სართული ['სართული: 1', 'სართული: 1', 'სართული: 5', 'სართული: 5']
listToStrf = ' '.join([str(i) for i in floor])
listToStrf2 = listToStrf.split(' ')
# print(listToStrf2)
for k in listToStrf2:
    if k == 'სართული:':
        listToStrf2.remove(k)
# print(listToStrf2)
#------------------------------------------------ოთახები['43.00 მ²1 ოთახი', '70.00 მ²4 ოთახი']
listToStrr = ' '.join([str(i) for i in rooms])
listToStrr2 = listToStrr.split('მ²')
listToStrr3 = ' '.join([str(i) for i in listToStrr2])
listToStrr4= listToStrr3.split(' ')
# print(listToStrr4)
for k in listToStrr4:
    if k == 'ოთახი' or k=='':
        listToStrr4.remove(k)
# print(listToStrr4)
every_other_elements = [listToStrr4[index] for index in range(1, len(listToStrr4), 2)]
# print(every_other_elements)
#---------------------------------------------------------------ფართი ['50.00 მ²', '65.00 მ²', '35.00 მ²', '71.00 მ²']
listToStra = ' '.join([str(i) for i in area])
listToStra2 = listToStra.split(' ')
# print(listToStra2)
for k in listToStra2:
    if k == 'მ²':
        listToStra2.remove(k)
# print(listToStra2)
#-----------------------------------------ფასი ['85,000', '105,000', '69,500'] მძიმე მოშორდება
listp=[]
for k in price:
    new =''
    for i in k:
        if i!= ',':
            new+=i
    listp.append(new)
# print(listp)
#====================================================================გრაფიკების აგება
import pandas as pd
import numpy as np

data={"area": listToStra2, "floor":listToStrf2 ,"rooms":every_other_elements , "price":listp}
# print(data)
df=pd.DataFrame(data)
# print(df)

# df.to_excel("datascrappin.xlsx", sheet_name="sheetOne")
dataa=pd.read_excel("datascrappin.xlsx")
#---------------------------------------------------- რეგრესიული მოდელი ( statistics)
print(f"Mean={round(dataa.price.mean(),2)}")
print(f"Meadian={round(dataa.price.median(),2)}")
print(f"std={round(dataa.price.std(),2)}")
np_data = np.array(dataa.price)  # percentili rom davtvalo magistvis minda numpy
print(f"50 Percentile = {round(np.percentile(np_data, 50 ),2)}")

import matplotlib.pyplot as plt
from scipy import stats
x=dataa.area
y=dataa.price
# plt.scatter(dataa.area,dataa.price, color = "red", s=20, marker='o') # r=korelaciaa
slope, intercept, r, p, std_err = stats.linregress(x, y)
def funcc_pd(x):
  return slope * x + intercept

Build_model = list(map(funcc_pd, x))         #print(funcc_pd([20, 30,40]))

plt.scatter(x,y, color = "red", s=20, marker='o')
plt.plot(x, Build_model)
plt.xlabel("m2")
plt.ylabel("price")
plt.show()


#-------------------------------------რეგრესიული მოდელი (ანალიზი)
from sklearn import linear_model
from plotnine import ggplot, aes, geom_point, geom_line
from plotnine.themes import theme_minimal
model=linear_model.LinearRegression()
X = dataa[['area']]   # satreningo da satesto monacembad unda daiyos
y= dataa.price
model.fit(X,y)
# print(model.intercept_) #b
# print(model.coef_) #k
print(f"Score = {model.score(X,y)}") #კორელაცია_სანდოობა
predict_info= np.array([[20],[30], [40]])
print(np.round(model.predict(predict_info), 2))




