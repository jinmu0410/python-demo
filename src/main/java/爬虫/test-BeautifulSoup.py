from bs4 import BeautifulSoup
#本地html解析，查看find、find_all、select

if __name__ == '__main__':
   fo = open("/Users/jinmu/Downloads/1.html",'r',encoding='utf-8')
   soup = BeautifulSoup(fo, "lxml")

   #print(soup)

   # find
   #print(soup.find('div',id='u1'))
   #print(soup.find_all('a',class_='mnav'))


   #select
   #print('id查找:', soup.select('#u1'))
   #print('class查找:',soup.select('.mnav'))
   #print('属性查找:', soup.select('a[name="tj_trmap"]'))
   list = soup.select('.mnav')
   for a in list:
       print(a.text)



