#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

mkdir -p $DIR/data/votering
cd $DIR/data/votering

download_data() {
    declare -a years=( #"199899" "19992000" "200001" "200102"  # Not available in JSON
                      "200203" "200304" "200405" "200506"
                      "200607" "200708" "200809" "200910"
                      "201011" "201112" "201213" "201314"
                      "201415" "201415" "201516" "201617" "201718")

    for i in "${years[@]}"
    do
        FILENAME="votering-${i}.json.zip"
        if [ ! -f  $FILENAME ]; then
            wget http://data.riksdagen.se/dataset/votering/votering-${i}.json.zip
        fi
    done
    echo "All data downloaded, to redownload, remove archives in ./data/votering"
}

unpack_data() {
    for i in *.json.zip
    do
        SRCDIR=$(echo ${i} | grep -o "20[0-9]*")
        mkdir $SRCDIR
        unzip -q $i -d $SRCDIR
    done
}


if [ -z "$CI" ]; then
    # This shell is interactive (not in CI)
    while true; do
        read -p "Do you want to download the files? (yes/no): " yn
        case $yn in
            [Yy]* ) download_data; break;;
            [Nn]* ) break;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    while true; do
        read -p "Do you want to unpack the files? (yes/no): " yn
        case $yn in
            [Yy]* ) unpack_data; break;;
            [Nn]* ) break;;
            * ) echo "Please answer yes or no.";;
        esac
    done
else
    # This shell is not interactive (in CI)
    download_data;
    unpack_data;
fi
