### 
#    CONTRAINTES 
###

# optimisation sur une semaine de 5 jours , 7h par jour de travail par personne, 35h/semaine/personne, 
#et une amplitude horaire max de 13 heures (différence entre l'heure de fin de la journée de travail et l'heure de début de la journée de travail)

#Le temps de travail d'un intervenant par jour = temps d'exécution des missions assignées + temps de déplacement. 

import numpy as np
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

        # Charger les fichier CSV en spécifiant que la première ligne est une ligne de données et non pas l'entête 
        self.centers = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\centers.csv" , header=None)         # mettre le bon format fichier + pip install openpyxl

        #Distances : la matrice des distances. Les première lignes représentent la distance entre les centres et les missions. Les premières colonnes représentent la distance entre les missions et les centres. Les autres cases représentent la distance entre les missions
        self.distances = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\distances.csv" , header=None)

        self.employees = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\Employees.csv" , header=None)
        self.missions = pd.read_csv(r"C:\Users\Lucas\Documents\UTBM\Cours\INFO2\IT45\Projet\instances\instances\30Missions-2centres\Missions.csv" , header=None)
        # renommage des colonnes et affichage des données bruts

        self.centers = self.centers.rename(columns={0: 'id'})
        self.centers = self.centers.rename(columns={1: 'nom'})
        #print(f"CENTRE : \n\n {centers} \n \n")

        #print(f"distances : \n\n {distances} \n \n")

        #Employees = Employees.rename(columns={0: 'id'})
        self.employees = self.employees.rename(columns={0: 'id'})
        self.employees = self.employees.rename(columns={1: 'centre_ID'})
        self.employees = self.employees.rename(columns={2: 'compétence'})
        self.employees = self.employees.rename(columns={3: 'spécialité'})
        #print(f"Employees : \n\n {Employees} \n \n")
        #print(Employees.columns)

        self.missions = self.missions.rename(columns={0: 'id'})
        self.missions = self.missions.rename(columns={1: 'jour'})
        self.missions = self.missions.rename(columns={2: 'heure_début'})
        self.missions = self.missions.rename(columns={3: 'heure_fin'})
        self.missions = self.missions.rename(columns={4: 'compétence'})
        self.missions = self.missions.rename(columns={5: 'spécialité'})
        #print(f"Missions : \n\n {Missions} \n \n")


    def traitement_donnees(self):
        #regroupe les employés avec leur centre pour calculer les compétence de chaque centre
        self.centers_employees = pd.merge(self.centers, self.employees, left_on='id', right_on='centre_ID', how='inner', suffixes=('_center' , '_employee')) # chaque employé est associé à son centre dans un nouveau tableau , jointure inner join sur centre_ID
        self.centers_employees = self.centers_employees.drop('centre_ID', axis=1)     # la clé de jointure est supprimé car inutile
        print(self.centers_employees)
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



