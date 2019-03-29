import argparse
import csv
import os
import glob
import json
from urllib import request

ID_MAPPING_URL = "http://mac.citi.sinica.edu.tw/ikala/id_mapping.txt"
IKALA_INDEX_PATH = "../mir_dataset_loaders/indexes/ikala_index.json"


def make_ikala_index(ikala_data_path):
    lyrics_dir = os.path.join(ikala_data_path, "Lyrics")
    lyrics_files = glob.glob(os.path.join(lyrics_dir, "*.lab"))
    track_ids = sorted(
        [os.path.basename(f).split('.')[0] for f in lyrics_files])

    id_map_path = os.path.join(ikala_data_path, "id_mapping.txt")

    request.urlretrieve(ID_MAPPING_URL, filename=id_map_path)

    with open(id_map_path, 'r') as fhandle:
        reader = csv.reader(fhandle, delimiter='\t')
        singer_map = {}
        for line in reader:
            if line[0] == 'singer':
                continue
            singer_map[line[1]] = line[0]

    ikala_index = {k: {} for k in track_ids}
    for key in ikala_index.keys():
        songid = key.split('_')[0]
        ikala_index[key]['singer_id'] = singer_map[songid]
        ikala_index[key]['song_id'] = key.split('_')[0]
        ikala_index[key]['section'] = key.split('_')[1]
        ikala_index[key]['audio_path'] = "iKala/Wavfile/{}.wav".format(key)
        ikala_index[key]['pitch_path'] = "iKala/PitchLabel/{}.pv".format(key)
        ikala_index[key]['lyrics_path'] = "iKala/Lyrics/{}.lab".format(key)

    with open(IKALA_INDEX_PATH, 'w') as fhandle:
        json.dump(ikala_index, fhandle, indent=2)


def main(args):
    make_ikala_index(args.ikala_data_path)


with __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Make IKala index file.")
    PARSER.add_argument("ikala_data_path",
                        type=str,
                        help="Path to IKala data folder.")

    main(PARSER.parse_args())