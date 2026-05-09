Name = input("Enter the name of the client : ")
portefeuille = int(input("Enter la somme d'argent que vous avez dans votre portefeuille: "))
if portefeuille < 0:
    print("Invalid amount. Please enter a positive number.")
else:
    print(f"Client {Name} initialized with {portefeuille} coins.")
    print("Welcome to the project! What do you want to buy?")

    while portefeuille > 0:
        print("que voulez-vous acheter ?")
        print("1 - orange a 100\n2 - banane a 50\n3 - apple a 200\n4 - mangue a 300\n5 - cerise a 200\n6 - don\n")

        choix = input("Entrer votre choix en tapant le chiffre correspondant : ").strip()

        if choix == "1":
            prix = 100
            item = "orange"
        elif choix == "2":
            prix = 50
            item = "banane"
        elif choix == "3":
            prix = 200
            item = "apple"
        elif choix == "4":
            prix = 300
            item = "mangue"
        elif choix == "5":
            prix = 200
            item = "cerise"
        elif choix == "6":
            print("Merci pour votre donation !")
            break
        else:
            print("Choix invalide. Veuillez entrer un numéro entre 1 et 6.\n")
            continue

        if portefeuille >= prix:
            portefeuille -= prix
            print(f"Vous avez acheté {item}. Il vous reste donc {portefeuille}.")
        else:
            print("Solde insuffisant pour cet achat.\n")

    if portefeuille == 0:
        print("Votre portefeuille est vide. Merci pour vos achats !")
