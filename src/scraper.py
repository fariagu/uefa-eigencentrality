#!/usr/bin/env python

from lxml import etree
import csv
import networkx as nx
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)

country_ranking = {}
club_by_country = {}
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

with open('../resources/ClubsByCountry.csv', 'rb') as clubs_by_country:
    reader = csv.reader(clubs_by_country, delimiter=';')
    for row in reader:
        if len(country_ranking) != 0:
            club_by_country[row[0].decode('utf-8')] = row[1]
            if row[1] in country_ranking:
                country_ranking[row[1]]['clubs'][row[0]]= 0.0
            else:
                country_ranking[row[1]] = {'eigencentrality': 0.0, 'clubs': {row[0]: 0.0}}
        else:
            # first 3 bytes of file are garbage
            club_by_country[row[0][3:].decode('utf-8')] = row[1]
            country_ranking[row[1]] = {'eigencentrality': 0.0, 'clubs': {row[0][3:]: 0.0}}

# pp.pprint(club_by_country)

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

for tree in trees:
    homeClubs_raw.extend(tree.xpath(
        '//div[contains(@class, "team-home is-club ")]/div[@class="team-name"]/div/span[@class="fitty-fit"]/text()'))
    awayClubs_raw.extend(tree.xpath(
        '//div[contains(@class, "team-away is-club ")]/div[@class="team-name"]/div/span[@class="fitty-fit"]/text()'))
    homeScore.extend(tree.xpath('//span[contains(@class, "js-team--home-score")]/text()'))
    awayScore.extend(tree.xpath('//span[contains(@class, "js-team--away-score")]/text()'))

for club in homeClubs_raw:
    homeClubs_b.append(club.split("\n          ")[1].split("\n        ")[0].encode("utf-8"))
    homeClubs.append(club.split("\n          ")[1].split("\n        ")[0])

for club in awayClubs_raw:
    awayClubs_b.append(club.split("\n          ")[1].split("\n        ")[0].encode("utf-8"))
    awayClubs.append(club.split("\n          ")[1].split("\n        ")[0])

nodes = set(homeClubs)
nodes_b = set(homeClubs_b)

graph = nx.DiGraph()
graph.add_nodes_from(nodes, Eigencentrality=0)

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

centrality = nx.eigenvector_centrality_numpy(graph, 'weight')

# print country_ranking['Portugal']['eigencentrality']

for node in graph.nodes.iteritems():
    if not 'Eigencentrality' in node[1].keys():
        node[1]['Eigencentrality'] = 0

    node[1]['Eigencentrality'] = np.float64(centrality[node[0]]).item()
    print node[1]['Eigencentrality']

nx.write_gexf(graph, "ResultsGraph.gexf", "utf-8")

for key, value in country_ranking.iteritems():
    clubs = value['clubs']
    for node in centrality:
        if node.encode('utf-8') in clubs:
            clubs[node.encode('utf-8')] += centrality[node]
            value['eigencentrality'] += centrality[node]

# pp.pprint(country_ranking)
# print centrality['Shakhter']
# print len(country_ranking)

with open('ranking_clubs.csv', mode='wb') as club_results_file:
    writer = csv.writer(club_results_file, delimiter=";")
    writer.writerow(['Club', 'Score'])
    for node in centrality:
        writer.writerow([node.encode('utf-8'), format(centrality[node], '.8f')])

with open('ranking_countries.csv', mode='wb') as countries_results_file:
    writer = csv.writer(countries_results_file, delimiter=";")
    writer.writerow(['Country', 'Score'])
    for key, value in country_ranking.iteritems():
        writer.writerow([key, format(value['eigencentrality'], '.8f')])