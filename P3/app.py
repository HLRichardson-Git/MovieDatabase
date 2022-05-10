import re
from flask import Flask, request, render_template, url_for, flash, redirect

import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123password",
    database="testdb"
)

mycursor = mydb.cursor(buffered=True)

sql = "SELECT * FROM movies ORDER BY year DESC"

formatted_list = []

mycursor.execute(sql)
myresult = mycursor.fetchmany(size = 100)

for w,x,y,z in myresult:
    dictionary = {"Title": w, "Year": x, "Cast": y, "Genres(s)": z}
    formatted_list.append(dictionary)




@app.route('/home')
@app.route('/', methods=["POST", "GET"])
def index():

    search_list = []

    if request.method == "POST":
        
        search = request.form["search"]
        
        sqlFormula = "INSERT INTO categoryhistory (categoryName) VALUES (%s)"
        t = []
        t.append(search)

        mycursor.execute(sqlFormula, t)
        mydb.commit()

        sqlSearch = "SELECT * FROM movies WHERE title LIKE '%" + str(search) + "%'"
        mycursor.execute(sqlSearch)
        searchResult = mycursor.fetchall()

        for w,x,y,z in searchResult:
            dictionary = {"Title": w, "Year": x, "Cast": y, "Genres(s)": z}
            search_list.append(dictionary)
        
        return render_template("index.html", list=search_list)
    else:
        return render_template("index.html", list=formatted_list)


@app.route('/movie/<key>')
def movie(key): 

    sqlFormula = "INSERT INTO movieHistory (historyName) VALUES (%s)"
    t = []
    t.append(key)

    mycursor.execute(sqlFormula, t)
    mydb.commit()

    result = []

    sqlFetch = "SELECT * FROM movies WHERE title ='" + key + "'"
    mycursor.execute(sqlFetch)
    fetchResult = mycursor.fetchall()

    for w,x,y,z in fetchResult:
        dictionary = {"Title": w, "Year": x, "Cast": y, "Genres(s)": z}
        result.append(dictionary)

    return render_template('movie.html', result=result)

@app.route('/history')
def history():

    sqlHistory = "SELECT * FROM movieHistory"
    mycursor.execute(sqlHistory)
    clickResult = mycursor.fetchall()

    clickHistory = []
    
    for x in clickResult:
        dictionary = {"Title": x}
        clickHistory.append(dictionary)

    sqlSearchHistory = "SELECT * FROM categoryHistory"
    mycursor.execute(sqlSearchHistory)
    searchResult = mycursor.fetchall()

    searchHistory = []
    
    for x in searchResult:
        dictionary2 = {"Title": x}
        searchHistory.append(dictionary2)

    return render_template("history.html", clickHistory=clickHistory, searchHistory=searchHistory)

if __name__ == "__main__":
    app.run(debug=True)