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
	i.addPlayer(clubs[x],rating=float(rating[x]))
	x +=1

i.addPlayer("Hank") #default ranking is 1000
i.addPlayer("Bill",rating=900)

#print i.getPlayerRating(clubs[0]), i.getPlayerRating("Bill")

#i.recordMatch("Hank","Bill",winner="Hank")

#print i.getRatingList()

#i.recordMatch("Hank","Bill",winner="Bill")

#print i.getRatingList()

#i.recordMatch(clubs[0],"Bill",draw=True)

y=0
w=0
z=0
t=0
o=0


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