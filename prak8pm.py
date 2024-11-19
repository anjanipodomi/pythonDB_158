# Import library sqlite3 untuk mengelola database SQLite
import sqlite3
# Import elemen GUI dari tkinter
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')    #Menghubungkan atau membuat file database
    cursor = conn.cursor()                      #Membuat objek cursor untuk eksekusi query
    cursor.execute('''                          
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()                               #Menyimpan perubahan ke database
    conn.close()                                #Menutup koneksi database

#Fungsi untuk mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa") #Mengambil semua data
    rows = cursor.fetchall()                    #Mengembalikan data dalam bentuk list
    conn.close()
    return rows                                 #Mengembalikan hasil ke pemanggil

#Fungsi untuk menyimpan data ke tabel
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data di tabel
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

#Fungsi untuk menghapus data dari tabel
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

#Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran" #Biologi tertinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik" #Fisika tertinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa" #Bahasa inggris tertinggi
    else:
        return "Tidak Diketahui"    #Jika ada nilai yang sama

# Fungsi untuk menyimpan data baru ke database dari GUI
def submit():
    try:
        nama = nama_var.get()      #Ambil input nama
        biologi = int(biologi_var.get())       #Ambil input nilai biologi
        fisika = int(fisika_var.get())         #Ambil input nilai fisika
        inggris = int(inggris_var.get())       #Ambil input nilai bahasa Inggris

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)   #Hitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  #Simpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()      #Bersihkan input
        populate_table()    #Perbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")


# Fungsi untuk memperbarui data yang dipilih dari tabel
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih dari tabel
def delete():
    try:
        if not selected_record_id.get():    #Memeriksa apakah ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())   #Ambil ID record yang dipilih
        delete_database(record_id)  #Hapus data berdasarkan ID
        messagebox.showinfo("Sukses", "Data berhasil dihapus!") #Tampilkan pesan sukses
        clear_inputs()      #Bersihkan input
        populate_table()    #Perbarui tabel setelah penghapusan
    except ValueError as e: #Tangani jika terjadi error dalam proses
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan input form
def clear_inputs():
    nama_var.set("")        #Kosongkan input nama
    biologi_var.set("")     #Kosongkan input nilai biologi
    fisika_var.set("")      #Kosongkan input nilai fisika
    inggris_var.set("")     #Kosongkan input nilai inggris
    selected_record_id.set("")  #Kosongkan ID record yang dipilih

# Fungsi untuk mengisi ulang data pada tabel
def populate_table():
    for row in tree.get_children():     #Menghapus semua data yang ada pada tabel
        tree.delete(row)
    for row in fetch_data():            #Ambil data dari database
        tree.insert('', 'end', values=row)  #Masukkan data ke tabel


# Fungsi untuk mengisi input form berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]     #Ambil item yang dipilih
        selected_row = tree.item(selected_item)['values']   #Ambil nilai dari item yang dipilih

        # Isi input form dengan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:      #Tangani jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!") #Tampilkan pesan error

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")   #Menentukan judul jendela

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  #Untuk menyimpan ID record yang dipilih

#Membuat label dan input field untuk Nama Siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

#Membuat label dan input field untuk Nilai Biologi
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

#Membuat label dan input field untuk Nilai Fisika
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

#Membuat label dan input field untuk Nilai Inggris
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

#Membuat tombol untuk menambahkan data
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
#Membuat tombol untuk memperbarui data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
#Membuat tombol untuk menghapus data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

#Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())    #Menampilkan nama kolom dengan huruf kapital
    tree.column(col, anchor='center')           #Menyusun isi kolom di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  #Menempatkan tabel di jendela

#Mengikat klik pada tabel untuk mengisi input berdasarkan data yang dipilih
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

#Memuat data dari database ke tabel
populate_table()

#Menjalankan aplikasi Tkinter
root.mainloop()