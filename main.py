#!/usr/bin/python3


import os
import json
import codecs
import logging

logging.basicConfig(level=logging.INFO)

DATADIR = "data"


def main():
    votings = get_votings("201314")

    headcount = get_headcount_by_party(next(iter(votings.values())))
    parties = list(headcount.keys())

    supported = dict(zip(parties, [0]*len(parties)))

    for key, voting in votings.items():
        votes = get_votes_by_party(voting)
        support = party_support(votes)

        for party in support:
            if party not in supported:
                supported[party] = 0
            supported[party] += 1 if support[party] else 0
    
    print(supported)
    

def party_support(votes):
    support = {}
    for party in votes:
        support[party] = True if votes[party]["Ja"] > votes[party]["Nej"] else False
    return support

def get_headcount_by_party(voting):
    results = {}
    for voter in voting:
        if voter["parti"] not in results:
            results[voter["parti"]] = 0
        results[voter["parti"]] += 1
    return results


def get_votings(year: "denotes starting yeartag"):
    results = {}
    directory = DATADIR + "/votering-"+year
    filenames = next(os.walk(directory))[2]

    print("Polls: {}".format(len(filenames)))

    for filename in filenames:
        logging.debug("Reading file {}".format(filename))
        with codecs.open(directory + "/" + filename, "r", "utf-8-sig") as f:
            results[filename] = json.loads(f.read())["dokvotering"]["votering"]
    return results


def get_votes_by_party(voting):
    party_votes = {}
    len(voting)
    for voter in voting:
        if voter["parti"] not in party_votes:
            party_votes[voter["parti"]] = {"Ja": 0, "Nej": 0, "Frånvarande": 0, "Avstår": 0}
        party_votes[voter["parti"]][voter["rost"]] += 1
    return party_votes


if __name__ == "__main__":
    main()
