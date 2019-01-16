from elopy import *
import csv
import pandas
import numpy
import unicodecsv

clubs = []
score = []
results = []
rating = []
hometeam = []
awayteam = []
final = []
csv_file = "../ranking_clubs.csv"
results_file = "../results.csv"

with open(csv_file) as f:
	csv_reader = csv.reader(f,delimiter=';')
	next(csv_reader, None)
    	for row in csv_reader:
        	clubs.append(row[0])

with open(csv_file) as f:
	csv_reader = csv.reader(f,delimiter=';')
	next(csv_reader, None)
    	for row in csv_reader:
        	rating.append(row[1])

with open(results_file) as f:
	csv_reader = csv.reader(f,delimiter=';')
	next(csv_reader, None)
    	for row in csv_reader:
        	hometeam.append(row[0])

with open(results_file) as f:
	csv_reader = csv.reader(f,delimiter=';')
	next(csv_reader, None)
    	for row in csv_reader:
        	awayteam.append(row[1])

with open(results_file) as f:
	csv_reader = csv.reader(f,delimiter=';')
	next(csv_reader, None)
    	for row in csv_reader:
        	results.append(row[2])


i = Implementation()

x=0
while x < len(clubs):
	i.addPlayer(clubs[x],rating=1500)
	x +=1

t=0
o=0

while t < len(results):
	if results[t] == 'Draw':
		i.recordMatch(hometeam[o],awayteam[o],draw=True)
		o+=1
		t+=1
	elif results[t] == 'Win':
		i.recordMatch(hometeam[o],awayteam[o],winner=hometeam[o])
		o+=1
		t+=1
	elif results[t] == 'Loss':
		i.recordMatch(hometeam[o],awayteam[o],winner=awayteam[o])
		o+=1
		t+=1
	else:
		break

final = i.getRatingList()

with open('elodefault1500.csv', mode='wb') as elo_file:
	writer = csv.writer(elo_file, delimiter=";")
	writer.writerow(['Teams', 'Elo Rating'])   # Header
	for elem in final:
		print(elem[0])
		writer.writerow([elem[0], elem[1]])

#print i.getPlayerRating(clubs[0]), i.getPlayerRating("Bill")


#i.recordMatch(clubs[0],"Bill",draw=True)
"""
y=0
w=0
z=0



while y < len(results)-10:
	while z < len(clubs):
		if w == len(hometeam):
				break
		else:
				if clubs[z] == hometeam[w]:
							if results[y] == 'Draw':
								while t < len(clubs):
									print ("got here")
									print(clubs[z])
									print(awayteam[o])
									if clubs[t] == awayteam[o]:
										i.recordMatch(clubs[z],clubs[t],draw=True)
										y+=1
										w+=1
										z=0
										o+=1
										t=0
										print ("got draw")
										break
									else:
										t+=1
										break
							elif results[y] == 'Win':
								while t < len(clubs):
									print ("got here2")
									print(clubs[z])
									print(awayteam[o])
									if clubs[t] == awayteam[o]:
										print("got on win")
										i.recordMatch(clubs[z],clubs[t],winner=clubs[z])
										y+=1
										w+=1
										z=0
										o+=1
										t=0
										print ("got win")
										break
									else:
										t+=1
										break
							elif results[y] == 'Loss':
								while t < len(clubs):
									print(clubs[z])
									print ("got here3")
									if clubs[t] == awayteam[o]:
										print(clubs[z])
										print(clubs[t])
										i.recordMatch(clubs[z],clubs[t],winner=clubs[t])
										y+=1
										w+=1
										z=0
										o+=1
										t=0
										print ("got loss")
									else:
										t+=1
										break
				else:
					z+=1		

print results[0]
print y
print w
print z

print i.getRatingList()
"""