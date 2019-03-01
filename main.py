#!/usr/bin/python3

import os
import json
import codecs
import logging
import itertools

logging.basicConfig(level=logging.INFO)

DATADIR = "data"


def main():
    votings = get_votings("201314")

    print_agreements(get_agreements(votings))


def _sanitize_party(party):
    # Fixes some issues in the underlying data,
    # such as when Folkpartiet renamed themselves to Liberalerna
    return party if party != 'FP' else 'L'


def print_agreements(agreements):
    for pair in sorted(agreements, key=(lambda a: agreements[a]), reverse=True):
        pairsplit = pair.split("-")
        pairstr = pairsplit[0].ljust(3) + "-" + pairsplit[1].rjust(3)
        print("{}:  ".format(pairstr) + "{}".format(agreements[pair]))


def get_agreements(votings):
    headcount = get_headcount_by_party(next(iter(votings.values())))
    parties = sorted([_sanitize_party(party) for party in headcount.keys()])

    # [("M", "S"), ("V", "SD"), ...]
    party_pairs = list(itertools.combinations(parties, 2))

    agreements = dict(zip(["-".join(pair) for pair in party_pairs], [0] * len(party_pairs)))
    # supported = dict(zip(parties, [0] * len(parties)))

    for key, voting in votings.items():
        votes = get_votes_by_party(voting)
        support = party_support(votes)

        for party_pair in party_pairs:
            # Ensures party is in support dict
            for party in party_pair:
                if party not in support:
                    support[party] = False

            agreements["-".join(party_pair)] += 1 if support[party_pair[0]] == support[party_pair[1]] else 0
    return agreements


def party_support(votes):
    """Returns a dict with the result of the majority funtion for a set of votes grouped by party"""
    support = {}
    for party in votes:
        support[party] = True if votes[party]["Ja"] > votes[party]["Nej"] else False
    return support


def get_headcount_by_party(voting):
    results = {}
    for voter in voting:
        parti = voter["parti"].upper()
        if parti not in results:
            results[parti] = 0
        results[parti] += 1
    return results


def get_votings(yeartag: str):
    results = {}
    directory = DATADIR + "/votering/" + yeartag
    filenames = next(os.walk(directory))[2]

    print("Polls {}: {}".format(yeartag, len(filenames)))

    for filename in filenames:
        logging.debug("Reading file {}".format(filename))
        with codecs.open(directory + "/" + filename, "r", "utf-8-sig") as f:
            data = json.loads(f.read())
            try:
                results[filename] = data["dokvotering"]["votering"]
            except TypeError as e:
                print("Something went wrong while parsing poll, skipping")
                print(data)
                #raise e
    return results


def get_votes_by_party(voting):
    party_votes = {}
    len(voting)

    for voter in voting:
        party = _sanitize_party(voter["parti"].upper())
        if party not in party_votes:
            party_votes[party] = {"Ja": 0, "Nej": 0, "Frånvarande": 0, "Avstår": 0}
        party_votes[party][voter["rost"]] += 1
    return party_votes


if __name__ == "__main__":
    main()
