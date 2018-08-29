from urllib2 import urlopen
import urllib2
import json
import sys
import MySQLdb


# Function to establish a connection with database
def dbconnect():
    try:
        db = MySQLdb.connect(
            host="localhost",
            user="<username>",
            passwd="<password>",
        )
    except Exception as e:
        sys.exit("Can't connect to Database")
    return db


def create_db(db_name, table_name):
    try:
        db = dbconnect()
        cursor = db.cursor()

        # for creating database this line will hide warning
        cursor.execute("SET sql_notes = 0;")

        # Create Database:
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_name))

        """Note: Create Database and Tables."""
        cursor.execute("SET sql_notes = 0;")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS {}.{}(id INT primary key auto_increment,article_num int(10) unique key,title varchar(150));""".format(db_name, table_name))

        cursor.execute("SET sql_notes = 1;")

        """ Fetch data from api, used json.load, convert between files and objects. Output will be list of dict."""
        # Method 1:
        # response = urllib2.urlopen("https://jsonplaceholder.typicode.com/posts")
        # print response
        # data = json.load(response)

        # Method 2:
        TO = 1
        website = ("https://jsonplaceholder.typicode.com/posts")
        try:
            response = urlopen(website, timeout=TO)
            data = json.load(response)
        except:
            print "Sorry, try again"

        """ Reading from Json file """
        # Method 3:
        # with open('book_info.json') as f:
        #     data = json.load(f)

        """Note: Insert into Database. Iterate over the list and save desired items from dict to the database columns.
           We set the column "article_num" as unique, ON DUPLICATE KEY UPDATE it will check if "article_num" already exists, if not than simply update column."""

        for i in data:
            cursor.execute(
                """INSERT INTO {}.{}(article_num, title) VALUES(%s,%s)
                ON DUPLICATE KEY UPDATE article_num =%s """.format
                (db_name, table_name),
                (i['id'], i['title'], i['id']))

        db.commit()
        db.close()

    except Exception as e:
        print e

# Call function to create Database and Table.
create_db(db_name="my_book", table_name="articles")
