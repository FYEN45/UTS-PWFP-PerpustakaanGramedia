import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash
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
        try:
            buku = request.form
            kodeBuku = buku['kodebuku']
            judulBuku = buku['judulbuku']
            stok = buku['stok']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tbuku(kodeBuku, judul, stok) VALUES(%s, %s, %s)', (kodeBuku, judulBuku, stok))
            mysql.connection.commit()
            cursor.close()

            flash('Buku berhasil ditambahkan!')
            return redirect('/daftarBuku')

        except (MySQLdb.Error) as err:
            flash('Buku gagal ditambahkan! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/daftarBuku')

    return render_template('tambahBuku.html')

@app.route('/hapus/<kodeBuku>', methods = ['GET', 'POST'])
def hapus(kodeBuku):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tbuku WHERE kodeBuku=%s', (kodeBuku,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Buku berhasil dihapus!')
        return redirect('/daftarBuku')

    except (MySQLdb.Error) as err:
        flash('Buku gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/daftarBuku')

@app.route('/edit/<kodeBuku>', methods = ['GET', 'POST'])
def edit(kodeBuku):
    if (request.method == 'POST'):
        try:
            buku = request.form
            kodeBuku = buku['kodebuku']
            judulBuku = buku['judulbuku']
            stok = buku['stok']

            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tbuku SET judul=%s, stok=%s WHERE kodeBuku=%s', (judulBuku, stok, kodeBuku))
            mysql.connection.commit()
            cursor.close()

            flash('Buku berhasil diedit!')
            return redirect('/daftarBuku')
        
        except (MySQLdb.Error) as err:
            flash('Buku gagal diedit! %d: %s' % (err.args[0], err.args[1]))
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
        try:
            pinjam = request.form
            kodePinjam = pinjam['kodepinjam']
            kodeBuku = pinjam['kodebuku']
            nim = pinjam['NIM']
            tanggalPinjam = pinjam['tanggalpinjam']

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT stok FROM tbuku WHERE kodeBuku=%s", (kodeBuku,))
            stok = cursor.fetchall()
            
            if (stok):
                if(stok[0][0] > 1):
                    cursor.execute("INSERT INTO tpinjam(kodePinjam, kodeBuku, NIM, tglPinjam) VALUES(%s, %s, %s, %s)", (kodePinjam, kodeBuku, nim, tanggalPinjam))
                    cursor.execute('UPDATE tbuku SET stok=%s WHERE kodeBuku=%s', (stok[0][0] - 1, kodeBuku))
                    mysql.connection.commit()
                    cursor.close()
                    
                    flash('Berhasil meminjam buku!')
                    return redirect('/pinjam')
                else:
                    flash('Gagal meminjam buku! Stok buku habis!')
                    return redirect('/pinjam')

        except (MySQLdb.Error) as err:
            flash('Gagal Pinjam! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/pinjam')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    kodeBuku = cursor.fetchall()
    
    cursor.execute('SELECT * FROM tanggota')
    nim = cursor.fetchall()
    cursor.close()

    return render_template('tambahPinjam.html', container = [kodeBuku, nim])

@app.route('/hapusPinjam/<kodePinjam>', methods = ['GET', 'POST'])
def hapusPinjam(kodePinjam):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tpinjam WHERE kodePinjam=%s', (kodePinjam,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Peminjaman berhasil dihapus!')
        return redirect('/pinjam')

    except (MySQLdb.Error) as err:
        flash('Peminjaman gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/pinjam')

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
        try:
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

            flash('Berhasil mengembalikan buku!')
            return redirect('/kembali')
        
        except (MySQLdb.Error) as err:
            flash('Gagal mengembalikan buku! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/kembali')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    kodeBuku = cursor.fetchall()
    
    cursor.execute('SELECT * FROM tanggota')
    nim = cursor.fetchall()
    cursor.close()

    return render_template('tambahKembali.html', container = [kodeBuku, nim])

@app.route('/hapusKembali/<kodeKembali>', methods = ['GET', 'POST'])
def hapusKembali(kodeKembali):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tkembali WHERE kodeKembali=%s', (kodeKembali,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Pengembalian berhasil dihapus!')
        return redirect('/kembali')

    except (MySQLdb.Error) as err:
        flash('Pengembalian gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/kembali')

# --------------------------------------------------
# [CRUD] Anggota
# --------------------------------------------------
@app.route('/anggota', methods = ['GET', 'POST'])
def daftarAnggota():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tanggota')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarAnggota.html', container = hasil)

@app.route('/tambahAnggota', methods=['GET', 'POST'])
def tambahAnggota():
    if (request.method == 'POST'):
        try:
            anggota = request.form
            nim = anggota['NIM']
            namaMhs = anggota['namamahasiswa']
            jurusan = anggota['jurusan']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tanggota(NIM, namaMhs, jurusan) VALUES(%s, %s, %s)', (nim, namaMhs, jurusan))
            mysql.connection.commit()
            cursor.close()
            
            flash('Berhasil menambahkan anggota!')
            return redirect('/anggota')
        
        except (MySQLdb.Error) as err:
            flash('Gagal menambahkan anggota! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/anggota')

    return render_template('tambahAnggota.html')

@app.route('/hapusAnggota/<NIM>', methods = ['GET', 'POST'])
def hapusAnggota(NIM):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tanggota WHERE NIM=%s', (NIM,))
        mysql.connection.commit()
        cursor.close()

        flash('Berhasil menghapus anggota!')
        return redirect('/anggota')

    except (MySQLdb.Error) as err:
            flash('Gagal menghapus anggota! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/anggota')

@app.route('/editAnggota/<NIM>', methods = ['GET', 'POST'])
def editAnggota(NIM):
    if (request.method == 'POST'):
        try:
            anggota = request.form
            nim = anggota['NIM']
            namaMhs = anggota['namamahasiswa']
            jurusan = anggota['jurusan']

            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tanggota SET namaMhs=%s, jurusan=%s WHERE NIM=%s', (namaMhs, jurusan, nim))
            mysql.connection.commit()
            cursor.close()
            
            flash('Berhasil mengedit anggota!')
            return redirect('/anggota')

        except (MySQLdb.Error) as err:
            flash('Gagal mengedit anggota! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/anggota')
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tanggota WHERE NIM=%s', (NIM,))
    hasil = cursor.fetchall()

    cursor.close()
    return render_template('editAnggota.html', container = hasil)

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
            flash('Login Berhasil! Welcome %s!' % username)
            return redirect('/daftarBuku')
        else:
            flash('Username & Password salah!')
            return render_template('login.html')

    return render_template('login.html')
    

# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)