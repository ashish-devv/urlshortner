from flask import Flask,render_template,request,redirect
import random
import string
import sqlite3


app=Flask(__name__)


def randomno():
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(6)))

def uniqueornot(r):
    conn=sqlite3.connect('a.db')
    c=conn.cursor()
    s='SELECT * from urlcollection WHERE uniq="'+str(r)+'"'
    c.execute(s)
    all=c.fetchall()
    c.close()
    return all


@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        data = request.form['url']
        conn=sqlite3.connect('a.db')
        c=conn.cursor()
        n=0
        while(n==0):
            number=randomno()
            print(number)
            z=uniqueornot(number)
            print(z)
            if(z==[]):
                n=n+1
        number=str(number)
        s='INSERT INTO urlcollection (url,uniq) VALUES("'+data+'","'+number+'");'
        number=request.base_url+number
        c.execute(s)
        all=c.fetchone()
        conn.commit()
        c.close()
        return render_template("index.html",number=number)


@app.route("/<string:url>")
def redirecting(url):
    u=url
    conn=sqlite3.connect('a.db')
    c=conn.cursor()
    s='SELECT url from urlcollection WHERE uniq="'+u+'"'
    print(s)
    c.execute(s)
    all=c.fetchone()
    c.close()
    print(all)
    if(all==None):
        return "<center><h1>NO VALID URL</h1></center>"
    print(all[0])
    print(type(all[0]))
    return redirect(all[0])



if __name__ == "__main__":
    app.run(debug=False)
