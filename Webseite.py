from flask import Flask
from flask import render_template
import sqlite3
from flask import request
from flask import redirect
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
    conn = connect_db()
    rezepte = conn.execute('SELECT * FROM rezepte WHERE rezepte.Rubrik LIKE ?', ["%"+rubrik+"%"]).fetchall()
    conn.close()
    return render_template("rubrik.html", rezepte = rezepte, titel=rubrik)

@app.route("/Suche")
def suche():
    conn = connect_db()
    rezepte = conn.execute('SELECT * FROM rezepte').fetchall()
    conn.close()
    return render_template("suche.html", rezepte = rezepte)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    #Form being submitted; grab data from form.
    suche = request.form['suchfeld']
    #At the end: Redirect to correct page
    return redirect("/Suche_"+suche)

@app.route("/Suche_<suche>")
def suche_liste(suche):
    conn = connect_db()
    rezepte = conn.execute('SELECT * FROM rezepte WHERE rezepte.Titel LIKE ?', ["%"+suche+"%"])
    #conn.close()
    return render_template("suche_liste.html", rezepte = rezepte)

@app.route("/detail_<rezeptID>")
def detail(rezeptID):

    conn = connect_db()
    current_rezept = conn.execute('SELECT * FROM rezepte WHERE rezeptID=?', [rezeptID]).fetchone()
    Zutatenliste = conn.execute('SELECT * FROM Zutaten WHERE rezeptID=?', [rezeptID]).fetchall()
#     Zutatenliste = current_rezept.Zutaten.split(",")
#     print(Zutatenliste)
    return render_template("detail.html", rezept = current_rezept, zutaten = Zutatenliste)

@app.route("/Rezept_hinzufügen")
def rezept_hinzufügen():
    conn = connect_db()
    conn.close()
    return render_template("rezept_hinzufügen.html")

@app.route('/handle_insert', methods=['POST'])
def handle_insert():
    #Form being submitted; grab data from form.
    titel = request.form['Titel']
    rubrik = request.form['Rubrik']
    anleitung = request.form['Anleitung']
    schwierigkeit = request.form['Schwierigkeit']
    zubereitungszeit = request.form['Zubereitungszeit']
    infos = request.form['Infos']
    personen = request.form['Personen']
    zutaten = request.form['Zutaten']
    bild = request.form['Bild']
    zutatenList = zutaten.split(",")
    #Rezept in Datenbank einfügen
    conn = connect_db()
    conn.execute('INSERT INTO rezepte (Titel, Rubrik, Anleitung, Schwierigkeit, Zubereitungszeit, Bildname, Infos, Personen) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [titel, rubrik, anleitung, schwierigkeit, zubereitungszeit, bild, infos, personen])
    current_rezept = conn.execute('SELECT * FROM rezepte WHERE rezeptID in(SELECT MAX(rezeptID) FROM rezepte)').fetchone()
    rezeptID = current_rezept["rezeptID"]
    for zutat in zutatenList:
        conn.execute('INSERT INTO Zutaten (rezeptID, Zutaten) VALUES (?, ?)', [rezeptID, zutat])
    conn.commit()
    conn.close()
    #At the end: Redirect to correct page
    return redirect("/rezept_hinzufügen_bestätigung")

@app.route("/rezept_hinzufügen_bestätigung")
def rezept_hinzufügen_bestätigung():
    conn = connect_db()
    current_rezept = conn.execute('SELECT * FROM rezepte WHERE rezeptID in(SELECT MAX(rezeptID) FROM rezepte)').fetchone()
    return render_template("rezept_hinzufügen_bestätigung.html", rezept = current_rezept)