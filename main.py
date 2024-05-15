import customtkinter #Importerer customtkinter for å lage GUI
import subprocess #Importerer subprocess for å kunne kjøre de andre python filene i mappen

#Funksjon for å kjøre bruker appen
def FunkBrukerApp():
    root.destroy() #Her lukker jeg vinduet med en gang knappen trykkes på og funksjonen kjører.
    subprocess.call(["python", "BrukerApp.py"]) #bruker subprocess og velger hvilken fil jeg skal kjøre og hvilke programmeringsspråk.

#Funksjon for å kjøre admin appen
def FunkAdminApp(): 
    root.destroy() #Her lukker jeg vinduet med en gang knappen trykkes på og funksjonen kjører.
    subprocess.call(["python", "AdminApp.py"]) #bruker subprocess og velger hvilken fil jeg skal kjøre og hvilke programmeringsspråk.

#Main funksjon
def main():
    global root #Gjør root vinduet om til en global variabel
    root = customtkinter.CTk() #Lager et vindu med customtkinter som jeg kaller for root
    root.title("Valg av program") #Gi vinduet navnet valg av program
    root.geometry("400x300") #Setter størrelsen på selve vinduet


    customtkinter.set_appearance_mode("dark") #Gjør sånn at GUIen blir automatisk i dark mode
    customtkinter.set_default_color_theme("green") #Gjør sånn at farge temaet er grønn

    varProgramLabel = customtkinter.CTkLabel(root, text="Hvilke program vil du kjøre?", font=("default", 30)) #Lager et label med teskt og font størrelse.
    varProgramLabel.pack(pady=20) #Packer label og legger til padding for at det skal bli mellomrom.

    varBrukerApp = customtkinter.CTkButton(root, text="Bruker applikasjon", font=("default", 30), command=FunkBrukerApp) #Lager en knapp med tekst, definerer font og størrelsen og legger til kommandoen som kjører Bruker appen.
    varBrukerApp.pack(pady=20) #Packer button og legger til padding for at det skal bli mellomrom.

    varAdminApp = customtkinter.CTkButton(root, text="Admin applikasjon", font=("default", 30), command=FunkAdminApp, fg_color="#196aa5", hover_color="SteelBlue4") #Lager en knapp med tekst, definerer font og størrelsen og legger til kommandoen som kjører admin appen. Har også egene farger på knappen.
    varAdminApp.pack(pady=20) #Packer button og legger til padding for at det skal bli mellomrom.

    root.mainloop() #Kjører vinduet.

if __name__ == "__main__":
    main() #Kjører main