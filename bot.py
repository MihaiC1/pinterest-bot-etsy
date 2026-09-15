import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime

SESSION_FILE = "pinterest_auth.json"

def posteaza_pin(imagine_path, titlu, descriere, link):
    with sync_playwright() as p:
        # Lansăm browserul folosind fișierul cu sesiunea salvată
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(storage_state=SESSION_FILE)
        page = context.new_page()

        # Sari complet peste login și mergi DIRECT la pagina de creare Pin!
        page.goto("https://www.pinterest.com/pin-creation-tool/")
        
        # Așteptăm să se încarce elementele esențiale din pagină
        page.wait_for_load_state("networkidle")
        time.sleep(4)
        # OPREȘTE SCRIPTUL PENTRU INSPECTARE DOM
        #page.pause()
        try:
            # 3. Încărcarea imaginii
            page.set_input_files("input[type='file']", imagine_path)
            time.sleep(2)

            # 4. Completarea datelor
            page.get_by_role("textbox", name="Titlu").fill(titlu)
            page.get_by_role("button", name="Descriere Descrie-ți Pinul").click()
            # Folosim tastatura virtuală pentru a scrie textul
            page.keyboard.type(descriere)

            page.get_by_role("textbox", name="Link").fill(link)
            time.sleep(1)

            page.mouse.click(10, 10)
            time.sleep(1)
            # 5. Publicarea (Apăsarea butonului de Save)
            page.get_by_role("button", name="Publică").click()
            # Așteptăm câteva secunde să se trimită datele la server
            time.sleep(7)
            print(f"Postat cu succes: {titlu}")
        
            # Scrie în jurnal
            with open("istoric.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Pin postat: {titlu}\n")

        except Exception as e:
            print(f"A apărut o problemă la completarea datelor. Eroare: {e}")
            
        finally:
            browser.close()

# ... (aici rămâne partea cu pandas care citește CSV-ul, la fel cum era înainte)
try:
    df = pd.read_csv("date_postari.csv", sep="|")
    
    nepostate = df[df['postat'] == 0]
    
    if nepostate.empty:
        print("Toate imaginile au fost postate!")
    else:
        rand_curent = nepostate.iloc[0]
        imagine_curenta = os.path.join("imagini", rand_curent['imagine'])
        
        posteaza_pin(
            imagine_curenta, 
            rand_curent['titlu'], 
            rand_curent['descriere'], 
            rand_curent['link']
        )

        # Actualizăm CSV-ul, adăugând sep="|"
        df.loc[df['imagine'] == rand_curent['imagine'], 'postat'] = 1
        df.to_csv("date_postari.csv", index=False, sep="|")
    
except Exception as e:
    print(f"Eroare generală: {e}")