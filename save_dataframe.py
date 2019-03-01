import agreements

if __name__ == "__main__":
    df = agreements.build_dataframe()
    df.to_json('party_compare.json')
