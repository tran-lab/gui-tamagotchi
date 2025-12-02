from sys import exit
import datetime as dt
import json
import os
from nicegui import ui

#import sys => sys.exit()

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

def hra():
    kocka["hlad"] += 10
    kocka["zizen"] += 10
    kocka["energie"] -= 10
    kocka["nestastnost"] = False
    print(f"{kocka["jmeno"]} vypadá šťastně. \nHlad je {kocka["hlad"]}. \nŽízeň je {kocka["zizen"]}. \nEnergie je {kocka["energie"]}")

def spanek():
    kocka["energie"] = 100
    print(f"Zzz...zzz... \n{kocka['jmeno']} je odpočatý. Energie {kocka['jmeno']} je {kocka['energie']}")

def napit():
    kocka["zizen"] -= 10
    print(f"{kocka['jmeno']} se napil. \nŽízeň je {kocka['zizen']}")

def hladoveni():
    global puvodni_cas

    ted = dt.datetime.now()
    
    if ted > puvodni_cas +dt.timedelta(seconds=10):
        kocka["hlad"] += 10
        print(f"{kocka["jmeno"]} začína mít hlad")
        puvodni_cas = ted #nahradit puvodni cas s casem ted

def starnuti():
    global puvodni_cas

    ted = dt.datetime.now()

    if ted > puvodni_cas +dt.timedelta(hours=1):
        kocka["vek"] += 1
        print(f"{kocka["jmeno"]} má narozeniny!")
        puvodni_cas = ted

def zkontroluj_status():
    if kocka["hlad"] > 120 or kocka["hlad"] < -20:
        kocka["zivoty"] -= 10

    if kocka["zizen"] > 100 or kocka["zizen"] < -30:
        kocka["zivoty"] -= 10

    if kocka["energie"] < -20:
        kocka["zivoty"] -= 10

    if kocka["zivoty"] <= 0:
        kocka["zije"] = False
        print(f"{kocka["jmeno"]} umřel.")
        exit()

def vypis_status():
    print(f"""
        Věk je: {kocka['vek']}
        Hlad je: {kocka['hlad']}
        Žízeň je: {kocka['zizen']}
        Energie je: {kocka['energie']}
        Zdraví je: {kocka['zivoty']}
        {kocka['jmeno']} je {"Šťastný" if kocka['nestastnost'] == False else "Nešťastný"}
    """)

def main():

    tlacitka = {
        "Krmení": krmeni,
        "Hra": hra,
        "Spánek": spanek,
        "Napít": napit,

    }

    load()

    with ui.element("div").classes("w-full h-screen flex items-center justify-center flex-col gap-5"):
        ui.label("Vítej!")
        with ui.grid(columns=5):
            for jmeno, funkce in tlacitka.items():
                ui.button(jmeno, on_click=funkce)

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
    hladoveni()
    starnuti()
    save()
    zkontroluj_status()

    ui.run(native=True)

main()