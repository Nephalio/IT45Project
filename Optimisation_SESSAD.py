import numpy as np
import os
import pandas as pd

# nécessite d'installer les librairies numpy ( pip install numpy ) et pandas ( pip install pandas )
# chemin vers le fichier à modifier et peut nécessiter d'installer openyxl  ( pip install openpyxl )

# Récupère le chemin du répertoire contenant le script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construit le chemin vers le dossier "instances"
instances_directory = os.path.join(script_directory, "instances")

# Construit le chemin vers le dossier "30Missions-2centres"
missions_directory = os.path.join(instances_directory, "30Missions-2centres")

# Construit les chemins vers les fichiers CSV
centers_path = os.path.join(missions_directory, "centers.csv")
distances_path = os.path.join(missions_directory, "distances.csv")
employees_path = os.path.join(missions_directory, "Employees.csv")
missions_path = os.path.join(missions_directory, "Missions.csv")

# Charge les fichiers CSV
centers = pd.read_csv(centers_path, header=None)
distances = pd.read_csv(distances_path, header=None)
employees = pd.read_csv(employees_path, header=None)
missions = pd.read_csv(missions_path, header=None)


# renommage des colonnes et affichage des données bruts

centers = centers.rename(columns={0: 'id'})
centers = centers.rename(columns={1: 'nom'})
#print(f"CENTRE : \n\n {centers} \n \n")

#print(f"distances : \n\n {distances} \n \n")

employees = employees.rename(columns={0: 'id'})
employees = employees.rename(columns={1: 'centre_ID'})
employees = employees.rename(columns={2: 'compétence'})
employees = employees.rename(columns={3: 'spécialité'})
#print(f"Employees : \n\n {Employees} \n \n")
#print(Employees.columns)

missions = missions.rename(columns={0: 'id'})
missions = missions.rename(columns={1: 'jour'})
missions = missions.rename(columns={2: 'heure_début'})
missions = missions.rename(columns={3: 'heure_fin'})
missions = missions.rename(columns={4: 'compétence'})
missions = missions.rename(columns={5: 'spécialité'})
#print(f"Missions : \n\n {Missions} \n \n")



#regroupe les employés avec leur centre pour calculer les compétence de chaque centre
centers_Employees = pd.merge(centers, employees, left_on='id', right_on='centre_ID', how='inner', suffixes=('_center' , '_employee')) # chaque employé est associé à son centre dans un nouveau tableau , jointure inner join sur centre_ID
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
