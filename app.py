from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/tentang')
def tentang():
    return render_template('tentangPerpustakaan.html')

# --------------------------------------------------
# [CRUD] BUKU
# --------------------------------------------------
@app.route('/daftarBuku')
def daftarBuku():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarBuku.html', container = hasil)

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

# --------------------------------------------------
# [C R] PINJAM
# --------------------------------------------------
@app.route('/pinjam')
def pinjam():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tpinjam')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarPinjam.html', container = hasil)

@app.route('/tambahPinjam', methods = ['GET', 'POST'])
def tambahPinjam():
    if (request.method == 'POST'):
        pinjam = request.form
        kodePinjam = pinjam['kodepinjam']
        kodeBuku = pinjam['kodebuku']
        nim = pinjam['NIM']
        tanggalPinjam = pinjam['tanggalpinjam']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT stok FROM tbuku WHERE kodeBuku=%s", (kodeBuku,))
        stok = cursor.fetchall()
        
        if(stok[0][0] > 0):
            cursor.execute("INSERT INTO tpinjam(kodePinjam, kodeBuku, NIM, tglPinjam) VALUES(%s, %s, %s, %s)", (kodePinjam, kodeBuku, nim, tanggalPinjam))
            cursor.execute('UPDATE tbuku SET stok=%s WHERE kodeBuku=%s', (stok[0][0] - 1, kodeBuku))
            mysql.connection.commit()
            cursor.close()
            return redirect('/pinjam')
        else:
            return redirect('/pinjam')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    kodeBuku = cursor.fetchall()
    
    cursor.execute('SELECT * FROM tanggota')
    nim = cursor.fetchall()
    cursor.close()


    return render_template('tambahPinjam.html', container = [kodeBuku, nim])

# --------------------------------------------------
# [C R] KEMBALI
# --------------------------------------------------
@app.route('/kembali')
def kembali():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tkembali')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarKembali.html', container = hasil)

@app.route('/tambahKembali', methods = ['GET', 'POST'])
def tambahKembali():
    if (request.method == 'POST'):
        kembali = request.form
        kodeKembali = kembali['kodeKembali']
        kodeBuku = kembali['kodebuku']
        nim = kembali['NIM']
        tanggalKembali = kembali['tanggalKembali']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT stok FROM tbuku WHERE kodeBuku=%s", (kodeBuku,))
        stok = cursor.fetchall()
        
        cursor.execute("INSERT INTO tkembali(kodeKembali, kodeBuku, NIM, tglKembali) VALUES(%s, %s, %s, %s)", (kodeKembali, kodeBuku, nim, tanggalKembali))
        cursor.execute('UPDATE tbuku SET stok=%s WHERE kodeBuku=%s', (stok[0][0] + 1, kodeBuku))
        mysql.connection.commit()
        cursor.close()
        return redirect('/kembali')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    kodeBuku = cursor.fetchall()
    
    cursor.execute('SELECT * FROM tanggota')
    nim = cursor.fetchall()
    cursor.close()

    return render_template('tambahKembali.html', container = [kodeBuku, nim])

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "POST"):
        datalogin = request.form
        username = datalogin['username']
        password = datalogin['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))
        hasil = cursor.fetchall()
        
        if (len(hasil) > 0):
            return redirect('/daftarBuku')

    return render_template('login.html')
    

# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)