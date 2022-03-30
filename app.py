# Import Library yang dibutuhkan
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = '@#$123456&*()'

# Koneksi MYSQL (Tanpa SQLAlchemy)
# Mempersiapkan koneksi dengan server mysql.
# Menentukan HOST, USER, PASSWORD, dan DATABASE yang akan diakses
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'peminjamanbuku_db'

mysql = MySQL(app)

# Routing website ke halaman Home (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Routing website ke halaman Tentang Kami ('tentangPerpustakaan.html)
@app.route('/tentang')
def tentang():
    return render_template('tentangPerpustakaan.html')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# [CRUD] BUKU
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Routing website ke halaman Daftar Buku
# Mengambil data dari database tabel buku lalu menampilkannya di halaman Daftar Buku
@app.route('/daftarBuku')
def daftarBuku():

    # Menghubungkan ke database dan melakukan SELECT pada tabel buku
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    hasil = cursor.fetchall()

    cursor.close()
    return render_template('daftarBuku.html', container = hasil)

# Routing website ke halaman Tambah Buku
# Menampilkan halaman tambah buku
# Apabila form pada halaman tambah buku melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan percobaan menambahkan buku dalam tabel buku.
# Apabila sukses / gagal menambahkan buku dalam database akan menampilkan pesan dan redirect ke halaman Daftar Buku
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if (request.method == 'POST'):
        try:
            # Mengambil input dari form
            buku = request.form
            kodeBuku = buku['kodebuku']
            judulBuku = buku['judulbuku']
            stok = buku['stok']

            # Menghubungkan ke database dan melakukan Insert ke tabel buku
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tbuku(kodeBuku, judul, stok) VALUES(%s, %s, %s)', (kodeBuku, judulBuku, stok))
            mysql.connection.commit()
            cursor.close()

            flash('Buku berhasil ditambahkan!')
            return redirect('/daftarBuku')

        except (MySQLdb.Error) as err:
            # Menangkap error dan memberikan pesan gagal
            flash('Buku gagal ditambahkan! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/daftarBuku')

    return render_template('tambahBuku.html')

# Routing website ke halaman Hapus Buku
# Tidak me-render template apapun, dan langsung menjalankan fungsi hapus buku
# Apabila sukses / gagal menghapus buku dalam database akan menampilkan pesan dan redirect ke halaman Daftar Buku
@app.route('/hapus/<kodeBuku>', methods = ['GET', 'POST'])
def hapus(kodeBuku):
    try:
        # Menghubungkan ke database dan melakukan DELETE pada tabel buku
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tbuku WHERE kodeBuku=%s', (kodeBuku,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Buku berhasil dihapus!')
        return redirect('/daftarBuku')

    except (MySQLdb.Error) as err:
        # Menangkap error dan memberikan pesan gagal
        flash('Buku gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/daftarBuku')

# Routing website ke halaman Edit Buku
# Menampilkan halaman Edit Buku, lengkap dengan data buku yang akan di edit
# Apabila form pada halaman edit buku melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan percobaan mengedit buku dalam tabel buku.
# Apabila sukses / gagal mengedit buku dalam database akan menampilkan pesan dan redirect ke halaman Daftar Buku
@app.route('/edit/<kodeBuku>', methods = ['GET', 'POST'])
def edit(kodeBuku):
    if (request.method == 'POST'):
        try:
            # Mengambil input dari form
            buku = request.form
            kodeBuku = buku['kodebuku']
            judulBuku = buku['judulbuku']
            stok = buku['stok']

            # Menghubungkan ke database dan melakukan UPDATE pada tabel buku
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tbuku SET judul=%s, stok=%s WHERE kodeBuku=%s', (judulBuku, stok, kodeBuku))
            mysql.connection.commit()
            cursor.close()

            flash('Buku berhasil diedit!')
            return redirect('/daftarBuku')
        
        except (MySQLdb.Error) as err:
            # Menangkap Error dan memberikan pesan gagal
            flash('Buku gagal diedit! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/daftarBuku')
    
    # Menghubungkan ke database dan mengambil informasi buku yang akan di edit
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku WHERE kodeBuku=%s', (kodeBuku,))
    hasil = cursor.fetchall()

    cursor.close()
    return render_template('editBuku.html', container = hasil)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# [C R] PINJAM
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Routing website ke halaman Daftar Peminjam
# Menampilkan halaman Daftar Peminjam, lengkap dengan data - data peminjam
@app.route('/pinjam')
def pinjam():

    # Menghubungkan ke database dan melakukan SELECT pada tabel pinjam
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tpinjam')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarPinjam.html', container = hasil)

# Routing website ke halaman Tambah Peminjam
# Menampilkan halaman tambah peminjam
# Apabila form pada halaman tambah peminjam melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan percobaan menambahkan peminjam dalam tabel pinjam.
# Apabila sukses / gagal menambahkan peminjam dalam database akan menampilkan pesan dan redirect ke halaman Daftar Peminjam
@app.route('/tambahPinjam', methods = ['GET', 'POST'])
def tambahPinjam():
    if (request.method == 'POST'):
        try:
            # Mengambil input dari form
            pinjam = request.form
            kodePinjam = pinjam['kodepinjam']
            kodeBuku = pinjam['kodebuku']
            nim = pinjam['NIM']
            tanggalPinjam = pinjam['tanggalpinjam']

            # Menghubungkan ke database dan melakukan SELECT pada tabel buku
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT stok FROM tbuku WHERE kodeBuku=%s", (kodeBuku,))
            stok = cursor.fetchall()
            
            if (stok):
                if(stok[0][0] > 1):
                    # Memeriksa apakah stok buku tersedia
                    # Melakukan INSERT data peminjam
                    # Melakukan UPDATE jumlah stok buku
                    cursor.execute("INSERT INTO tpinjam(kodePinjam, kodeBuku, NIM, tglPinjam) VALUES(%s, %s, %s, %s)", (kodePinjam, kodeBuku, nim, tanggalPinjam))
                    cursor.execute('UPDATE tbuku SET stok=%s WHERE kodeBuku=%s', (stok[0][0] - 1, kodeBuku))
                    mysql.connection.commit()
                    cursor.close()
                    
                    flash('Berhasil meminjam buku!')
                    return redirect('/pinjam')
                else:
                    # Apabila stok tidak tersedia dan memberikan pesan buku habis
                    flash('Gagal meminjam buku! Stok buku habis!')
                    return redirect('/pinjam')

        except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
            flash('Gagal Pinjam! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/pinjam')

    # Menghubungkan ke database dan melakukan SELECT dari tabel buku
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    kodeBuku = cursor.fetchall()
    
    # Menghubungkan ke database dan melakukan SELECT dari tabel anggota
    cursor.execute('SELECT * FROM tanggota')
    nim = cursor.fetchall()
    cursor.close()

    return render_template('tambahPinjam.html', container = [kodeBuku, nim])

# Routing website ke halaman Hapus Peminjam
# Tidak me-render template apapun, dan langsung menjalankan fungsi hapus peminjam
# Apabila sukses / gagal meghapus peminjam dalam database akan menampilkan pesan dan redirect ke halaman Daftar Peminjam
@app.route('/hapusPinjam/<kodePinjam>', methods = ['GET', 'POST'])
def hapusPinjam(kodePinjam):
    try:
        # Menghubungkan ke database dan melakukan DELETE pada tabel pinjam
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tpinjam WHERE kodePinjam=%s', (kodePinjam,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Peminjaman berhasil dihapus!')
        return redirect('/pinjam')

    except (MySQLdb.Error) as err:
        # Menangkap error dan menampilkan pesan gagal
        flash('Peminjaman gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/pinjam')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# [C R] KEMBALI
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Routing website ke halaman Daftar Pengembali
# Menampilkan halaman Daftar Pengembali, lengkap dengan data - data pengembali
@app.route('/kembali')
def kembali():
    # Menghubungkan ke database dan melakukan SELECT pada tabel pinjam
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tkembali')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarKembali.html', container = hasil)

# Routing website ke halaman Tambah Pengembali
# Menampilkan halaman tambah pengembali
# Apabila form pada halaman tambah pengembali melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan percobaan menambahkan pengembali dalam tabel kembali.
# Apabila sukses / gagal menambahkan pengembali dalam database akan menampilkan pesan dan redirect ke halaman Daftar Pengembali
@app.route('/tambahPinjam', methods = ['GET', 'POST'])
@app.route('/tambahKembali', methods = ['GET', 'POST'])
def tambahKembali():
    if (request.method == 'POST'):
        try:
            # Mengambil input dari form
            kembali = request.form
            kodeKembali = kembali['kodeKembali']
            kodeBuku = kembali['kodebuku']
            nim = kembali['NIM']
            tanggalKembali = kembali['tanggalKembali']

            # Menghubungkan ke database dan melakukan SELECT dari tabel buku
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT stok FROM tbuku WHERE kodeBuku=%s", (kodeBuku,))
            stok = cursor.fetchall()
            
            # Melakukan INSERT data pengembali ke tabel kembali
            # Melakukan UPDATE jumlah stok pada tabel buku
            cursor.execute("INSERT INTO tkembali(kodeKembali, kodeBuku, NIM, tglKembali) VALUES(%s, %s, %s, %s)", (kodeKembali, kodeBuku, nim, tanggalKembali))
            cursor.execute('UPDATE tbuku SET stok=%s WHERE kodeBuku=%s', (stok[0][0] + 1, kodeBuku))
            mysql.connection.commit()
            cursor.close()

            flash('Berhasil mengembalikan buku!')
            return redirect('/kembali')
        
        except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
            flash('Gagal mengembalikan buku! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/kembali')

    # Menghubungkan ke database dan melakukan SELECT dari tabel buku
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tbuku')
    kodeBuku = cursor.fetchall()
    
    # Menghubungkan ke database dan melakukan SELECT dari tabel anggota
    cursor.execute('SELECT * FROM tanggota')
    nim = cursor.fetchall()
    cursor.close()

    return render_template('tambahKembali.html', container = [kodeBuku, nim])

# Routing website ke halaman Hapus Pengembali
# Tidak me-render template apapun, dan langsung menjalankan fungsi hapus pengembali
# Apabila sukses / gagal meghapus pengembali dalam database akan menampilkan pesan dan redirect ke halaman Daftar Pengembali
@app.route('/hapusKembali/<kodeKembali>', methods = ['GET', 'POST'])
def hapusKembali(kodeKembali):
    try:
        # Menghubungkan ke database dan melakukan DELETE pada tabel kembali
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tkembali WHERE kodeKembali=%s', (kodeKembali,))
        mysql.connection.commit()
        cursor.close()
        
        flash('Pengembalian berhasil dihapus!')
        return redirect('/kembali')

    except (MySQLdb.Error) as err:
        # Menangkap error dan menampilkan pesan gagal
        flash('Pengembalian gagal dihapus! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/kembali')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# [CRUD] Anggota
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Routing website ke halaman Daftar Anggota
# Mengambil data dari database tabel anggota lalu menampilkannya di halaman Daftar Anggota
@app.route('/anggota', methods = ['GET', 'POST'])
def daftarAnggota():
    
    #  Menghubungkan ke database dan melakukan SELECT pada tabel anggota
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tanggota')
    hasil = cursor.fetchall()
    
    cursor.close()
    return render_template('daftarAnggota.html', container = hasil)

# Routing website ke halaman Tambah Anggota
# Menampilkan halaman tambah anggota
# Apabila form pada halaman tambah anggota melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan percobaan menambahkan anggota dalam tabel anggota.
# Apabila sukses / gagal menambahkan anggota dalam database akan menampilkan pesan dan redirect ke halaman Daftar Anggota
@app.route('/tambahAnggota', methods=['GET', 'POST'])
def tambahAnggota():
    if (request.method == 'POST'):
        try:
            # Menangambil input form
            anggota = request.form
            nim = anggota['NIM']
            namaMhs = anggota['namamahasiswa']
            jurusan = anggota['jurusan']

            # Menghubungkan ke database dan melakukan INSERT pada tabel anggota
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tanggota(NIM, namaMhs, jurusan) VALUES(%s, %s, %s)', (nim, namaMhs, jurusan))
            mysql.connection.commit()
            cursor.close()
            
            flash('Berhasil menambahkan anggota!')
            return redirect('/anggota')
        
        except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
            flash('Gagal menambahkan anggota! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/anggota')

    return render_template('tambahAnggota.html')

# Routing website ke halaman Hapus Anggota
# Tidak me-render template apapun, dan langsung menjalankan fungsi hapus anggota
# Apabila sukses / gagal menghapus anggota dalam database akan menampilkan pesan dan redirect ke halaman Daftar Anggota
@app.route('/hapusAnggota/<NIM>', methods = ['GET', 'POST'])
def hapusAnggota(NIM):
    try:
        # Menghubungkan ke database dan melakukan DELETE pada tabel anggota
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tanggota WHERE NIM=%s', (NIM,))
        mysql.connection.commit()
        cursor.close()

        flash('Berhasil menghapus anggota!')
        return redirect('/anggota')

    except (MySQLdb.Error) as err:
        # Menangkap error dan menampilkan pesan error
        flash('Gagal menghapus anggota! %d: %s' % (err.args[0], err.args[1]))
        return redirect('/anggota')

# Routing website ke halaman Edit Anggota
# Menampilkan halaman Edit Anggota, lengkap dengan data anggota yang akan di edit
# Apabila form pada halaman edit anggota melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan percobaan mengedit anggota dalam tabel anggota.
# Apabila sukses / gagal mengedit anggota dalam database akan menampilkan pesan dan redirect ke halaman Daftar Anggota
@app.route('/editAnggota/<NIM>', methods = ['GET', 'POST'])
def editAnggota(NIM):
    if (request.method == 'POST'):
        try:
            # Mengambil input form
            anggota = request.form
            nim = anggota['NIM']
            namaMhs = anggota['namamahasiswa']
            jurusan = anggota['jurusan']

            # Menghubungkan ke database dan melakukan UPDATE pada tabel anggota
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tanggota SET namaMhs=%s, jurusan=%s WHERE NIM=%s', (namaMhs, jurusan, nim))
            mysql.connection.commit()
            cursor.close()
            
            flash('Berhasil mengedit anggota!')
            return redirect('/anggota')

        except (MySQLdb.Error) as err:
            # Menangkap error dan menampilkan pesan gagal
            flash('Gagal mengedit anggota! %d: %s' % (err.args[0], err.args[1]))
            return redirect('/anggota')
    
    # Menghubungkan ke database dan melakukan SELECT pada tabel anggota
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tanggota WHERE NIM=%s', (NIM,))
    hasil = cursor.fetchall()

    cursor.close()
    return render_template('editAnggota.html', container = hasil)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Routing website ke halaman Login
# Menampilkan halaman Login
# Apabila form pada halaman Login melakukan POST maka akan mengambil data yang dikirim dari form untuk melakukan verifikasi Login dengan tabel username
# Apabila sukses / gagal melakukan login akan menerima pesan
# Sukses diarahkan ke halaman daftar buku
# Gagal diarahkan ke halaman login untuk melakukan login kembali
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "POST"):
        # Mengambil input form login
        datalogin = request.form
        username = datalogin['username']
        password = datalogin['password']

        # Melakukan SELECT untuk memeriksa apakah username dan password ada dalam database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))
        hasil = cursor.fetchall()
        
        if (len(hasil) > 0):
            # Apabila terdapat data username dan password, verifikasi berhasil
            flash('Login Berhasil! Welcome %s!' % username)
            return redirect('/daftarBuku')
        else:
            # Apabila tidak ada data username dan password, verfikasi gagal
            flash('Username & Password salah!')
            return render_template('login.html')

    return render_template('login.html')
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug = True)



# ------------------------------------------------------------------------------------------------------------------------------------------------------
# Dibuat oleh Kelompok 3 : 
# Ferry Gunawan     [ 32190098 ]
# Kelvin Chandra    [ 32190041 ]
# Kevin Kusuma      [ 32190048 ]
# ------------------------------------------------------------------------------------------------------------------------------------------------------