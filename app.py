from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#$123456&*()'

# Koneksi MYSQL (PURE)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'peminjamanbuku_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/daftarBuku')
def daftar():
    container = []
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarBuku.html', container = hasil)

@app.route('/tentang')
def tentang():
    return render_template('tentangPerpustakaan.html')

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if (request.method == 'POST'):
        buku = request.form
        kodeBuku = buku['kodebuku']
        judulBuku = buku['judulbuku']
        stok = buku['stok']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tbuku(kodeBuku, judul, stok) VALUES(%s, %s, %s)', (kodeBuku, judulBuku, stok))
        mysql.connection.commit()
        cursor.close()
        return redirect('/daftarBuku')

    return render_template('tambahBuku.html')

@app.route('/pinjam')
def pinjam():
    return render_template('tambahBuku.html')

@app.route('/kembali')
def kembali():
    return render_template('tambahBuku.html')    

@app.route('/hapus/<kodeBuku>', methods = ['GET', 'POST'])
def hapus(kodeBuku):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tbuku WHERE kodeBuku=%s', (kodeBuku,))
    mysql.connection.commit()
    cursor.close()
    return redirect('/daftarBuku')

@app.route('/edit/<kodeBuku>', methods = ['GET', 'POST'])
def edit(kodeBuku):
    if (request.method == 'POST'):
        buku = request.form
        kodeBuku = buku['kodebuku']
        judulBuku = buku['judulbuku']
        stok = buku['stok']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE tbuku SET judul=%s, stok=%s WHERE kodeBuku=%s', (judulBuku, stok, kodeBuku))
        mysql.connection.commit()
        cursor.close()
        return redirect('/daftarBuku')
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku WHERE kodeBuku=%s', (kodeBuku,))
    hasil = cursor.fetchall()

    cursor.close()
    return render_template('editBuku.html', container = hasil)

if __name__ == "__main__":
    app.run(debug = True)