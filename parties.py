from typing import List, Dict
import json

from main import get_votings, TVoting


def get_member_ids(votings: Dict[str, TVoting]) -> List[str]:
    return list(set(vote["intressent_id"] for voting in votings.values() for vote in voting))


def get_member_info(votings: Dict[str, TVoting]) -> Dict[str, Dict]:
    member_info: Dict[str, Dict] = {}
    for voting in votings.values():
        for vote in voting:
            _id = vote['intressent_id']
            if _id not in member_info:
                member_info[_id] = {
                    "id": _id,
                    "name": vote["namn"],
                    "firstname": vote["fornamn"],
                    "lastname": vote["efternamn"],
                    "party": vote["parti"],
                    "valkrets": vote["valkrets"],
                    "valkrets_id": vote["valkretsnummer"],
                    "gender": vote["kon"],
                    "birthyear": vote["fodd"],
                    "votes": {},
                }
            member_info[_id]['votes'][vote['votering_id']] = {'vote': vote['rost']}
            # print(vote)
    return member_info


def get_valkretsar(members) -> Dict[str, Dict]:
    valkretsar: Dict[str, Dict] = {}
    for member_id, member in members.items():
        _id = member['valkrets_id']
        if _id not in valkretsar:
            valkretsar[_id] = {
                'name': member['valkrets'],
                'members': []
            }
        valkretsar[_id]['members'].append(member_id)
    return valkretsar


def _print_debug(votings: Dict[str, TVoting]):
    for voting in votings.values():
        for vote in voting:
            print(voting)


def main() -> None:
    votings = get_votings("201718")
    members = get_member_info(votings)
    valkretsar = get_valkretsar(members)
    # _print_debug(votings)
    # for _id, member in members.items():
    #     print(member)

    with open('members.json', 'w+') as f:
        f.write(json.dumps(members, indent=2, ensure_ascii=False))

    with open('valkretsar.json', 'w+') as f:
        f.write(json.dumps(valkretsar, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
