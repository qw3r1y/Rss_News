from multiprocessing import connection
import mysql.connector
import feedparser

url = "https://threatpost.com/feed/" 
url2 = "https://www.bleepingcomputer.com/feed/"  
url3 = "https://hnrss.org/frontpage"
url4 = "https://latesthackingnews.com/feed/"

threatpost = feedparser.parse(url)
bleepingcomputer = feedparser.parse(url2)
hnrss= feedparser.parse(url3)
latesthackingnews = feedparser.parse(url4)

def savetoDb(newsUrl): 
    connection = mysql.connector.connect(host = "localhost" , user = "root" , password = "toor" , database = "hackernews")
    cursor = connection.cursor()

    links = "SELECT HaberLink FROM hackernews;"
    cursor.execute(links)
    myresult = cursor.fetchall()
    
    linksFromDB = []    
    for link in myresult: 
        linksFromDB.append(link[0])

    for etu in newsUrl.entries:
        if not linksFromDB.__contains__(etu.link):
            print("Yeni Haberler Eklendi")
            sql = "INSERT INTO hackernews (HaberBaslik, HaberIcerik, HaberLink, HaberYazar ,Tarih) VALUES (%s,%s,%s,%s,%s)" 
            values = (etu.title,etu.description,etu.link,etu.author,etu.published)
            cursor.execute(sql , values)   
        else:
            print("Haberler var.")
            
    try:
        connection.commit()

    except mysql.connector.Error as err:
        print(err)

    finally:
        connection.close()
        print("Veriler aktarıldı.")

savetoDb(threatpost)
savetoDb(bleepingcomputer)
savetoDb(hnrss)
savetoDb(latesthackingnews)
