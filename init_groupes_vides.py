import mysql.connector as mysqlpy

user = 'root'
password = 'example'
host = 'localhost'
port = '3307'
database = 'binomotron'

bdd = mysqlpy.connect(user=user, password=password, host=host, port=port, database=database)
cursor = bdd.cursor()

query = "INSERT INTO groupes(libelle) VALUES ('Groupe1'), ('Groupe2'), ('Groupe3'), ('Groupe4'), ('Groupe5'), ('Groupe6'), ('Groupe7');"
cursor.execute(query)

bdd.commit()
cursor.close()
bdd.close()