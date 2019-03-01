#!/usr/bin/python3

from main import get_votings, get_agreements

from matplotlib import pyplot as plt
import numpy as np
import argparse


def rainbow_colors(n):
    colormap = plt.cm.gist_rainbow
    return [colormap(i) for i in np.linspace(0, 1, n)]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', default='', help='filter on a specific party')
    return parser.parse_args()


# TODO: Refactor, extract functions, use arguments instead of relying on functions in main.py
def plot(args):
    yearids = [f"20{str(n).rjust(2, '0')}{str(n + 1).rjust(2, '0')}" for n in range(2, 18)]
    print("Plotting for year {} through {}".format(yearids[0], yearids[-1]))

    agreements_by_year = {}
    n_votings = {}
    for yearid in yearids:
        votings = get_votings(yearid)
        agreements_by_year[yearid] = get_agreements(votings)
        n_votings[yearid] = len(votings)

    party_pairs = agreements_by_year[yearids[-1]].keys()

    # Set to None or "" to not filter by party
    filter_party = args.filter

    def includes_party(pair):
        has_party = filter_party in pair.split("-") if filter_party else True
        return pair[0] != "-" and has_party

    party_pairs = sorted(list(filter(includes_party, party_pairs)))
    print("Party pairs: {}".format(party_pairs))

    # Set a colormap that is easier to differentiate from
    plt.gca().set_prop_cycle('color', rainbow_colors(len(party_pairs)))

    lines = []
    for party_pair in party_pairs:
        agreements = []
        for yearid in sorted(agreements_by_year.keys()):
            try:
                agreements.append(100 * agreements_by_year[yearid][party_pair] / n_votings[yearid])
            except KeyError:
                # If one if the parties in the pair is missing from data
                agreements.append(None)
        lines.append(plt.plot(range(len(yearids)), agreements, label=party_pair))

    plt.title("Percentage of polls where a pair of parties respective majority voted the same")
    plt.style.use('ggplot')

    plt.xlabel("Year")
    plt.xlim(0, len(yearids) - 1)
    plt.xticks(range(len(yearids)), [yid[:-2] for yid in yearids])

    plt.ylabel("")
    plt.ylim(0, 100)
    plt.yticks(np.linspace(0, 100, 6), ["", "20%", "40%", "60%", "80%", "100%"])

    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.setp(lines, linewidth=3)

    plt.show(lines)


if __name__ == "__main__":
    args = get_args()
    plot(args)
