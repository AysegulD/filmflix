
from flask import Flask,flash,render_template,request,url_for,redirect,abort
import sqlite3 as sql

app = Flask(__name__)

def filmflix():
    conn = sql.connect('filmflix.db')
    conn.row_factory = sql.Row
    return conn

@app.route('/')

@app.route('/home')

def home():
    return render_template('home.html',title="Home")

@app.route('/addmovie',methods = ['GET','POST'])

def addmovie():
    if request.method == 'POST':
        title = request.form['title']
        yearReleased = request.form['yearReleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        conn = filmflix()
        cursor = conn.cursor()
        filmID = cursor.lastrowid


        cursor.execute('INSERT INTO tblFilms (filmID,title,yearReleased,rating,duration,genre) VALUES(?,?,?,?,?,?)',(filmID,title,yearReleased,rating,duration,genre))
        conn.commit()
        conn.close()
        return redirect(url_for('movies'))
    return render_template('addmovie.html',title="Add Movie")


@app.route('/movies')
def movies():
    conn = filmflix()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tblFilms')
    getFilms = cursor.fetchall()

    return render_template('movies.html',title="Movies",revokeFilm = getFilms)
def getFilmID(movieID):
    conn = filmflix()
    cursor = conn.cursor()
    movie =cursor.execute('SELECT * FROM tblFilms WHERE filmID = ?',(movieID,)).fetchone()
    conn.close()
    if movie is None:
        abort(404)
    return movie

@app.route('/<int:filmID>/updatemovie',methods = ['GET','POST'])

def updatemovie(filmID):
    movieRecord = getFilmID(filmID)
    if request.method == 'POST':
        title = request.form['title']
        yearReleased = request.form['yearReleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        conn = filmflix()
        cursor = conn.cursor()
        cursor.execute('UPDATE tblFilms SET title =?, yearReleased =?, rating =?, duration=?, genre=? WHERE filmID=?',(title,yearReleased,rating,duration,genre,filmID,))
        conn.commit()
        conn.close()
        return redirect(url_for('movies'))

    return render_template('updatemovie.html',title="Update Movie",movieRecord = movieRecord)


@app.route('/<int:filmID>/delete',methods=['POST',])
def delete(filmID):
    conn = filmflix()
    cursor =conn.cursor()
    cursor.execute('DELETE FROM tblFilms WHERE filmID =? ',(filmID,))
    conn.commit()
    conn.close()
    return redirect(url_for('movies'))

    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
