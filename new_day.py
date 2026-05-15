print("Table de multiplication")
for i in range(0, 13):
    for j in range(0,13) :  
     if j < 12 :
        print(f" {i} fois {j} = {i*j}")
     else :
          print(f" {i} fois {j} = {i*j} \n")
    if i < 12 :
       print(f"Debut  de la table de mulptiplication de {i + 1:3d}")
    else :
      print(f"merci")
print("fin de la table de multiplication")
# this is my firt version and enjoy your day 
