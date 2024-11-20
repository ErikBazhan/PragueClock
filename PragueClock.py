import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime, timedelta
import math
import time
from PIL import Image, ImageTk

# Funktion zur Erstellung des Hauptfensters
def erstelle_fenster():
    # Hauptfenster erstellen mit Yaru-Theme
    root = ThemedTk(theme="yaru")  
    root.title("Prager Uhr Simulation")  # Fenstertitel setzen
    root.geometry("1280x800")  # Fenstergröße setzen

    # Frame für die gesamte Anwendung
    haupt_frame = ttk.Frame(root, padding="10")
    haupt_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Ein eingerahmter Bereich für die Bedienelemente links
    elemente_frame = ttk.LabelFrame(haupt_frame, text="Bedienelemente", padding="10")
    elemente_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

    # Label-Widget Beispiel
    label = ttk.Label(elemente_frame, text="Willkommen zur Prager Uhr Simulation!")
    label.grid(row=0, column=0, padx=5, pady=5)

    # Combobox (Dropdown-Menü) für Stunden und Minuten erstellen
    auswahl = tk.StringVar()
    optionen = ["Stunden", "Minuten", "MittelEuropaischeZeit"]

    dropdown = ttk.Combobox(elemente_frame, textvariable=auswahl, values=optionen)
    dropdown.grid(row=1, column=0, padx=5, pady=5)
    dropdown.set("Wähle aus")

    # Label für die Ausgabe der Uhrzeit hinzufügen
    zeit_label = ttk.Label(elemente_frame, text="")
    zeit_label.grid(row=3, column=0, padx=5, pady=5)

    # Variablen zum Hervorheben der Zeiger
    highlight_stundenzeiger = tk.BooleanVar(value=False)
    highlight_minutenzeiger = tk.BooleanVar(value=False)
    highlight_mezzeiger = tk.BooleanVar(value=False)

    # Funktion zur Anzeige der Auswahl
    def auswahl_anzeigen():
        # Alle Zeiger zurücksetzen
        highlight_stundenzeiger.set(False)
        highlight_minutenzeiger.set(False)
        highlight_mezzeiger.set(False)

        if auswahl.get() == "Stunden":
            stunde = simulierte_zeit.hour
            zeit_label.config(text=f"Aktuelle Stunde: {stunde}")
            highlight_stundenzeiger.set(True)
        elif auswahl.get() == "Minuten":
            minute = simulierte_zeit.minute
            zeit_label.config(text=f"Aktuelle Minute: {minute}")
            highlight_minutenzeiger.set(True)
        elif auswahl.get() == "MittelEuropaischeZeit":
            mitteleuropaeische_zeit = simulierte_zeit.strftime("%H:%M:%S MEZ")
            zeit_label.config(text=f"MittelEuropäische Zeit: {mitteleuropaeische_zeit}")
            highlight_mezzeiger.set(True)
        else:
            zeit_label.config(text="Bitte eine Option auswählen")

    # Button hinzufügen, um die Auswahl zu bestätigen
    bestätigungs_button = ttk.Button(elemente_frame, text="Bestätigen", command=auswahl_anzeigen)
    bestätigungs_button.grid(row=2, column=0, padx=5, pady=5)

    # Button, um zur aktuellen Uhrzeit zurückzukehren
    def setze_aktuelle_zeit():
        nonlocal simulierte_zeit
        simulierte_zeit = datetime.now()  # Setzt die simulierte Zeit zurück auf die aktuelle Zeit
        geschwindigkeits_slider.set(1)  # Setzt die Geschwindigkeit zurück auf 1x

    aktuelle_zeit_button = ttk.Button(elemente_frame, text="Zur aktuellen Uhrzeit", command=setze_aktuelle_zeit)
    aktuelle_zeit_button.grid(row=6, column=0, padx=5, pady=5)

    # Button-Widget Beispiel
    button = ttk.Button(elemente_frame, text="Klick mich!", command=lambda: print("Button wurde geklickt!"))
    button.grid(row=4, column=0, padx=5, pady=5)

    # Ein eingerahmter Bereich für die Uhrzeitanzeige und Geschwindigkeitseinstellungen
    uhr_frame = ttk.LabelFrame(haupt_frame, text="Uhrzeitanzeige", padding="10")
    uhr_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.NE))

    # Label für die aktuelle Uhrzeit rechts im Fenster erstellen
    uhrzeit_label = ttk.Label(uhr_frame, font=("Helvetica", 16))
    uhrzeit_label.grid(row=0, column=0, padx=10, pady=10)

    # Canvas für das analoge Zifferblatt (Größe 700x700)
    canvas = tk.Canvas(uhr_frame, width=700, height=700, bg="white")
    canvas.grid(row=1, column=0, padx=10, pady=10)

    # Hintergrundbild laden und anpassen
    hintergrund_image = Image.open("Uhr_Backround_700x700.jpg")
    hintergrund_image = hintergrund_image.resize((700, 700), Image.LANCZOS)
    hintergrund_tk = ImageTk.PhotoImage(hintergrund_image)

    # Variable zur Simulation der Zeit
    simulierte_zeit = datetime.now()

    # Slidebar für Geschwindigkeitsanpassung erstellen
    geschwindigkeits_slider = tk.Scale(elemente_frame, from_=-1000, to=1000, orient=tk.HORIZONTAL, length=200)
    geschwindigkeits_slider.grid(row=7, column=0, padx=5, pady=10)
    geschwindigkeits_slider.set(1)

    # Funktion zur Aktualisierung der Uhrzeit
    def uhrzeit_aktualisieren():
        nonlocal simulierte_zeit
        geschwindigkeit = geschwindigkeits_slider.get()
        simulierte_zeit += timedelta(seconds=1 * geschwindigkeit)
        uhrzeit_label.config(text=f"Aktuelle Uhrzeit: {simulierte_zeit.strftime('%H:%M:%S')}")
        zeichne_zifferblatt()
        zeichne_boem_h_ziffernblatt()
        root.after(1000, uhrzeit_aktualisieren)

    # Funktion zum Zeichnen des Zifferblatts
    def zeichne_zifferblatt():
        canvas.delete("all")
        canvas.create_image(0, 0, image=hintergrund_tk, anchor=tk.NW)            

        stunden_winkel = math.radians((simulierte_zeit.hour % 12 + simulierte_zeit.minute / 60) * 30)
        stunden_x = 350 + 200 * math.sin(stunden_winkel)
        stunden_y = 350 - 200 * math.cos(stunden_winkel)
        canvas.create_line(350, 350, stunden_x, stunden_y, width=4, fill="white")

        minuten_winkel = math.radians(simulierte_zeit.minute * 6)
        minuten_x = 350 + 250 * math.sin(minuten_winkel)
        minuten_y = 350 - 250 * math.cos(minuten_winkel)
        canvas.create_line(350, 350, minuten_x, minuten_y, width=2, fill="white")

    # Hier beginnt Daniels Teil

        # Aktuelle Uhrzeit
        stunden = simulierte_zeit.hour % 12
        minuten = simulierte_zeit.minute
        
        # Winkel der Zeiger (360 Grad = 24 Stunden oder 60 Minuten/Sekunden)
        angle_stunden = (stunden + minuten/60 ) * 15  # Winkel zwischen 2 aufeinanderfolgenden Stunden = 15 Grad
        winkel_radians = math.radians(angle_stunden)

        # Den Stundenzeiger für die Mitteleuropaische Zeit zeichnen
        x, y = ZeigerRechnen(250, angle_stunden)  #Koordinaten für die Spitze des Dreiecks
        if highlight_mezzeiger.get():
            canvas.create_line(350, 350, x, y, width=7, fill='green', tags="Nadel")
        else:
            canvas.create_line(350, 350, x, y, width=5, fill="white")
        
        # Liste mit den Punkten, um den Dreieck zu zeichnen (handgeformtes Polygon)
        x_h, y_h = ZeigerRechnen(190, angle_stunden)
        gold_hand = [
            x, y,
            x_h - 20*math.cos(winkel_radians), y_h - 20*math.sin(winkel_radians),
            x_h + 20*math.cos(winkel_radians), y_h + 20*math.sin(winkel_radians),
        ]

        #Dreieck zeichnen
        canvas.create_polygon(gold_hand, fill="#FFD700", width=3, outline="black", tags="Nadel")
    
    # Funktion zum Berechnen der Position der Spitze der Nadel
    def ZeigerRechnen(laenge, winkel):
        winkel_radians = math.radians(winkel)
        x = 350 + laenge * math.sin(winkel_radians)
        y = 350 - laenge * math.cos(winkel_radians)
        return x, y

    # Hier endet Daniels Teil


    # Hier beginnt Dominick's Teil

    #Anmerkung: Code wird aktuell schrittweise "übertragen"

    def zeichne_boem_h_ziffernblatt():

        #Hintergrundboem_h_ziffernblatt_bild öffnen
        boem_h_ziffernblatt_bild = Image.open("boem_h_ziffernblatt_700x700.png")  # Pfad zum boem_h_ziffernblatt_Bild
        #Anpassung der boem_h_ziffernblatt_Bildgröße
        boem_h_ziffernblatt_bild = boem_h_ziffernblatt_bild.resize((565, 565), Image.Resampling.LANCZOS)
        #Erstellung eines boem_h_ziffernblatt_Bildobjektes, das in Tkinter verwendet werden kann
        hintergrundboem_h_ziffernblatt_bild = ImageTk.PhotoImage(boem_h_ziffernblatt_bild)
        #Fügt boem_h_ziffernblatt_Bild auf dem Canvas-Widgetr hinzu und platziert es auf den Koordinaten 150,150 (Zentrierung)
        canvas.create_image(351, 348, image=hintergrundboem_h_ziffernblatt_bild) # Zentrierung funktioniert nicht ganz! Wahrscheinlich ist eines der Bilder oval oder so -Erik
        #Hält das Hintergrundboem_h_ziffernblatt_bild Objekt im Speicher, um (garbage collected) zu vermeiden
        canvas.image = hintergrundboem_h_ziffernblatt_bild

    # Hier endet aktuell Dominick's Teil


    # Uhrzeit-Aktualisierung starten
    uhrzeit_aktualisieren()
    return root

# Hauptfunktion, die das Fenster erstellt und die Tkinter-Schleife startet
def main():
    root = erstelle_fenster()
    root.mainloop()

# Entry-Point der Anwendung
if __name__ == "__main__":
    main()
