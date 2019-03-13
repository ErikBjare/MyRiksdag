import json

import agreements

if __name__ == "__main__":
    df = agreements.build_dataframe()
    with open('party_compare.json', 'w+') as f:
        f.write(json.dumps(json.loads(df.to_json()), indent=2))
