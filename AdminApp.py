import csv
import sqlite3
import warnings
from PIL import Image
from tkinter import ttk
import hashlib

import customtkinter #pip3 install customtkinter
from CTkMessagebox import CTkMessagebox #pip install CTkMessagebox

#Funksjon som lager en database
def FunkLagDatabase():
    global conn #Gjør conn om til en global variabel
    conn = sqlite3.connect('GamasjerASDatabase.db') #Lager en database som heter GamasjerASDatabase.db

    global c #Gjør c om til en global variabel
    c = conn.cursor() #Lager en cursor

    #Lager en tabell som heter Brukerliste, med kolonenne ID, Brukernavn, Passord, Fornavn, Etternavn, Epost, Telefonnummer, Postnummer. Bruker VARCHAR for å kunne ha tekst, INTEGER for å kunne ha tall, og UNIQUE for å kunne ha unike verdier
    c.execute('''
            CREATE TABLE IF NOT EXISTS Brukerliste (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Brukernavn VARCHAR(56) NOT NULL UNIQUE,
                Passord UNIQUE NOT NULL CHECK (LENGTH(Passord) >= 5),
                Fornavn VARCHAR(25) NOT NULL,
                Etternavn VARCHAR(30) NOT NULL,
                Epost VARCHAR(50) UNIQUE NOT NULL,
                Telefonnummer INTEGER VARCHAR(8 ) NOT NULL UNIQUE, 
                Postnummer INTEGER VARCHAR(4) NOT NULL
            )
        ''')
    conn.commit() #Commiter i databasen
    conn.close() #Lukker databasen

#Funksjon som importerer brukere
def FunkImporterBrukere():
    try: #Bruker Try except
        conn = sqlite3.connect('GamasjerASDatabase.db') #Kobler til databasen 
        c = conn.cursor()
        with open('Assets/BrukerlisteGUI.csv', 'r') as csvfil:  #Åpner csv filen
                lescsv = csv.reader(csvfil) #Leser csv filen
                next(lescsv)  #Hopper over første rad i csv filen

                for row in lescsv: #For hver rad i csv filen
                    varKryptertPassord = hashlib.sha256(row[1].encode()).hexdigest() #Krypterer passordet med hashlib
                    c.execute('''
                        INSERT INTO Brukerliste(
                                Brukernavn,
                                Passord,
                                Fornavn, 
                                Etternavn, 
                                Epost, 
                                Telefonnummer, 
                                Postnummer
                                )
                        VALUES(?, ?, ?, ?, ?, ?, ?)''', row[0:1] + [varKryptertPassord] + row[2:]) #Setter inn informasjonen fra csv i brukerliste tabellen og de riktige kolonnene
                    

                conn.commit()
                CTkMessagebox(title="Importering fullført", message="Brukerene har blitt importert i databasen.",
                    icon="check", option_1="Fortsett", button_color="green") #Bruker messagebox til å få opp en melding hvis det funker.              
    except Exception as e: #Brukte exception as e fo å printe ut erroren jeg fikk, men fjernet det senere siden alt funket og da var det ikke nøvendig.
        CTkMessagebox(title="Feilmelding", message=f"Importering av Brukerliste feilet!", icon="cancel") #Bruker messagebox til å få opp en feilmelding hvis det ikke funker.
        conn.close

#Funksjon som sletter brukere
def FunkSlettBrukere():
    conn = sqlite3.connect('GamasjerASDatabase.db') 
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM Brukerliste''') #Sletter alt sammen som ligger inne i brukerliste tabellen.
        c.execute('''DELETE FROM sqlite_sequence''') 
        #Siden jeg har brukt AUTOINCRIMENT, så vil det bli lagret informasjon i tabellen sqlite_sequence, selv om jeg sletter alt ifra brukertabellen vil det fortsatt være info der,
        #Sånn at hvis jeg skal importere brukere vil IDen starte på 201 selv om brukerene har blitt slettet pga infoen i sqlite_sequence. Derfor slettet jeg alt i den også. 
        conn.commit()
        CTkMessagebox(title="Sletting fullført", message="Brukerene har blitt slettet i databasen.",
                  icon="check", option_1="Fortsett") #Her får man opp en melding hvis det fungerer.
    except Exception as e:
        CTkMessagebox(title="Feilmelding", message=f"Sletting av Brukerliste feilet!: {e}", icon="cancel") #Her får man opp en feilmelding hvis det ikke fungerer, og der står også erroren. 
    finally:
        conn.close

#Funksjon som søker opp kunder
def FunkSearchBrukere(id):
    conn = sqlite3.connect('GamasjerASDatabase.db') #Kobler til databasen
    c = conn.cursor()
    try:
        c.execute('''
                SELECT
                    ID,
                    Brukernavn,
                    Fornavn,
                    Etternavn,
                    Epost,
                    Telefonnummer,
                    Postnummer
                FROM Brukerliste 
                WHERE ID = ?
                ''', (id,))
        rows = c.fetchall() #Henter informasjonen som er i tabellen og lagrer det i rows
        return rows #Returnerer rows
    except Exception as e:
        CTkMessagebox(title="Feilmelding", message=f"Noe gikk galt: {e}", icon="cancel")
    finally:
        conn.close()


#Main
def main():
    FunkLagDatabase()

    varAdminWindow = customtkinter.CTk() #Lager vinduet
    varAdminWindow.title('Gamasjer AS') #Tittel på vinduet
    varAdminWindow.after(0, lambda:varAdminWindow.state('zoomed')) #Vinduet starter maksimert. Dette funket på laptoppen, men ikke når jeg hadde en ekstern skjerm koblet til i laptoppen. Hvis det ikke funker sett vinduet til maksimert når du starter det for best mulig opplevelse. 


    customtkinter.set_appearance_mode("dark") #Setter modusen til dark mode.
    customtkinter.set_default_color_theme("blue") #Setter farge temaet til grønn.

    varBakgrunnBilde = customtkinter.CTkImage(dark_image=Image.open("Images/AdminGUIBakgrunn.png"),size=(1920, 1080)) #Åpner opp bakgrunnsbilde og definerer størrelsen.
    varBakgrunnLabel = customtkinter.CTkLabel(varAdminWindow, image=varBakgrunnBilde, text="")   # type: ignore
    varBakgrunnLabel.place(x=0, y=0, relwidth=1, relheight=1) #Plasserer bakgrunnsbilde i vindue med riktig kordinater.

    tabview = customtkinter.CTkTabview(varAdminWindow) #Lager en tabview.
    tabview.pack(padx=20, pady=20) #Bruker pack sånn at tabview syntes, definerer størelsen på tabviewen. 

    #Lager de forskjellige tabbene. 
    varTab1 = tabview.add("Startside")  
    varTab2 = tabview.add("Legg til innhold")  
    varTab3= tabview.add("Fjern innhold")  
    varTab4= tabview.add("Søk i kundedatabase")  
    tabview.set("Startside") #Gjør sånn at dette er den første man får opp når man starter programmet. 

    #Lager en overskrift og et paragraf. Velger hvilke tab det skal være i, velger font størrelse, og marginene. Alt i paragrafet vil ikke stemme siden noen funksjoner har blitt slettet for å passe oppgaven.
    varVelkommenOverskrift = customtkinter.CTkLabel(varTab1, text="Velkommen til Gamasjer AS sitt database verktøy!", font=("Arial", 20)).pack(pady=5)
    varVelkommenParagrapf = customtkinter.CTkLabel(varTab1, text="Dette programmet er utviklet for å administrere en brukerdatabase med funksjoner, inkludert import av brukere fra CSV-filer, opprette en ren database, slette brukere og søke etter brukere. \n\nDen bruker SQLite for databasebehandling og tilpasset tkinter for det grafiske brukergrensesnittet. Nøkkelfunksjoner inkluderer import av brukere og postnumre, sletting av brukere og postnumre, og søk etter brukere etter ID.", font=("Arial", 12), wraplength=500, justify='left').pack(pady=5)

    #Legger til en logo. Bruker photoimage funksjonen til å dette, ganske enkel kode. 
    varLogoBilde = customtkinter.CTkImage(dark_image=Image.open("Images/logo.png"),size=(263, 163))
    varBildeLabel = customtkinter.CTkLabel(varTab1, image=varLogoBilde, text="").pack(pady=15)


    #Ganske enkel kode, her legger jeg til labels, paragraf, og knapper. Jeg linker knappene til de forskjellige funksjonene sånn at man kan kjøre de via knapper. 
    varLeggtilLabel = customtkinter.CTkLabel(varTab2, text="Legg til innhold i databasen", font=("Arial", 20)).pack(pady=5)
    varLeggtilParagraf = customtkinter.CTkLabel(varTab2, text="Her kan du administrere innholdet i databasen din ved å legge til og oppdatere data. Først kan du opprette en ny database ved å klikke på Lag en database - dette vil sette opp strukturen som trengs for å lagre informasjonen din. Deretter kan du bruke Importer brukere i databasen for å legge til nye brukerdata fra en CSV-fil, og Importer postnummer i databasen for å legge til postnummerinformasjon på samme måte.\n\nMed disse verktøyene kan du enkelt administrere og oppdatere innholdet i databasen din for å sikre nøyaktig og oppdatert informasjon.", font=("Arial", 12), wraplength=500, justify='left').pack(pady=5)
    varImporterCSV = customtkinter.CTkButton(varTab2, text="Importer brukere i databasen", font=("Arial", 15), width=250, command=FunkImporterBrukere).pack(pady=3)

    #Samme kode her, definerer fargen sånn at det passer med tanke på at man skal fjerne noe. 
    varFjernLabel = customtkinter.CTkLabel(varTab3, text="Fjern innhold ifra databasen", font=("Arial", 20)).pack(pady=5)
    varFjernParagraf = customtkinter.CTkLabel(varTab3, text="Her kan du fjerne innhold fra databasen ved å slette brukere eller postnummer. Ved å klikke på Slett brukere, vil du kunne fjerne brukerdata fra databasen din. Dette kan være nyttig hvis du for eksempel ønsker å rydde opp i gamle eller unødvendige brukerprofiler. Tilsvarende kan du bruke Slett postnummere for å fjerne postnummerinformasjon som ikke lenger er relevant eller nøyaktig.\n\nDisse verktøyene gir deg kontroll over databasens innhold ved å tillate deg å fjerne unødvendig eller utdatert informasjon med letthet.", font=("Arial", 12), wraplength=500, justify='left').pack(pady=5)
    varSlettBrukere = customtkinter.CTkButton(varTab3, text="Slett brukere", fg_color="red", hover_color="maroon", width=250, command=FunkSlettBrukere).pack(pady=3)

    #En funksjon som oppdaterer tabellen i GUI,det skapte problemer å ha den utenom så da var det lettest og bare ha den inne i main.
    def OppdaterTabell():
        conn = sqlite3.connect('GamasjerASDatabase.db')
        c = conn.cursor()
        for i in varTree.get_children(): 
            varTree.delete(i) #Sletter alt som ligger i treeview(tabellen)
        try:
            #Joiner sammen alt bortsett fra postnummer ifra postnummer listen sånn at det ikke blir duplikat. Sorterer etter ID sånn at det blir mer ryddig.
            c.execute('''
                SELECT
                    ID,
                    Brukernavn,
                    Fornavn, 
                    Etternavn, 
                    Epost, 
                    Telefonnummer, 
                    Postnummer
                FROM Brukerliste    
                ''') 
                
            resultat = c.fetchall() #Lagrer det i en variable som heter resultat

            
            for row in resultat:
                varTree.insert("", "end", values=row) #Setter inn resultatene i hver rad i treeview.

        except Exception as e:
            CTkMessagebox(title="Feilmelding", message=f"Noe gikk galt: {e}", icon="cancel") #Gir error hvis det ikke fungerer.
        #Kjører funksjonen hvert 10 sekund, det var dette som skapte problemer når jeg skulle integrere den med FunkAddITabell.
        varAdminWindow.after(10000, OppdaterTabell)
    
    #En funksjon som oppdaterer tabellen med resultatet ifra det man skriver inn i search entry sånn at man får opp info om brukeren.
    def FunkSearchOppdatering():
        rows = FunkSearchBrukere(varSearchEntry.get()) #Henter funksjonen FunkSearchBrukere og legger det i rows.
        if rows is None: #Hvis rows er None så returnerer den.
            rows = [] 
        for i in varTree.get_children(): #For hver rad i treeviewet
            varTree.delete(i) #Sletter det som er i tabellen.
        for row in rows: 
            varTree.insert("", "end", values=row) #Henter det man skriver inn entry feltet, setter inn informasjonen ifra FunkSearchBrukere og setter det inn i hver kolonne.
        if not rows: #Hvis man skriver inn en bruker som ikke finnes så får man en advarsel. 
            CTkMessagebox(title="Advarsel", message="Brukeren finnes ikke!!!", icon="warning") #Messagebox error
            return

    #KLabels og knapper, og en entry hvor man kan skrive inn bruker ID. Bruker grid sånn at jeg kan ha flere widgets ved siden av hverandre. 
    varSearchLabel = customtkinter.CTkLabel(varTab4, text="Søk i kundedatabasen", font=("Arial", 20)).grid(row=0, column=0, columnspan=2)
    varSearchEntry = customtkinter.CTkEntry(varTab4, width=350, placeholder_text="Skriv in kunde ID...")
    varSearchEntry.grid(row=1, column=0, sticky='e')
    varSearchButton = customtkinter.CTkButton(varTab4, text="Søk", width=20, command=FunkSearchOppdatering)
    varSearchButton.grid(row=1, column=1, sticky='w')

    #Her definerer jeg fargene og font størrelse som jeg skal bruke for å endre på hvordan treeview(tabellen) ser ut. 
    varBGFarge = varAdminWindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
    varTekstFarge = varAdminWindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
    varSelectionFarge = varAdminWindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
    varHeaderFarge = varAdminWindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
    varTekstSize = 14
    varHeaderTekstSize = 16

    #Her velger jeg hvordan treeviewet skal se ut og legger til de fargene jeg definerte tidligere.  
    varTreestyle = ttk.Style()
    varTreestyle.theme_use('default')
    varTreestyle.configure("Treeview", background=varBGFarge, foreground=varTekstFarge, fieldbackground=varBGFarge, font=('Helvetica', varTekstSize), borderwidth=0)
    varTreestyle.configure("Treeview.Heading", background=varHeaderFarge, foreground=varTekstFarge, font=('Helvetica', varHeaderTekstSize),)
    varTreestyle.map('Treeview', background=[('selected', varBGFarge)], foreground=[('selected', varSelectionFarge)])
    varAdminWindow.bind("<<TreeviewSelect>>", lambda event: varAdminWindow.focus_set())

    #Her lager jeg treeviewet, jeg lager de forskjellige kolonnene først, også velger jeg hva headingen på kolonnen skal være, i dette tilfellet valgte jeg at de heter det samme.
    varTree = ttk.Treeview(varTab4, columns=("ID", "Brukernavn",  "Fornavn", "Etternavn","Epost", "Telefonnummer", "Postnummer"), show='headings')
    varTree.heading("ID", text="ID")
    varTree.heading("Brukernavn", text="Brukernavn")
    varTree.heading("Fornavn", text="Fornavn")
    varTree.heading("Etternavn", text="Etternavn")
    varTree.heading("Epost", text="Epost")
    varTree.heading("Telefonnummer", text="Telefonnummer")
    varTree.heading("Postnummer", text="Postnummer")
    
    #Her bruker jeg grid igjen, også bruker width til å endre størrelsen på kolonnene. Disse innstillingene er tilpasset sånn at det er best på laptoppen min. Men man kan også justere kolonne bredde inne på GUIen ved å dra. 
    varTree.grid(row=3, column=0, columnspan=2, pady=(25, 0 ))
    varTree.column("ID", width=70)
    varTree.column("Brukernavn", width=120)
    varTree.column("Fornavn", width=120)
    varTree.column("Etternavn", width=150)
    varTree.column("Epost", width=290)
    varTree.column("Telefonnummer", width=170)
    varTree.column("Postnummer", width=70)

    #Her kjører jeg funksjonene som adder informasjonen i tabellen og oppdaterer den.
    OppdaterTabell()

    varAdminWindow.mainloop() #Her kjører jeg GUI vinduet. 
   
if __name__ == "__main__":
    main() #Kjører main