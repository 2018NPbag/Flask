from flask import Flask
from flask import render_template
import sqlite3
app = Flask(__name__)
#my_films=[{"title":"Hobbit","muvieId":0,"content": "Bilbo Beutlin"},{"title":"Herr der Ringe","muvieId":1, "content": "Frodo Beutlin"},{"title":"Harry Potter","muvieId":2}]

def connect_db():
    conn = sqlite3.connect('Rezept.db.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = connect_db()
    rezepte = conn.execute('SELECT * FROM rezepte').fetchall()
    conn.close()
    return render_template("home.html", rezept = rezepte)

@app.route("/Rubrik_<rubrik>")
def rubrik(rubrik):
    print(rubrik)
    conn = connect_db()
    rezepte = conn.execute('SELECT * FROM rezepte WHERE rezepte.Rubrik LIKE ?', ["%"+rubrik+"%"]).fetchall()
    conn.close()
    return render_template("rubrik.html", rezepte = rezepte, titel=rubrik)

@app.route("/Suche")
def suche(Titel):
    conn = connect_db()
    rezepte = conn.execute('SELECT * FROM rezepte').fetchall()
    conn.close()
    return render_template("suche.html", rezepte = rezepte)


@app.route("/Detail_<rezeptID>")
def detail(rezeptID):

    conn = connect_db()
    current_rezept = conn.execute('SELECT * FROM rezepte WHERE rezeptID=?', [rezeptID]).fetchone()
    Zutatenliste = conn.execute('SELECT * FROM Zutaten WHERE rezeptID=?', [rezeptID]).fetchall()
#     Zutatenliste = current_rezept.Zutaten.split(",")
#     print(Zutatenliste)
    return render_template("detail.html", rezept = current_rezept, zutaten = Zutatenliste)
