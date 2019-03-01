#!/usr/bin/python3

import argparse
from typing import Optional, Tuple, List, Dict

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from main import get_votings, get_agreements


def rainbow_colors(n: int) -> List:
    colormap = plt.cm.gist_rainbow
    return [colormap(i) for i in np.linspace(0, 1, n)]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', default='', help='filter on a specific party')
    return parser.parse_args()


def build_agreements_by_year(yearids) -> Tuple[Dict[str, dict], Dict[str, int]]:
    agreements_by_year = {}
    n_votings = {}
    for yearid in yearids:
        votings = get_votings(yearid)
        agreements_by_year[yearid] = get_agreements(votings)
        n_votings[yearid] = len(votings)
    return agreements_by_year, n_votings


def build_dataframe():
    yearids = [f"20{str(n).rjust(2, '0')}{str(n + 1).rjust(2, '0')}" for n in range(2, 5)]
    agreements_by_year, n_votings = build_agreements_by_year(yearids)

    party_pairs = _party_pairs(agreements_by_year)
    print("Party pairs: {}".format(party_pairs))

    df = pd.DataFrame(index=yearids)
    df["total"] = n_votings.values()
    for party_pair in party_pairs:
        df[party_pair] = pd.Series()
        for year in agreements_by_year.keys():
            agreements = agreements_by_year[year]
            if party_pair in agreements:
                df[party_pair][year] = agreements_by_year[year][party_pair]
        df[party_pair] = 100 * df[party_pair] / df["total"]
    return df


def _party_pairs(agreements_by_year, filter_party: str = None):
    last_year = sorted(agreements_by_year.keys())[-1]
    party_pairs = agreements_by_year[last_year].keys()

    def includes_party(pair: str, filter_party: Optional[str]):
        has_party = filter_party in pair.split("-") if filter_party else True
        return pair[0] != "-" and has_party

    return sorted([pair for pair in party_pairs if includes_party(pair, filter_party)])


# TODO: Refactor, extract functions, use arguments instead of relying on functions in main.py
def plot(args):
    df = build_dataframe()
    yearids = df.index.values

    # print("Plotting for year {} through {}".format(yearids[0], yearids[-1]))

    df.drop('total', axis=1).plot()

    # Set a colormap that is easier to differentiate from
    #plt.gca().set_prop_cycle('color', rainbow_colors(len(party_pairs)))

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

    plt.show()


if __name__ == "__main__":
    args = get_args()

    plot(args)
    """
    if args.command == "json":


    elif args.command == "plot":
        plot(args)
        """
