import numpy as np
import pandas as pd

# nécessite d'installer les librairies numpy ( pip install numpy ) et pandas ( pip install pandas )
# chemin vers le fichier à modifier et peut nécessiter d'installer openyxl  ( pip install openpyxl )

# Charger les fichier CSV en spécifiant que la première ligne est une ligne de données et non pas l'entête 
centers = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\centers.csv" , header=None)         # mettre le bon format fichier + pip install openpyxl
distances = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\distances.csv" , header=None)
Employees = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\Employees.csv" , header=None)
Missions = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\Missions.csv" , header=None)


# renommage des colonnes et affichage des données bruts

centers = centers.rename(columns={0: 'id'})
centers = centers.rename(columns={1: 'nom'})
#print(f"CENTRE : \n\n {centers} \n \n")

#print(f"distances : \n\n {distances} \n \n")

Employees = Employees.rename(columns={0: 'id'})
Employees = Employees.rename(columns={1: 'centre_ID'})
Employees = Employees.rename(columns={2: 'compétence'})
Employees = Employees.rename(columns={3: 'spécialité'})
#print(f"Employees : \n\n {Employees} \n \n")
#print(Employees.columns)

Missions = Missions.rename(columns={0: 'id'})
Missions = Missions.rename(columns={1: 'jour'})
Missions = Missions.rename(columns={2: 'heure_début'})
Missions = Missions.rename(columns={3: 'heure_fin'})
Missions = Missions.rename(columns={4: 'compétence'})
Missions = Missions.rename(columns={5: 'spécialité'})
#print(f"Missions : \n\n {Missions} \n \n")



#regroupe les employés avec leur centre pour calculer les compétence de chaque centre
centers_Employees = pd.merge(centers, Employees, left_on='id', right_on='centre_ID', how='inner', suffixes=('_center' , '_employee')) # chaque employé est associé à son centre dans un nouveau tableau , jointure inner join sur centre_ID
centers_Employees = centers_Employees.drop('centre_ID', axis=1)     # la clé de jointure est supprimé car inutile
print(centers_Employees)
print("\n")

counts_competence = centers_Employees.groupby(['id_center', 'nom'])['compétence'].value_counts().unstack(fill_value=0) # compte le nombre de compétence LSF et LPC de chaque centre
print(f"Nombre de Compétence de chaque centre : \n\n {counts_competence} \n\n")
counts_specialite = centers_Employees.groupby(['id_center', 'nom'])['spécialité'].value_counts().unstack(fill_value=0) # compte le nombre de spécialité de chaque centre
print(print(f"Nombre de Spécialité de chaque centre : \n\n {counts_specialite} \n\n"))

#print(centers_Employees.groupby(['compétence','nom']).value_counts())   # affiche qui possèdent des compétences LPC et LSF pour les centre
#print(centers_Employees["compétence"].value_counts())               # compte le nombre d'employé ayant les compétences LSF et LPC total de tous les centres (sans distinction des centres)
#print(centers_Employees.describe())
