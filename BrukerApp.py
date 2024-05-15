import sqlite3 
import hashlib 
import customtkinter 
from CTkMessagebox import CTkMessagebox 
from PIL import Image #Importerer Image fra PIL for å kunne bruke bilder
from tkinter import TclError #Importerer TclError for å kunne håndtere feil

#Funksjon for å lage database
def FunkLagDatabase():
    global conn #Globaliserer conn
    conn = sqlite3.connect('GamasjerASDatabase.db') #Kobler til databasen

    global c 
    c = conn.cursor()  

#Funksjon for å lage logge inn
def FunkLogginn():
    
    global varBrukernavnLogin #Globaliserer variabelen
    varBrukernavnLogin = varBrukernavnEntry.get() #Henter brukernavnet fra det man skrever inn med .get
    
    global varEpostLogin
    varEpostLogin = varLEpostEntry.get()
    
    global varPassordLogin
    varPassordLogin = varLPassordEntry.get()

    global varKryptertLoginPassord
    varKryptertLoginPassord = hashlib.sha256(varPassordLogin.encode()).hexdigest() #Krypterer passordet og globaliserer dfet også.

    try:
        conn = sqlite3.connect('GamasjerASDatabase.db')
        c = conn.cursor()

        
        c.execute('''SELECT * FROM Brukerliste WHERE 
                    Brukernavn=? 
                    AND Epost=? 
                    AND Passord=?''', 
                    (varBrukernavnLogin, varEpostLogin,  varKryptertLoginPassord)) #Henter informasjonen fra databasen for å senere sjekke om det er riktig

        
        if c.fetchone() is not None: #Hvis det er riktig informasjon så vil det komme opp en messagebox
            CTkMessagebox(title="Login", message="Du har logget inn.",
                    icon="check", option_1="Fortsett")
            FunkVisInfo() #Kjører funksjonen som viser informasjonen om brukeren.
        else:
            CTkMessagebox(title="Login", message="Du har skrevet inn feil informasjon.", #Hvis det er feil informasjon så vil det komme opp en messagebox
                    icon="cancel", option_1="Avbryt")
    except Exception as e:  #Hvis selve funksjonen failer så får man dette. 
            print(e)
            CTkMessagebox(title="Login", message="En feil oppstod, du har ikke blitt logget inn!",
                        icon="cancel", option_1="Avbryt")
    finally: conn.close()

def FunkLagBrukernavn(varFornavn, varEtternavn): #Funksjon for å lage brukernavn
    varBrukernavn = f"{varFornavn}.{varEtternavn}" #Tar fornavn + etternavn og setter et punktum i midten.
    return varBrukernavn #Returnerer brukernavnet

#Funksjon for å registrere bruker
def FunkRegistrer():
    try:
        
        varFornavn = varFornavnEntry.get() #Henter fornavnet fra entryen med .get funksjonen også setter det i en variabel. Gjør det samme på de under.
        varEtternavn = varEtternavnEntry.get()
        varTlf = varTlfEntry.get()
        varPostnummer = varPostnummerEntry.get()
        varEpost = varEpostEntry.get()
        
        varPassord = varPassordEntry.get()
        varPassordBekreft = varBekreftPassordEntry.get()

        
        if varPassord == varPassordBekreft: #Sjekker om passordene stemmer
            varBrukernavn = FunkLagBrukernavn(varFornavn, varEtternavn) #Kjører funksjonen for å lage brukernavn

            varKryptertPassord = hashlib.sha256(varPassord.encode()).hexdigest() #Krypterer passordet og kaller det for noe i en variabel.

            conn = sqlite3.connect('GamasjerASDatabase.db')
            c = conn.cursor()

            
            c.execute('''INSERT INTO Brukerliste(
                      Brukernavn, 
                      Fornavn, 
                      Etternavn, 
                      Telefonnummer, 
                      Postnummer, 
                      Epost, 
                      Passord
                      ) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (varBrukernavn, varFornavn, varEtternavn, varTlf, varPostnummer, varEpost, varKryptertPassord)) #Legger inn informasjonen i databasen

            
            conn.commit()
            conn.close()
            CTkMessagebox(title="Registering", message="Brukeren har blitt opprettet.", #Messagebox hvis det er riktig
                  icon="check", option_1="Ok")
        else:
            CTkMessagebox(title="Registrering", message="Brukerkrav er ikke oppfylt.", #Messagebox for hvis det er feil.
                  icon="warning", option_1="Avbryt")
    except Exception as e:
         CTkMessagebox(title="Registrering", message="Funksjonen feilet!",
                  icon="cancel", option_1="Avbryt")

def FunkSlettBruker():
    try:  
        conn = sqlite3.connect('GamasjerASDatabase.db')
        c = conn.cursor()

        
        c.execute('''DELETE FROM Brukerliste WHERE Brukernavn = ?''', (varBrukernavnLogin,)) #Sletter brukeren fra databasen
        c.execute('''DELETE FROM sqlite_sequence''')  #Sletter alt i dette databsen siden det ligger igjen info der pga autoincriment.

        
        conn.commit()
        conn.close()
        
        CTkMessagebox(title="Sletting av bruker", message="Brukeren har blitt slettet.",
                  icon="check", option_1="Ok")
    
    except Exception as e: 
        CTkMessagebox(title="Sletting av bruker", message="Funksjonen feilet!",
                  icon="cancel", option_1="Avbryt")

#Funksjon for å endre passord        
def FunkEndrePassord():
    try:
        varNyttPassord = varPassordEntry.get() #Henter passordet fra passodentryen og bruker .get

        conn = sqlite3.connect('GamasjerASDatabase.db')

        cursor = conn.cursor()

        varKryptertNyttPassord = hashlib.sha256(varNyttPassord.encode()).hexdigest() #Krypterer

        varByttPassordSQL = '''UPDATE Brukerliste SET Passord = ? WHERE Brukernavn = ?''' #Oppdaterer passordet i databasen med det nye passordet

        cursor.execute(varByttPassordSQL, (varKryptertNyttPassord, varBrukernavnLogin)) #Executer den variabelen. 

        conn.commit()
        
        CTkMessagebox(title="Endring av passord", message="Passordet har blitt endret.",
                    icon="check", option_1="Ok")
        
    except Exception as e: 
        print(e)
        CTkMessagebox(title="Endring av passord", message="En feil oppstod, passordet har ikke blitt endret!",
                    icon="cancel", option_1="Avbryt")
    finally: conn.close()

#Funksjon for å vise brukerinfo
def FunkVisInfo():
    try:
        conn = sqlite3.connect('GamasjerASDatabase.db')
        c = conn.cursor()
        

        
        c.execute('''SELECT * FROM Brukerliste WHERE Brukernavn=? AND Epost=? AND Passord=?''', (varBrukernavnLogin, varEpostLogin,  varKryptertLoginPassord)) #Henter informasjonen fra databasen og legger til riktige variabler.
        varBrukerinfo = c.fetchone() #Henter informasjonen og legger det i en variabel.


        global varInfovarBrukerWindow
        varInfovarBrukerWindow = customtkinter.CTk() #Lager vinduet
        varInfovarBrukerWindow.title('Brukerinfo')
        varInfovarBrukerWindow.geometry("320x450")

            
        if varBrukerinfo is not None: #Hvis det er informasjon så vil alt dette komme opp. Enkle customtkinter koder som ikke trenger mye forklaring. 
            varRegistrerLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Brukerinfo", font=("default", 35))
            varRegistrerLabel.grid(row=2, column=0, padx=10, pady=10, columnspan=2) #Bruker grid

            varBrukernavnLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Brukernavn").grid(row=3, column=0, padx=15, pady=1, sticky='w')
            varBrukernavnEntry = customtkinter.CTkTextbox(varInfovarBrukerWindow, width=300, height=1)
            varBrukernavnEntry.insert("1.0", varBrukerinfo[1])  #Setter inn informasjonen i entryen. 
            varBrukernavnEntry.configure(state='disabled') #Gjør at man ikke kan edite boksen. 
            varBrukernavnEntry.grid(row=4, column=0, padx=10, pady=1, columnspan=2)

            varFornavnLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Fornavn").grid(row=5, column=0, padx=15, pady=1, sticky='w')
            varFornavnEntry = customtkinter.CTkTextbox(varInfovarBrukerWindow, width=150, height=1)
            varFornavnEntry.insert("1.0", varBrukerinfo[3])  
            varFornavnEntry.configure(state='disabled')
            varFornavnEntry.grid(row=6, column=0, padx=1, pady=1, sticky='e')

            varEtternavnLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Etternavn").grid(row=5, column=1, padx=15, pady=1, sticky='w')
            varEtternavnEntry = customtkinter.CTkTextbox(varInfovarBrukerWindow, width=150, height=1)
            varEtternavnEntry.insert("1.0", varBrukerinfo[4])  
            varEtternavnEntry.configure(state='disabled')
            varEtternavnEntry.grid(row=6, column=1, padx=1, pady=1, sticky='w')

            varTlfLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Telefonnummer").grid(row=7, column=0, padx=15, pady=1, sticky='w')
            varTlfEntry = customtkinter.CTkTextbox(varInfovarBrukerWindow, width=150, height=1)
            varTlfEntry.insert("1.0", varBrukerinfo[6])  
            varTlfEntry.configure(state='disabled')
            varTlfEntry.grid(row=8, column=0, padx=1, pady=1, sticky='e')

            varPostnummerLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Postnummer").grid(row=7, column=1, padx=15, pady=1, sticky='w')
            varPostnummerEntry = customtkinter.CTkTextbox(varInfovarBrukerWindow, width=150, height=1)
            varPostnummerEntry.insert("1.0", varBrukerinfo[7])  
            varPostnummerEntry.configure(state='disabled')
            varPostnummerEntry.grid(row=8, column=1, padx=1, pady=1, sticky='w')

            varEpostLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Epost").grid(row=9, column=0, padx=15, pady=1, sticky='w')
            varEpostEntry = customtkinter.CTkTextbox(varInfovarBrukerWindow, width=300, height=1)
            varEpostEntry.insert("1.0", varBrukerinfo[5])  
            varEpostEntry.configure(state='disabled')
            varEpostEntry.grid(row=10, column=0, padx=10, pady=1, columnspan=2)

            varPassordLabel = customtkinter.CTkLabel(varInfovarBrukerWindow, text="Passord").grid(row=11, column=0, padx=15, pady=1, sticky='w')
            varPassordEntry = customtkinter.CTkEntry(varInfovarBrukerWindow, width=150, placeholder_text="Nytt passord...")
            varPassordEntry.grid(row=12, column=0, padx=1, pady=1, sticky='e')

            varEndrePassordButton = customtkinter.CTkButton(varInfovarBrukerWindow, width=150, text="Bytt Passord", command=FunkEndrePassord)
            varEndrePassordButton.grid(row=12, column=1, padx=1, pady=1, sticky='w')
            
            varSlettdButton = customtkinter.CTkButton(varInfovarBrukerWindow, width=300, height=35, text="Slett Bruker", font=("default", 20, "bold"), fg_color="red", hover_color="maroon", command=FunkSlettBruker)
            varSlettdButton.grid(row=13, column=0, padx=10, pady=15, columnspan=2)

            varInfovarBrukerWindow.mainloop() 
    except TclError: #Ignorerer tlcerror hvis det skjer, det er ikke noe viktig. 
        pass
    except Exception as e: 
        CTkMessagebox(title="Brukerinfo", message="Funksjonen feilet!",
                  icon="cancel", option_1="Avbryt")
    finally: conn.close()

#Main funksjonen
def main():
    varBrukerWindow = customtkinter.CTk() #Lager vindu
    varBrukerWindow.title('Gamasjer AS') #Tittel
    varBrukerWindow.after(0, lambda:varBrukerWindow.state('zoomed')) #starter maksimert, funker ikke på alle maskiner men den går på laptoppen.

    varBakgrunnBilde = customtkinter.CTkImage(dark_image=Image.open("Images/GUIBakgrunn.png"),size=(1920, 1080)) #Åpner opp bakgrunnsbilde og definerer størrelsen.
    varBakgrunnLabel = customtkinter.CTkLabel(varBrukerWindow, image=varBakgrunnBilde, text="")   # type: ignore
    varBakgrunnLabel.place(x=0, y=0, relwidth=1, relheight=1) #Plasserer bakgrunnsbilde i vindue med riktig kordinater.


    customtkinter.set_appearance_mode("dark") #Gjør at den blir i dark mode
    customtkinter.set_default_color_theme("green") #Setter farge tema til grønt.
    tabview = customtkinter.CTkTabview(varBrukerWindow)  #Lager tabviewet.
    tabview.pack(padx=20, pady=20) #Packer tabviewet. 

    #Lager de forskjellige tabbene.
    varTab1 = tabview.add("Startside")  
    varTab2 = tabview.add("Login")  
    varTab3= tabview.add("Registrer")  
    tabview.set("Startside") 

    #Resten er veldig enkel customtkinter kode, jeg har gjort noen av variablene global så det blir lettere, og linket knappene til kommandoene jeg vil kjøre.
    varVelkommenOverskrift = customtkinter.CTkLabel(varTab1, text="Velkommen til Gamasjer AS sitt brukerverktøy!", font=("default", 20, "bold")).pack(pady=5)
    varVelkommenParagrapf = customtkinter.CTkLabel(varTab1, text="Velkommen til Gamasjer AS sitt brukerverktøy! Dette programmet er skreddersydd for å gjøre din opplevelse så enkel og effektiv som mulig. Her kan du utføre flere handlinger for å administrere din brukerkonto og få tilgang til våre tjenester.\n\nPå startsiden vil du bli ønsket velkommen med informasjon om de ulike funksjonene og hvordan du kan navigere mellom fanene. I registreringsfanen kan du enkelt opprette en ny brukerkonto ved å fylle ut nødvendig informasjon. På logginnfanen kan du trygt logge inn med ditt brukernavn og passord for å få tilgang til våre tjenester.\n\nVi håper du finner dette verktøyet nyttig, og ikke nøl med å kontakte vår kundeservice hvis du har spørsmål eller trenger hjelp.", font=("default", 12), wraplength=500, justify='left').pack(pady=5, padx=15)
    varServiceTlf = customtkinter.CTkLabel(varTab1, text="Ring vår servicedesk: +47 913 43 152", font=("default", 12), wraplength=500, justify='center', text_color='SpringGreen2').pack(pady=5)


    varLogoBilde = customtkinter.CTkImage(dark_image=Image.open("Images/logo.png"),size=(263, 163))
    varBildeLabel = customtkinter.CTkLabel(varTab1, image=varLogoBilde, text="").pack(pady=15)

    varRegistrerLabel = customtkinter.CTkLabel(varTab3, text="Registrer ny bruker", font=("default", 35))
    varRegistrerLabel.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

    global varFornavnEntry
    varFornavnEntry = customtkinter.CTkEntry(varTab3, width=150, placeholder_text="Fornavn...")
    varFornavnEntry.grid(row=6, column=0, padx=1, pady=10, sticky='e')

    global varEtternavnEntry
    varEtternavnEntry = customtkinter.CTkEntry(varTab3, width=150, placeholder_text="Etternavn...")
    varEtternavnEntry.grid(row=6, column=1, padx=1, pady=10, sticky='w')

    global varTlfEntry
    varTlfEntry = customtkinter.CTkEntry(varTab3, width=150, placeholder_text="Telefonnummer...")
    varTlfEntry.grid(row=7, column=0, padx=1, pady=10, sticky='e')

    global varPostnummerEntry
    varPostnummerEntry = customtkinter.CTkEntry(varTab3, width=150, placeholder_text="Postnummer...")
    varPostnummerEntry.grid(row=7, column=1, padx=1, pady=10, sticky='w')

    global varEpostEntry
    varEpostEntry = customtkinter.CTkEntry(varTab3, width=300, placeholder_text="Epost...")
    varEpostEntry.grid(row=9, column=0, padx=10, pady=10, columnspan=2,)

    global varPassordEntry
    varPassordEntry = customtkinter.CTkEntry(varTab3, width=150, placeholder_text="Passord...", show="*")
    varPassordEntry.grid(row=10, column=0, padx=1, pady=10, sticky='e')

    global varBekreftPassordEntry
    varBekreftPassordEntry = customtkinter.CTkEntry(varTab3, width=150, placeholder_text="Bekreft Passord...", show="*")
    varBekreftPassordEntry.grid(row=10, column=1, padx=1, pady=10, sticky='w')

    varRegistrerButton = customtkinter.CTkButton(varTab3, width=300, height=35, text="Registrer", font=("default", 20, "bold"), command=FunkRegistrer)
    varRegistrerButton.grid(row=11, column=0, padx=10, pady=10, columnspan=2)


    varLoginLabel = customtkinter.CTkLabel(varTab2, text="Logg inn i bruker", font=("default", 35))
    varLoginLabel.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

    global varBrukernavnEntry
    varBrukernavnEntry = customtkinter.CTkEntry(varTab2, width=300, placeholder_text="Brukernavn...")
    varBrukernavnEntry.grid(row=6, column=0, padx=1, pady=5, columnspan=2)

    global varLEpostEntry
    varLEpostEntry = customtkinter.CTkEntry(varTab2, width=150, placeholder_text="Epost...")
    varLEpostEntry.grid(row=7, column=0, padx=1, pady=5, sticky='e')

    global varLPassordEntry
    varLPassordEntry = customtkinter.CTkEntry(varTab2, width=150, placeholder_text="Passord...", show="*")
    varLPassordEntry.grid(row=7, column=1, padx=1, pady=5, sticky='w')

    varLoginButton = customtkinter.CTkButton(varTab2, width=300, height=35, text="Login", font=("default", 20, "bold"), command=FunkLogginn)
    varLoginButton.grid(row=11, column=0, padx=10, pady=10, columnspan=2)

    varBrukerWindow.mainloop() #Kjører vinduet

    FunkLagDatabase() #Kjører lag database funksjonen.
if __name__ == "__main__":
    main() #Kjører main