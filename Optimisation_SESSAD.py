### 
#    CONTRAINTES 
###

# optimisation sur une semaine de 5 jours , 7h par jour de travail par personne, 35h/semaine/personne, 
#et une amplitude horaire max de 13 heures (différence entre l'heure de fin de la journée de travail et l'heure de début de la journée de travail)

#Le temps de travail d'un intervenant par jour = temps d'exécution des missions assignées + temps de déplacement. 

import numpy as np
import os
import pandas as pd



''' 
class Gene :            # chaque gène est une affectation d'une mission à un employé
    
    def __init__(self,mission, centre, cout_distance, specialite_employe, date, heure_arrive, heure_de_depart , lieu_de_depart):
        self.mission = mission
        self.centre = centre
        self.cout_distance = cout_distance
        self.specialite_employe = specialite_employe
        self.date = date
        self.heure_arrive = heure_arrive
        self.heure_de_depart = heure_de_depart
        self.lieu_de_depart = lieu_de_depart

#class Choromosome :     # représentation d'une solution , chaque solution est une liste d'affection et chaque affectation est une liste
    #def __init__(self,nb_affecation):   
        #for i in range(nb_affecation):
'''

class Donnees :     # classe qui recenses les données du problème

    def __init__(self):     
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

        self.centers = self.centers.rename(columns={0: 'id'})
        self.centers = self.centers.rename(columns={1: 'nom'})
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

        self.counts_competence = self.centers_employees.groupby(['id_center', 'nom'])['compétence'].value_counts().unstack(fill_value=0) # compte le nombre de compétence LSF et LPC de chaque centre
        print(f"Nombre de Compétence de chaque centre : \n\n {self.counts_competence} \n\n")
        self.counts_specialite = self.centers_employees.groupby(['id_center', 'nom'])['spécialité'].value_counts().unstack(fill_value=0) # compte le nombre de spécialité de chaque centre
        print(print(f"Nombre de Spécialité de chaque centre : \n\n {self.counts_specialite} \n\n"))

#print(centers_Employees.groupby(['compétence','nom']).value_counts())   # affiche qui possèdent des compétences LPC et LSF pour les centre
#print(centers_Employees["compétence"].value_counts())               # compte le nombre d'employé ayant les compétences LSF et LPC total de tous les centres (sans distinction des centres)
#print(centers_Employees.describe())



test = Donnees()
test.traitement_donnees()



