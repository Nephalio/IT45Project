### 
#    CONTRAINTES 
###

# optimisation sur une semaine de 5 jours , 7h par jour de travail par personne, 35h/semaine/personne, 
#et une amplitude horaire max de 13 heures (différence entre l'heure de fin de la journée de travail et l'heure de début de la journée de travail)

#Le temps de travail d'un intervenant par jour = temps d'exécution des missions assignées + temps de déplacement. 

import numpy as np
import os
import pandas as pd

import time
import random



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

class Donnees :     # classe qui lit les fichiers et recenses les données du problème





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
        self.centers = pd.read_csv(centers_path, header=None)
        self.distances = pd.read_csv(distances_path, header=None)
        self.employees = pd.read_csv(employees_path, header=None)
        self.missions = pd.read_csv(missions_path, header=None)

        # renommage des colonnes et affichage des données bruts

        self.centers = self.centers.rename(columns={0: 'id'})
        self.centers = self.centers.rename(columns={1: 'nom'})
        #print(f"CENTRE : \n\n {self.centers} \n \n")

        #print(f"distances : \n\n {self.distances} \n \n")

        self.employees = self.employees.rename(columns={0: 'id'})
        self.employees = self.employees.rename(columns={1: 'centre_ID'})
        self.employees = self.employees.rename(columns={2: 'compétence'})
        self.employees = self.employees.rename(columns={3: 'spécialité'})
        #print(f"Employees : \n\n {self.employees} \n \n")
        #print(self.mployees.columns)

        self.missions = self.missions.rename(columns={0: 'id'})
        self.missions = self.missions.rename(columns={1: 'jour'})
        self.missions = self.missions.rename(columns={2: 'heure_début'})
        self.missions = self.missions.rename(columns={3: 'heure_fin'})
        self.missions = self.missions.rename(columns={4: 'compétence'})
        self.missions = self.missions.rename(columns={5: 'spécialité'})
        #print(f"Missions : \n\n {self.missions} \n \n")






    def traitement_donnees(self):

        # tableau déjà construit dans employee
        #regroupe les employés avec leur centre pour calculer les compétence de chaque centre
        self.centers_employees = pd.merge(self.centers, self.employees, left_on='id', right_on='centre_ID', how='inner', suffixes=('_center' , '_employee')) # chaque employé est associé à son centre dans un nouveau tableau , jointure inner join sur centre_ID
        self.centers_employees = self.centers_employees.drop('centre_ID', axis=1)     # la clé de jointure est supprimé car inutile
        #print(self.centers_employees)
        #print("\n")

        # a calculer depuis le tableau employé
        self.counts_competence = self.centers_employees.groupby(['id_center', 'nom'])['compétence'].value_counts().unstack(fill_value=0) # compte le nombre de compétence LSF et LPC de chaque centre
        print(f"Nombre de Compétence de chaque centre : \n\n {self.counts_competence} \n\n")
        self.counts_specialite = self.centers_employees.groupby(['id_center', 'nom'])['spécialité'].value_counts().unstack(fill_value=0) # compte le nombre de spécialité de chaque centre
        print(print(f"Nombre de Spécialité de chaque centre : \n\n {self.counts_specialite} \n\n"))

        # quelques tests d'accès aux données des tableaux
        #print(f'test nombre de spécialité mécanique au centre 2  = {self.counts_specialite.iloc[1,1]} {self.counts_specialite.iat[1,1]}')
        #print(f'test = {self.missions.iat[0,5]}')   #renvoie musique

        #print(centers_Employees.groupby(['compétence','nom']).value_counts())   # affiche qui possèdent des compétences LPC et LSF pour les centre
        #print(centers_Employees["compétence"].value_counts())               # compte le nombre d'employé ayant les compétences LSF et LPC total de tous les centres (sans distinction des centres)
        #print(centers_Employees.describe())

class Population :      # population composé d'ensemble de solution




    def __init__(self,donnees):
        # crée une population initiale
        self.population = []    # liste de solution  
        self.nb_individu = 1

        for k in range(self.nb_individu):         # création de nb_individu solution initiale
            solution = []               # une solution est une liste d'affectation
            planning_employee = Employee(donnees.employees)                   # pour chaque solution ou choromosome un planning des employee y est associé
            for i in range(donnees.missions.shape[0]): #parcours le tableau mission ligne par ligne
                affectation = []            # liste contenant les informations d'une affectation de mission sous la forme [id_employe,mission]

                index_employee_aleatoire = (random.randint(1,donnees.employees.shape[0])  - 1)   # choix d'un id d'employé aléatoire
                competence_mission = donnees.missions.iat[i,4] # accès à la compétence de la mission à la ligne i

                while donnees.employees.iat[index_employee_aleatoire,2] != competence_mission :     # temps que l'employé tiré au hasard n'a pas la bonne compétence on recommence
                    index_employee_aleatoire = (random.randint(1,donnees.employees.shape[0])  - 1)
                
                mission_affecter = planning_employee.est_disponible(index_employee_aleatoire,donnees.missions.iloc[i])     # ligne du tableau de la mission i passée en paramètre
                if(mission_affecter):   # si la mission est affecter alors on l'ajoute dans la liste affectation
                    affectation.append(index_employee_aleatoire+1)  # +1 pour avoir l'id_employé comme dans le jeu de donnée
                    affectation.append(donnees.missions.iloc[i])    # l'affectation prend toutes les données de la mission en question
                    solution.append(affectation)        # le choromosome apprend l'affectation 
                else:
                    print(f"mission {donnees.missions.iat[i,0]} non affecté (planning correspondant une ligne au dessus) \n")

            solution.append(planning_employee)          # le planning des employés associé à la solution est ajouté en fin de liste 
            self.population.append(solution)

    




    def affichage_population(self):
        
        for i in range(len(self.population)):
            #print(self.population[i])
            #print(f"planning_employé = {self.population[i][-1]}")
            self.population[i][-1].affichage_planning()
            print("\n\n\n")
            #for j in range(len(self.population[i])-1):
                #print(f"id_employe = {self.population[i][j][0]} effectue la mission  : id = {self.population[i][j][1][0]} , jour = {self.population[i][j][1][1]} , heure_debut = {self.population[i][j][1][2]} , heure_fin = {self.population[i][j][1][3]}")
            self.population[i][-1].affichage_tournee()
      


class Employee :    # classe qui gère les contraintes des employées




    def __init__(self,employee):

        # les missions peuvent commencer au plus tot à 7h du matin et finir à 20h du soir
        self.nb_jour_semaine = 5
        self.intervalle_temps_planning = 10     # le planning a des itnervalle de temps de 10 minutes
        self.decoupage_horaire = int(60 / self.intervalle_temps_planning)                                  # chaque heure est découpe en 6 intervalle de 10 minute
        self.amplitude_horaire_max_employee = 13*self.decoupage_horaire  # 13 = amplitude horaire max , il y a entre 7h et 20h qu'un employé peut avoir une mission, 1 heure est découpé en 6 intervalle de 10 minute
        self.nb_employee = employee.shape[0]

        # liste représentant le planning de chaque employé , 5 listes de 13 éléments représentant s'il est libre à une heure précise pour chaque employé , ce pour chaque employé
        # ainsi self.employee_horaire[1] représente le planning sur la semaine de l'employée qui a l'id 2 , self.employee_horaire[1][1] est son planning du mardi 
        # si = 0 alors c'est une heure libre , si = 1 alors l'employee n'est pas libre
        self.employee_horaire = [ [ [0 for i in range(self.amplitude_horaire_max_employee)]  for j in range(self.nb_jour_semaine) ] for k in range(self.nb_employee) ]
        #print(self.employee_horaire)   

        # construction de la liste de la tournée de chaque employé pour les 5 jours de la semaine qui commence et finit  sa tournée par son centre auquel il est affecté
        self.tournees_employees = []        
        for i in range(self.nb_employee):   
            l = []  
            for j in range(self.nb_jour_semaine):
                l.append([employee.iat[i,1] , employee.iat[i,1]])           # on affecte le centre de l'employée comme départ et fin de tournée car l'employée part du centre et finit sa tournée en retournant au centre
            self.tournees_employees.append(l)

        # test
        #self.tournees_employees[1][4].append(10)    # l'employé avec l'id = 2 au jour 5 (vendredi) prend la mission 10
        #print(self.tournees_employees)





    def est_disponible(self,id_employee,mission):
        #id_employee = id_employee - 1     # les indices sont décallés

        nb_intervalle_temps_a_verifier = int((mission[3] - mission[2]) / self.intervalle_temps_planning)    # nombre d'intervalle de temps, c'est à dire de case à vérifier
        index_time =  int((mission[2] - 420) / self.intervalle_temps_planning)                               #indice à partir du quelle la liste va commencer a être parcouru

        print(f"index time = {index_time} , heure_début_mission = {mission[2]} , heure_fin = {mission[3]} , nb_intervalle = {nb_intervalle_temps_a_verifier} ")

        ### 
        #   Vérification que l'employé est disponible sur la plage horaire de la mission , 
        #   les contraintes qui ont le plus de chances de ne pas être respecté sont vérifié en premier pour éviter les calculs inutiles
        ###

        # premier parcours de l'horaire correspondant à la mission pour voir si l'employé est disponible 
        for i in range(nb_intervalle_temps_a_verifier):
            if (self.employee_horaire[id_employee][mission[1]-1][index_time] == 1):                 # si un dans l'intervalle une case vaut 1 alors l'employé n'est pas disponible , mission[1] = date 
                    print(f"planning de l'employé pour qui la mission n'est pas affectée à cause qu'une autre mission chevauche une autre sur cette plage horaire = {self.employee_horaire[id_employee][mission[1]-1]}")
                    return False
                    #break                                                                       # l'employee est indisponible sur une tranche horaire couvrant la mission
            index_time +=  1

        ###
        # Vérification que l'employé ne dépasse pas 7h/j 
        ###
        somme_horaire_par_jour = 0
        for i in range(self.amplitude_horaire_max_employee):        # parcours d'une journée
            if (self.employee_horaire[id_employee][mission[1]-1][i] == 1):
                somme_horaire_par_jour += 1
            if( (somme_horaire_par_jour*10 + nb_intervalle_temps_a_verifier*10) >= 420):    # vérifie que la somme des heures déjà travailler + celle de la mission qui pourrait être ajouté ne dépasse pas 7h
                print(f"planning de l'employé pour qui la mission n'est pas affectée car >7h/jour max = {self.employee_horaire[id_employee][mission[1]-1]}")
                return False
            
        ###
        # Vérification que l'employé ne dépasse pas 35h/semaine
        ###
        somme_horaire_par_semaine = somme_horaire_par_jour      # on ne recalcule pas la somme des heures du jour déjà calculé précèdement
        for i in range(self.nb_jour_semaine):
            if (i!= mission[1]-1):                              # on vérifie que le jour en question n'est pas celui de la mission associé qui est déjà calculé
                for j in range(self.amplitude_horaire_max_employee):        # parcours d'une journée
                    if (self.employee_horaire[id_employee][i][j] == 1):
                        somme_horaire_par_semaine += 1
            if( (somme_horaire_par_semaine*10 + nb_intervalle_temps_a_verifier*10) >= 420*self.nb_jour_semaine):    # vérifie que la somme des heures déjà travailler + celle de la mission qui pourrait être ajouté ne dépasse pas 35h
                        print(f"planning de l'employé pour qui la mission n'est pas affectée car >35h/jour max = {self.employee_horaire[id_employee][mission[1]-1]}")
                        return False

        # on rentre dans cette boucle si l'employé est bien disponible et que toutes les contraintes sont respectés, dans ce cas on actualise son planning
        index_time =  int((mission[2] - 420) / self.intervalle_temps_planning) 
        #print(f"index time = {index_time} , heure_début = {mission[2]} , nb_intervalle = {nb_intervalle_temps_a_verifier} ")
        for i in range(nb_intervalle_temps_a_verifier):
            self.employee_horaire[id_employee][mission[1]-1][index_time] = 1                 # si un dans l'intervalle une case vaut 1 alors l'employé n'est pas disponible , mission[1] = date 
            index_time +=  1

        self.tournees_employees[id_employee][mission[1]-1].insert(-1,mission[0])        # insère à l'avant derniere élément juste avant le retour au centre

        print(f"planning de l'employé mis à jour à qui la mission {mission[0]} vient d'etre affectée = {self.employee_horaire[id_employee][mission[1]-1]}")
        print("\n\n")
        return True
    

    def affichage_planning(self):
        for i in range(self.nb_employee):
            for j in range(self.nb_jour_semaine):
                print(f" planning de l'id_employé = {i+1} au jour {j+1} = {self.employee_horaire[i][j]} \n")            # i+1 pour être raccord avec les id et jour des données 
                print(f"{len(self.employee_horaire[i][j])}")

    def affichage_tournee(self):
        for i in range(self.nb_employee):
            for j in range(self.nb_jour_semaine):
                print(f" tournée de l'employé avec l'id = {i+1} au jour {j+1} = {self.tournees_employees[i][j]} \n")            # i+1 pour être raccord avec les id et jour des données 




            


current_time = int(time.time())
random.seed(current_time)

donnees = Donnees()
donnees.traitement_donnees()
print(donnees.missions)
print(donnees.centers)
print(donnees.employees)
# print(donnees.missions.shape[0]) # nb de ligne du tableau mission

#planning_employee = Employee(donnees.employees)
#test = donnees.employees.iloc[0]
#print(test[2])

# test sur la représentation des données
''' 
affectation = []
affectation.append(5)
affectation.append(donnees.missions.iloc[1])    
print(f"affectation = {affectation}")
print(f"affectation = {affectation[0]}")
print(f"affectation competence= {affectation[1][4]}")
'''

population_initial = Population(donnees)
population_initial.affichage_population()




