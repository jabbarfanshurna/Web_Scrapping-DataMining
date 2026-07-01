"""
Mini Project - Web Scraping scrapethissite.com/pages/
Scrape 3 halaman, masing-masing disimpan ke file CSV terpisah:
1. Countries of the World: A Simple Example
2. Hockey Teams: Forms, Searching and Pagination
3. Oscar Winning Films: AJAX and Javascript
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os

BASE_URL = "https://www.scrapethissite.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUTPUT_DIR = "./output"


def get_soup(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    time.sleep(2)  # sopan santun ke server
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# -------------------------------------------------------------------
# 1. Countries of the World: A Simple Example
# -------------------------------------------------------------------
def scrape_countries():
    url = f"{BASE_URL}/pages/simple/"
    print(f"Scraping: {url}")
    soup = get_soup(url)

    data = []
    for row in soup.find_all("div", class_="country"):
        nama = row.find("h3", class_="country-name").get_text(strip=True)
        ibukota = row.find("span", class_="country-capital").get_text(strip=True)
        populasi = row.find("span", class_="country-population").get_text(strip=True)
        luas = row.find("span", class_="country-area").get_text(strip=True)

        data.append({
            "negara": nama,
            "ibukota": ibukota,
            "populasi": populasi,
            "luas_km2": luas
        })

    df = pd.DataFrame(data)
    path = f"{OUTPUT_DIR}/countries.csv"
    df.to_csv(path, index=False)
    print(f"  -> {len(df)} baris disimpan ke {path}")
    return df


# -------------------------------------------------------------------
# 2. Hockey Teams: Forms, Searching and Pagination
# -------------------------------------------------------------------
def scrape_hockey():
    url = f"{BASE_URL}/pages/forms/"
    all_data = []
    halaman = 1
    max_halaman = 30  # batas aman, situs ini punya 24 halaman data

    while halaman <= max_halaman:
        print(f"Scraping hockey halaman {halaman}: {url} (page_num={halaman})")
        soup = get_soup(url, params={"page_num": halaman})

        rows = soup.find_all("tr", class_="team")
        if not rows:
            print(f"Halaman {halaman} kosong, berhenti.")
            break

        for row in rows:
            team_name = row.find("td", class_="name").get_text(strip=True)
            year = row.find("td", class_="year").get_text(strip=True)
            wins = row.find("td", class_="wins").get_text(strip=True)
            losses = row.find("td", class_="losses").get_text(strip=True)
            ot_losses_tag = row.find("td", class_="ot-losses")
            ot_losses = ot_losses_tag.get_text(strip=True) if ot_losses_tag else ""
            pct = row.find("td", class_="pct").get_text(strip=True)
            gf = row.find("td", class_="gf").get_text(strip=True)
            ga = row.find("td", class_="ga").get_text(strip=True)
            diff = row.find("td", class_="diff").get_text(strip=True)

            all_data.append({
                "team_name": team_name,
                "year": year,
                "wins": wins,
                "losses": losses,
                "ot_losses": ot_losses,
                "win_pct": pct,
                "goals_for": gf,
                "goals_against": ga,
                "diff": diff
            })

        halaman += 1

    df = pd.DataFrame(all_data)
    path = f"{OUTPUT_DIR}/hockey_teams.csv"
    df.to_csv(path, index=False)
    print(f"  -> {len(df)} baris disimpan ke {path}")
    return df


# -------------------------------------------------------------------
# 3. Oscar Winning Films: AJAX and Javascript
# -------------------------------------------------------------------
def scrape_oscars():
    """
    Halaman ini memuat data lewat AJAX. Request-nya ke URL yang sama
    dengan tambahan query string ?ajax=true&year=<tahun>, mengembalikan JSON.
    """
    ajax_url = f"{BASE_URL}/pages/ajax-javascript/"
    tahun_list = [str(y) for y in range(2010, 2016)]  # situs ini menyediakan data 2010-2015

    all_data = []
    for tahun in tahun_list:
        print(f"  Mengambil data JSON tahun {tahun}")
        resp = requests.get(ajax_url, headers=HEADERS, params={"ajax": "true", "year": tahun})
        time.sleep(2)

        if resp.status_code != 200:
            print(f"  Gagal ambil tahun {tahun} (status {resp.status_code})")
            continue

        try:
            films = resp.json()
        except json.JSONDecodeError:
            print(f"  Response tahun {tahun} bukan JSON valid, dilewati.")
            continue

        for film in films:
            all_data.append({
                "tahun": tahun,
                "judul": film.get("title", ""),
                "nominasi": film.get("nominations", ""),
                "menang_best_picture": "Ya" if film.get("best_picture") else "Tidak",
                "poster_url": film.get("poster", "")
            })

    df = pd.DataFrame(all_data)
    path = f"{OUTPUT_DIR}/oscar_films.csv"
    df.to_csv(path, index=False)
    print(f"  -> {len(df)} baris disimpan ke {path}")
    return df


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=== 1. Countries of the World ===")
    scrape_countries()

    print("\n=== 2. Hockey Teams ===")
    scrape_hockey()

    print("\n=== 3. Oscar Winning Films ===")
    scrape_oscars()

    print("\nSemua data selesai discrape dan disimpan sebagai CSV.")


if __name__ == "__main__":
    main()
