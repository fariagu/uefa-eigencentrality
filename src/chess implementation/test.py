from elopy import *
from numpy import genfromtxt


club_ranking = genfromtxt('../ranking_clubs.csv', delimiter=',')
results_data = genfromtxt('../results.csv', delimiter=',')

print(', '.join(club_ranking))

i = Implementation()

i.addPlayer("Hank")
i.addPlayer("Bill",rating=900)

print i.getPlayerRating("Hank"), i.getPlayerRating("Bill")

i.recordMatch("Hank","Bill",winner="Hank")

print i.getRatingList()

i.recordMatch("Hank","Bill",winner="Bill")

print i.getRatingList()

i.recordMatch("Hank","Bill",draw=True)

print i.getRatingList()

i.removePlayer("Hank")

print i.getRatingList()