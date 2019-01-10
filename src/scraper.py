#!/usr/bin/env python

from lxml import etree
import csv
import networkx as nx
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)

country_ranking = {}
club_by_country = {}
club_list_raw = []
club_list = []
country_list = []
homeClubs_raw = []
awayClubs_raw = []
homeScore = []
awayScore = []
homeClubs_b = []
homeClubs = []
awayClubs_b = []
awayClubs = []
homeClubsScore = []
awayClubsScore = []

tree_legacy_ranking = etree.parse("../resources/legacy_ranking.html")

trees = [
    etree.parse("../resources/el-2014.html"),
    etree.parse("../resources/el-2015.html"),
    etree.parse("../resources/el-2016.html"),
    etree.parse("../resources/el-2017.html"),
    etree.parse("../resources/el-2018.html"),
    etree.parse("../resources/cl-2014.html"),
    etree.parse("../resources/cl-2015.html"),
    etree.parse("../resources/cl-2016.html"),
    etree.parse("../resources/cl-2017.html"),
    etree.parse("../resources/cl-2018.html")
]

# transcribing list of clubs and another list with their respective country
club_list_raw.extend(tree_legacy_ranking.xpath('//a[@class="team-name visible-sm visible-xs"]/text()'))
# country_list.extend(tree_legacy_ranking.xpath('//td[@class="table_member-country"]/text()'))

with open('ranking_clubs_legacy.csv', mode='wb') as club_ranking_legacy_file:
    writer = csv.writer(club_ranking_legacy_file, delimiter=";")
    # writer.writerow(['Club']) # Header
    for club in club_list_raw:
        # cleaning excess characters
        club_name = club.split("\n                    ")[1].split("\n        ")[0]
        writer.writerow([club_name.encode('utf-8')])

# # initializing country_ranking dictionary (not in use: some clubs aren't listed)
# for club, country in zip(club_list, country_list):
#     if len(country_ranking) != 0 and country in country_ranking:
#         country_ranking[country]['clubs'][club] = 0.0
#     else:
#         country_ranking[country] = {'eigencentrality': 0.0, 'clubs': {club: 0.0}}

# Some clubs that played games in the last five years aren't listed in the uefa ranking page:
# "https://pt.uefa.com/memberassociations/uefarankings/club/#/yr/2019"
# So the club->country association is made from this manually compile csv file
with open('../resources/ClubsByCountry.csv', 'rb') as clubs_by_country:
    reader = csv.reader(clubs_by_country, delimiter=';')
    for row in reader:
        if len(country_ranking) != 0:
            club_by_country[row[0].decode('utf-8')] = row[1]
            if row[1] in country_ranking:
                country_ranking[row[1]]['clubs'][row[0]] = 0.0
            else:
                country_ranking[row[1]] = {'eigencentrality': 0.0, 'clubs': {row[0]: 0.0}}
        else:
            # first 3 bytes of file are garbage
            club_by_country[row[0][3:].decode('utf-8')] = row[1]
            country_ranking[row[1]] = {'eigencentrality': 0.0, 'clubs': {row[0][3:]: 0.0}}

# uncomment to visualize dictionary structure
# pp.pprint(country_ranking)

# parsing match results from html files
# "https://pt.uefa.com/uefachampionsleague/history/season=2018/matches/#/all"   (2014-2018)
# "https://pt.uefa.com/uefaeuropaleague/history/season=2018/matches/#/all"      (2014-2018)
for tree in trees:
    homeClubs_raw.extend(tree.xpath(
        '//div[contains(@class, "team-home is-club ")]/div[@class="team-name"]/div/span[@class="fitty-fit"]/text()'))
    awayClubs_raw.extend(tree.xpath(
        '//div[contains(@class, "team-away is-club ")]/div[@class="team-name"]/div/span[@class="fitty-fit"]/text()'))
    homeScore.extend(tree.xpath('//span[contains(@class, "js-team--home-score")]/text()'))
    awayScore.extend(tree.xpath('//span[contains(@class, "js-team--away-score")]/text()'))

# cleaning excess characters
for club in homeClubs_raw:
    homeClubs_b.append(club.split("\n          ")[1].split("\n        ")[0].encode("utf-8"))
    homeClubs.append(club.split("\n          ")[1].split("\n        ")[0])

for club in awayClubs_raw:
    awayClubs_b.append(club.split("\n          ")[1].split("\n        ")[0].encode("utf-8"))
    awayClubs.append(club.split("\n          ")[1].split("\n        ")[0])

# convert to set to eliminate duplicate values
nodes = set(homeClubs)
nodes_b = set(homeClubs_b)

# initialize graph
graph = nx.DiGraph()
graph.add_nodes_from(nodes, Eigencentrality=0)

# home win: home <- away                    (edge weight = 2)
# away win: home -> away                    (edge weight = 2)
# draw:     home <- away and home -> away   (edge weight = 1 each)
# for subsequent matches between the same teams: no edge added, weight incremented
for home, away, scoreHome, scoreAway in zip(homeClubs, awayClubs, homeScore, awayScore):
    if scoreHome > scoreAway:  # home win
        if graph.has_edge(away, home):
            graph[away][home]['weight'] += 2
        else:
            graph.add_edge(away, home, weight=2, color=club_by_country[home])
    elif scoreHome < scoreAway:  # away win
        if graph.has_edge(home, away):
            graph[home][away]['weight'] += 2
        else:
            graph.add_edge(home, away, weight=2, color=club_by_country[away])
    else:  # draw
        if graph.has_edge(away, home):
            graph[away][home]['weight'] += 1
        else:
            graph.add_edge(away, home, weight=1, color=club_by_country[home])

        if graph.has_edge(home, away):
            graph[home][away]['weight'] += 1
        else:
            graph.add_edge(home, away, weight=1, color=club_by_country[away])

# calculate weighted eigenvector centrality
centrality = nx.eigenvector_centrality_numpy(graph, 'weight')

# format result in order to print to file
for node in graph.nodes.iteritems():
    if 'Eigencentrality' not in node[1].keys():
        node[1]['Eigencentrality'] = 0

    node[1]['Eigencentrality'] = np.float64(centrality[node[0]]).item()
    # print(node[1]['Eigencentrality'])

# write graph in format readable by gephi
nx.write_gexf(graph, "ResultsGraph.gexf", "utf-8")

# aggregate each club's eigencentrality score into the country's score (sum)
for key, value in country_ranking.iteritems():
    clubs = value['clubs']
    for node in centrality:
        if node.encode('utf-8') in clubs:
            clubs[node.encode('utf-8')] += centrality[node]
            value['eigencentrality'] += centrality[node]

# write club ranking to csv file
with open('ranking_clubs.csv', mode='wb') as club_results_file:
    writer = csv.writer(club_results_file, delimiter=";")
    writer.writerow(['Club', 'Score'])  # Header
    for node in centrality:
        writer.writerow([node.encode('utf-8'), format(centrality[node], '.8f')])

# write country ranking to csv file
with open('ranking_countries.csv', mode='wb') as countries_results_file:
    writer = csv.writer(countries_results_file, delimiter=";")
    writer.writerow(['Country', 'Score'])   # Header
    for key, value in country_ranking.iteritems():
        writer.writerow([key, format(value['eigencentrality'], '.8f')])
