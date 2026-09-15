import os
import pandas as pd
import requests
import base64
from datetime import datetime

# 1. Preia token-ul setat în GitHub Actions
ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
BOARD_ID = "ID_UL_PANOULUI_TAU" # <- PUNE AICI ID-UL BOARD-ULUI TĂU

if not ACCESS_TOKEN:
    print("Eroare: Token-ul nu a fost găsit în variabilele de mediu!")
    exit(1)

if BOARD_ID == "ID_UL_PANOULUI_TAU":
    print("Eroare: Nu ai setat BOARD_ID în script!")
    exit(1)

def posteaza_pin_api(imagine_path, titlu, descriere, link):
    url = "https://api.pinterest.com/v5/pins"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Codificăm imaginea în Base64 pentru a o trimite direct prin API
    with open(imagine_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    
    # Setăm tipul fișierului în funcție de extensie
    ext = imagine_path.split('.')[-1].lower()
    content_type = f"image/{ext}" if ext in ['jpeg', 'png'] else "image/jpeg"
    if ext == 'jpg': content_type = "image/jpeg"

    payload = {
        "board_id": BOARD_ID,
        "title": titlu,
        "description": descriere,
        "link": link,
        "media_source": {
            "source_type": "image_base64",
            "content_type": content_type,
            "data": encoded_string
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print(f"Postat cu succes prin API: {titlu}")
        with open("istoric.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Pin postat: {titlu}\n")
        return True
    else:
        print(f"Eroare la postare: {response.status_code}")
        print(response.json())
        return False

# 2. Citirea CSV-ului și execuția
try:
    df = pd.read_csv("date_postari.csv", sep="|")
    
    nepostate = df[df['postat'] == 0]
    
    if nepostate.empty:
        print("Toate imaginile au fost postate!")
    else:
        rand_curent = nepostate.iloc[0]
        imagine_curenta = os.path.join("imagini", rand_curent['imagine'])
        
        if not os.path.exists(imagine_curenta):
            print(f"Eroare: Imaginea {imagine_curenta} nu există în folder!")
            exit(1)
            
        succes = posteaza_pin_api(
            imagine_curenta, 
            rand_curent['titlu'], 
            rand_curent['descriere'], 
            rand_curent['link']
        )

        if succes:
            # Actualizăm CSV-ul, menținând separatorul |
            df.loc[df['imagine'] == rand_curent['imagine'], 'postat'] = 1
            df.to_csv("date_postari.csv", index=False, sep="|")
            
except Exception as e:
    print(f"Eroare generală: {e}")