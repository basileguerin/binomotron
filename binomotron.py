import random
import mysql.connector as mysqlpy

user = 'root'
password = 'example'
host = 'localhost'
port = '3307'
database = 'binomotron'

bdd = mysqlpy.connect(user=user, password=password, host=host, port=port, database=database)
cursor = bdd.cursor()

def crea_groupes():
    """Créer des groupes de n personnes à partir d'une liste d'apprenants."""

    #On demande la date
    date = input("Quelle est la date (AAAAMMJJ) du jour ? : ")

    #On récupère la liste des apprenants de la BDD
    query = "SELECT nom_apprenant, prenom_apprenant FROM liste_apprenants" 
    cursor.execute(query)

    #On l'insère dans la liste vide
    liste_apprenants = []
    for i in cursor:
        liste_apprenants.append(i)

    #On mélange la liste d'apprenants
    shuffle = liste_apprenants[:]
    random.shuffle(shuffle)

    #On crée une liste vide pour stocker les binômes
    binomes=[]

    #On récupère la taille de la liste mélangée
    x = len(shuffle)

    #On demande à l'utilisateur combien d'élèves par groupe
    nbraw = input("Combien d'étudiants par groupe ? ")  
    nb = int(nbraw)

    #On remplit la liste binômes
    if ((x >= nb) and (x <= len(shuffle))):
        for i in range(0, len(shuffle), nb):
            binome = shuffle[i:i+nb]
            binomes.append(binome)
    else : 
        print("Pas assez d'étudiants pour faire des groupes de cette taille")
        crea_groupes()

    #Si il y a un étudiant seul on l'ajoute à un groupe
    for binome in binomes:
        if(len(binome)==1):
            ans = input("Il y a un étudiant seul. L'affecter à un groupe ? [y/n] ")
            if(ans == 'y'):
                binomes[0].append(binome[0])
                binomes.remove(binome)

    #On transforme la liste binomes en dictionnaire
    dico = {k:v for k,v in enumerate(binomes)}

    #On stocke les groupes dans la BDD
    n_groupe = 1
    for groupe in dico.values():
        query1 = f"SELECT id_groupe FROM groupes WHERE libelle = 'Groupe{n_groupe}'"
        cursor.execute(query1)
        n_groupe = n_groupe + 1
        for i in cursor:
            id_groupe = i[0]
        for j in range(len(groupe)):
            apprenant = groupe[j]
            query2 = f"SELECT id_apprenant FROM liste_apprenants WHERE (nom_apprenant, prenom_apprenant) = {apprenant}"
            cursor.execute(query2)
            for i in cursor:
                id_apprenant = i[0]
            query3 = f"INSERT INTO apprenants_groupes(id_groupe, id_apprenant, date_creation) VALUES ({id_groupe},{id_apprenant},{date});"
            cursor.execute(query3)
    
    #On commit le tout 
    bdd.commit()
    print("Les groupes aléatoires ont étés ajoutés dans la BDD !")

def recup_mail():
    """Récupérer l'adresse mail d'un étudiant dont on donne le nom via la console
    mail() --> 'xxxx@isen-ouest.yncrea.fr' """

    nom = input("Entrez le nom de l'étudiant : ")
    query = f"SELECT mail_apprenant FROM liste_apprenants WHERE (nom_apprenant = '{nom}');"
    cursor.execute(query)
    for i in cursor:
        mail = i[0]
    print(mail)

def affiche_groupe():
    """Affiche la liste des groupes crées pour une date donnée"""

    date = input("Groupes pour quelle date(AAAA-MM-JJ) ? : ")
    query = f"""SELECT libelle, nom_apprenant, prenom_apprenant
    FROM groupes, apprenants_groupes, liste_apprenants
    WHERE apprenants_groupes.id_apprenant=liste_apprenants.id_apprenant AND apprenants_groupes.id_groupe=groupes.id_groupe AND date_creation ='{date}'"""
    cursor.execute(query)
    for i in cursor:
        print(i[0], i[1], i[2])

#crea_groupes()
#recup_mail()
affiche_groupe()

cursor.close()
bdd.close()