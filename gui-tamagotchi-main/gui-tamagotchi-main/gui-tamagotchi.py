from sys import exit
import datetime as dt
import json
import os
from nicegui import ui, app
import asyncio
from PIL import Image

#import sys => sys.exit()

zprava = None
spritesheet = Image.open("cat.png")
obrazek = None

kocka = {
    # "jmeno": "Aladin",
    # "hlad": 50,
    # "zizen": 0,
    # "barva": "fialová",
    # "zivoty": 100,
    # "cisota": 100,
    # "energie": 90,
    # "zije": True,
    # "vek": 0,
    # "nestastnost": False,
    # "nemoc": False,
}
default_kocka = {
    "jmeno": "Aladin",
    "hlad": 50,
    "zizen": 0,
    "barva": "fialová",
    "zivoty": 100,
    "cisota": 100,
    "energie": 90,
    "zije": True,
    "vek": 0,
    "nestastnost": False,
    "nemoc": False,
}

# with open("tamagotchi.json", "w", encoding="utf-8") as f:
#     json.dump(kocka, f, ensure_ascii=False, indent=4)

puvodni_cas = dt.datetime.now()

def save():
    global kocka
    with open("tamagotchi.json", "w", encoding="utf-8") as f:
        json.dump(kocka, f, ensure_ascii=False, indent=4)

def reset():
    global kocka, default_kocka
    kocka = default_kocka
    save()

def load():
    # TODO reset hry, kontrola existence tamagotchi.json
    global kocka, default_kocka

    if os.path.isfile("tamagotchi.json"):
        with open("tamagotchi.json", "r", encoding="utf-8") as f:
            kocka = json.load(f)
    else:
        kocka = default_kocka
        save()


def krmeni():
    kocka["hlad"] -= 10
    print(f"{kocka["jmeno"]} vypadá šťastně. \nHlad je {kocka["hlad"]}")
    zprava.text = (f"{kocka["jmeno"]} vypadá šťastně.")
    obrazek.source = strih(2, 65)
    ui.notify(f"Hlad je {kocka["hlad"]}")
    zkontroluj_status()


def prochazka():
    kocka["hlad"] += 10
    kocka["zizen"] += 10
    kocka["energie"] -= 10
    kocka["cisota"] -= 15
    zprava.text = (f"{kocka["jmeno"]} je velmi šťastný.")
    obrazek.source = strih(0, 5)
    ui.notify(f"Hlad je {kocka["hlad"]}. Žízeň je {kocka["zizen"]}. Energie je {kocka["energie"]}. Čistota je {kocka["cisota"]}")
    zkontroluj_status()


def koupel():
    kocka["cisota"] += 10
    zprava.text = (f"{kocka["jmeno"]} je čistý.")
    obrazek.source = strih(2, 12)
    zkontroluj_status()


def hra():
    kocka["hlad"] += 10
    kocka["zizen"] += 10
    kocka["energie"] -= 10
    kocka["cisota"] += 5
    kocka["nestastnost"] = False
    print(f"{kocka["jmeno"]} vypadá šťastně. \nHlad je {kocka["hlad"]}. \nŽízeň je {kocka["zizen"]}. \nEnergie je {kocka["energie"]}")
    zprava.text = (f"{kocka["jmeno"]} je velmi šťastný.")
    obrazek.source = strih(0, 8)
    ui.notify(f"Hlad je {kocka["hlad"]}. \nŽízeň je {kocka["zizen"]}. \nEnergie je {kocka["energie"]}")
    zkontroluj_status()


async def spanek():
    kocka["energie"] = 100
    print(f"Zzz...zzz... \n{kocka['jmeno']} je odpočatý. Energie {kocka['jmeno']} je {kocka['energie']}")
    obrazek.source = strih(0, 49)
    zprava.text = (f"Zzz...zzz...")
    await asyncio.sleep(1)
    zprava.text = (f"\n{kocka['jmeno']} je odpočatý.")
    ui.notify(f"Energie {kocka['jmeno']} je {kocka['energie']}")
    zkontroluj_status()


def napit():
    kocka["zizen"] -= 10
    print(f"{kocka['jmeno']} se napil. \nŽízeň je {kocka['zizen']}")
    zprava.text = (f"{kocka['jmeno']} se napil.")
    obrazek.source = strih(3, 36)
    ui.notify(f"Žízeň je {kocka['zizen']}")
    zkontroluj_status()


def hladoveni():
    global puvodni_cas

    ted = dt.datetime.now()
    
    if ted > puvodni_cas +dt.timedelta(seconds=10):
        kocka["hlad"] += 10
        ui.notify(f"{kocka["jmeno"]} začína mít hlad")
        puvodni_cas = ted #nahradit puvodni cas s casem ted

def starnuti():
    global puvodni_cas

    ted = dt.datetime.now()

    if ted > puvodni_cas +dt.timedelta(hours=1):
        kocka["vek"] += 1
        ui.notify(f"{kocka["jmeno"]} má narozeniny!")
        puvodni_cas = ted

def zkontroluj_status():
    if kocka["hlad"] > 120 or kocka["hlad"] < -20:
        kocka["zivoty"] -= 10

    if kocka["zizen"] > 100 or kocka["zizen"] < -30:
        kocka["zivoty"] -= 10

    if kocka["energie"] < -20:
        kocka["zivoty"] -= 10

    if kocka["cisota"] < -20:
        kocka["nestastnost"] -= True

    if kocka["zivoty"] <= 0:
        kocka["zije"] = False
        print(f"{kocka["jmeno"]} umřel.")
        app.shutdown()
        exit()
    hladoveni()
    starnuti()
    save()

def vypis_status():
    print(f"""
        Věk je: {kocka['vek']}
        Hlad je: {kocka['hlad']}
        Žízeň je: {kocka['zizen']}
        Energie je: {kocka['energie']}
        Zdraví je: {kocka['zivoty']}
        {kocka['jmeno']} je {"Šťastný" if kocka['nestastnost'] == False else "Nešťastný"}
    """)
    zprava.text = (f"""
        Věk je: {kocka['vek']}
        Hlad je: {kocka['hlad']}
        Žízeň je: {kocka['zizen']}
        Energie je: {kocka['energie']}
        Zdraví je: {kocka['zivoty']}
        {kocka['jmeno']} je {"Šťastný" if kocka['nestastnost'] == False else "Nešťastný"}
    """)
    obrazek.source = strih(0, 1)


def exit():
    save()
    app.shutdown

def strih(x, y):
    x = x * 64
    y = y * 64
    return spritesheet.crop((x, y, x + 64, y + 64))

def main():
    global zprava, obrazek

    tlacitka = {
        "Krmení": krmeni,
        "Napít": napit,
        "Hra": hra,
        "Procházka": prochazka,
        "Koupel": koupel,
        "Spánek": spanek,

    }

    tlacitka2 = {
        "Status": vypis_status,
        "Exit": exit,
        "Reset": reset
    }

    load()

    with ui.element("div").classes("w-full h-screen flex items-center justify-center flex-col gap-5"):
        # spritesheet = Image.open("cat.png")
        obrazek = ui.image(strih(0, 1)).classes("h-32 w-32")
        zprava = ui.label("Vítej!")
        with ui.grid(columns=3, rows=2):
            for jmeno, funkce in tlacitka.items():
                ui.button(jmeno, on_click=funkce).props("color=amber-200 text-color=emerald-600 rounded")
            for jmeno, funkce in tlacitka2.items():
                ui.button(jmeno, on_click=funkce).props("color=red-400 text-color=black rounded")

    # print("Vítej!")
    print("""
        /\\_/\\  
       ( O.O )
      (  v v  )
        """)

    # print(f"""Pro ukončení napiš konec. 
    #     \nPro nakrmení {kocka["jmeno"]} stiskni k. 
    #     \nPro napití stiskni z. 
    #     \nPro hraní s {kocka["jmeno"]} stiskni h. 
    #     \nPro spánek stiskni s. 
    #     \nPro reset napiš reset""")

    # uziv_input = input()

    # match uziv_input.lower():
    #     case "konec":
    #         print("Ukončení programu... bye (>w<)!")
    #     case "v":
    #         vypis_status()
    #     case "reset":
    #         reset()
    #     case _:
    #         print("Neplatná klávesa")
    
    ui.run(native=True)

    # hladoveni()
    # starnuti()
    # save()
    # zkontroluj_status()

ui.query('body').style("background-color: lightblue")

main()

