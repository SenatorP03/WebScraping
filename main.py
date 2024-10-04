import time
import  requests
import selectorlib
import ssl
import smtplib
import time
import sqlite3

"INSERT INTO events VALUES('Tiger','Tiger city','2010.11.20')"
"Select * FROM events WHERE Date = '2010.01.20'"


URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("SQLlite db.db")


#getting data from the site
def scrape(url):
    """Scrape the page source from URL"""
    response = requests.get(url)
    source = response.text
    return source

#extracting the tour from the main scrapped text
def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "adeiyeprecious650@gmail.com"
    password = "ysytdlporvfiamjo"

    reciever = "adeiyeprecious650@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, reciever, message)
        print("Email was sent")

#creates a txt file to store the tours gotten
def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    connection.commit()

#create a function to read the data.txt file
def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    Band,City,Date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE Band =? AND City=? AND Date=?",
                   (Band,City,Date))
    rows = cursor.fetchall()
    print(rows)
    return (rows)


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message= "hey there is an upcoming event")
        time.sleep(2)