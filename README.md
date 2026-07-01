# Web Scraping Project - Data Mining

Proyek ini merupakan implementasi web scraping menggunakan Python sebagai bagian dari tugas mata kuliah **Data Mining**. Data dikumpulkan dari dua website latihan, yaitu **quotes.toscrape.com** dan **scrapethissite.com**, kemudian diolah dan disimpan dalam format CSV untuk analisis lebih lanjut.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/BeautifulSoup4-HTML%20Parser-yellow" alt="BeautifulSoup">
  <img src="https://img.shields.io/badge/pandas-Data%20Analysis-150458?logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Status-Finished-brightgreen" alt="Status">
</p>

---

# Daftar Isi

- Gambaran Proyek
- Struktur Folder
- Teknologi yang Digunakan
- Instalasi
- Menjalankan Program
- Penjelasan Implementasi
- Output Data
- Praktik Scraping yang Baik
- Author

---

# Gambaran Proyek

Repository ini terdiri dari dua program scraping yang memiliki tujuan berbeda.

| File | Website | Fitur Utama |
|------|----------|-------------|
| `latihan_mandiri.py` | quotes.toscrape.com | Mengambil quote dari beberapa halaman beserta tag unik |
| `mini_project.py` | scrapethissite.com | Mengambil data Countries, Hockey Teams, dan Oscar Films |

Seluruh hasil scraping akan diekspor secara otomatis ke dalam file CSV sehingga dapat langsung digunakan untuk analisis data.

---

# Struktur Folder

```text
WebScraping/
│
├── latihan_mandiri.py
├── mini_project.py
├── output/
│   ├── quotes.csv
│   ├── kategori.csv
│   ├── countries.csv
│   ├── hockey_teams.csv
│   └── oscar_films.csv
└── README.md
```

---

# Teknologi yang Digunakan

Proyek ini dibangun menggunakan beberapa library Python berikut.

- Python 3.13
- requests
- BeautifulSoup4
- pandas

---

# Instalasi

Clone repository terlebih dahulu.

```bash
git clone https://github.com/username/web-scraping-project.git
```

Masuk ke folder project.

```bash
cd web-scraping-project
```

Install seluruh dependency.

```bash
pip install requests beautifulsoup4 pandas
```

---

# Menjalankan Program

Scraper dapat dijalankan secara terpisah.

```bash
python latihan_mandiri.py
```

atau

```bash
python mini_project.py
```

Setelah proses selesai, seluruh hasil akan tersimpan pada folder **output**.

---

# Penjelasan Implementasi

### Multi-page Scraping

Pada website Quotes to Scrape, program akan mengunjungi beberapa halaman secara berurutan hingga seluruh quote yang dibutuhkan berhasil dikumpulkan.

### Pengumpulan Tag

Selain mengambil isi quote dan penulisnya, scraper juga mengumpulkan seluruh tag yang muncul. Data tag kemudian diolah menjadi daftar kategori tanpa duplikasi.

### Pagination

Untuk halaman Hockey Teams, perpindahan halaman dilakukan menggunakan parameter `page_num`. Proses scraping akan berhenti ketika halaman yang diminta sudah tidak lagi memiliki data.

### Pengambilan Data AJAX

Data Oscar Winning Films tidak tersedia secara langsung pada HTML utama. Oleh karena itu scraper melakukan request ke endpoint AJAX (`?ajax=true&year=<tahun>`) yang mengembalikan data dalam format JSON sebelum diproses menjadi tabel.

### Delay Request

Program memberikan jeda sekitar dua detik di setiap request sebagai bentuk penerapan scraping yang lebih ramah terhadap server.

---

# Output Data

| Dataset | Total Data |
|----------|-----------:|
| Quotes | 30 |
| Tag/Kategori | 60 |
| Countries | 250 |
| Hockey Teams | 582 |
| Oscar Winning Films | 87 |

Semua dataset disimpan dalam format **CSV** sehingga mudah digunakan kembali untuk proses analisis maupun visualisasi.

---

# Praktik Scraping

Website yang digunakan pada proyek ini merupakan website latihan yang memang disediakan untuk belajar web scraping.

Beberapa praktik yang diterapkan pada project ini antara lain:

- memberikan jeda antar request;
- menghindari request yang terlalu cepat;
- memanfaatkan endpoint JSON ketika tersedia;
- melakukan scraping hanya pada data publik.

Pendekatan tersebut dapat dijadikan dasar ketika melakukan scraping pada website lain dengan tetap memperhatikan aturan penggunaan dan file `robots.txt` yang dimiliki setiap situs.

---

# Author

**Abd Jabbar Fanshurna Musra**

NIM H071241088  
Program Studi Sistem Informasi  
Universitas Hasanuddin

Tugas Individu Mata Kuliah **Data Mining**
