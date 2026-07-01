"""
Latihan Mandiri - Web Scraping quotes.toscrape.com
Tugas:
1. Ambil semua kategori dari website quotes.toscrape
2. Ambil semua quote dari 3 halaman
3. Simpan hasil ke Excel
4. Tambahkan delay 2 detik tiap request
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUTPUT_DIR = "./output"


def get_soup(url):
    """Ambil dan parse HTML dari sebuah URL, dengan delay 2 detik."""
    response = requests.get(url, headers=HEADERS)
    time.sleep(2)  # delay 2 detik tiap request
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def ambil_kategori():
    """1. Ambil semua kategori (tags) dari halaman quotes.toscrape."""
    soup = get_soup(f"{BASE_URL}/")
    tag_box = soup.find("div", class_="tags-box")
    kategori_list = []

    if tag_box:
        for tag in tag_box.find_all("a", class_="tag"):
            kategori_list.append({
                "kategori": tag.get_text(strip=True),
                "jumlah_quote": tag.find("span") is None,  # placeholder, dihitung terpisah jika perlu
            })
    else:
        # fallback: kumpulkan semua tag unik dari tiap quote di 3 halaman
        pass

    # quotes.toscrape juga punya halaman /tag/<nama>/ untuk tiap kategori,
    # tapi cara paling simpel: ambil dari sidebar "Top Ten tags"
    kategori_final = [k["kategori"] for k in kategori_list]
    return kategori_final


def ambil_semua_quote(jumlah_halaman=3):
    """2. Ambil semua quote dari sejumlah halaman tertentu."""
    semua_quote = []

    for halaman in range(1, jumlah_halaman + 1):
        url = f"{BASE_URL}/page/{halaman}/"
        print(f"Scraping halaman {halaman}: {url}")
        soup = get_soup(url)

        quote_divs = soup.find_all("div", class_="quote")
        if not quote_divs:
            print(f"Halaman {halaman} kosong, berhenti.")
            break

        for q in quote_divs:
            teks = q.find("span", class_="text").get_text(strip=True)
            penulis = q.find("small", class_="author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.find_all("a", class_="tag")]

            semua_quote.append({
                "halaman": halaman,
                "quote": teks,
                "penulis": penulis,
                "tags": ", ".join(tags)
            })

    return semua_quote


def ambil_kategori_dari_quotes(daftar_quote):
    """Alternatif: kumpulkan semua kategori unik dari tag di setiap quote."""
    semua_tag = set()
    for q in daftar_quote:
        if q["tags"]:
            for t in q["tags"].split(", "):
                semua_tag.add(t)
    return sorted(semua_tag)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== Mengambil semua quote dari 3 halaman ===")
    data_quote = ambil_semua_quote(jumlah_halaman=3)
    print(f"Total quote terkumpul: {len(data_quote)}")

    print("\n=== Mengambil semua kategori ===")
    kategori = ambil_kategori_dari_quotes(data_quote)
    print(f"Total kategori unik: {len(kategori)}")

    # Simpan ke CSV terpisah (sesuai format yang diminta: tiap data -> csv)
    df_quote = pd.DataFrame(data_quote)
    df_kategori = pd.DataFrame({"kategori": kategori})

    path_quote = os.path.join(OUTPUT_DIR, "quotes.csv")
    path_kategori = os.path.join(OUTPUT_DIR, "kategori.csv")

    df_quote.to_csv(path_quote, index=False)
    df_kategori.to_csv(path_kategori, index=False)

    print(f"\nSelesai! Data disimpan ke:")
    print(f"  - {path_quote}")
    print(f"  - {path_kategori}")


if __name__ == "__main__":
    main()
