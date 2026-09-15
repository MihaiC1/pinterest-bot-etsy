from playwright.sync_api import sync_playwright
import time

# Aici vom salva datele sesiunii (cookies)
SESSION_FILE = "pinterest_auth.json"

with sync_playwright() as p:
    # Deschidem un browser complet normal, fără automatizări pe el
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigăm la pagina principală
    page.goto("https://www.pinterest.com/")
    
    print("--------------------------------------------------")
    print("Browser-ul s-a deschis.")
    print("1. Loghează-te manual pe Pinterest (prin Google sau email).")
    print("2. Așteaptă să ajungi pe pagina principală a contului tău.")
    print("3. Când ai terminat și ești logat, apasă ENTER în acest terminal.")
    print("--------------------------------------------------")
    
    input("Apasă ENTER după ce te-ai logat complet...")

    # Salvăm sesiunea într-un fișier local
    context.storage_state(path=SESSION_FILE)
    print(f"Sesiunea a fost salvată cu succes în {SESSION_FILE}!")
    
    browser.close()