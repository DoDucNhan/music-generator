from utils import midi_to_notes, notes_to_midi
import pandas as pd
import argparse
import os

# Sending request to API
import requests
import json


BASE = "https://run-model.azurewebsites.net"
# midi file
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="path to input midi file")
ap.add_argument("-o", "--output", default="./", help="path to output midi file")
args = vars(ap.parse_args())

raw_notes = midi_to_notes(args["input"])
print(raw_notes.head())

data = raw_notes.to_dict()
data = json.dumps(data)
response = requests.post(BASE, data)
di = response.json()
generated_notes = pd.DataFrame.from_dict(di)
print(generated_notes.head())

out_file = 'output.mid'
out_pm = notes_to_midi(
    generated_notes, out_file=os.path.join(args["output"], out_file), instrument_name='Acoustic Grand Piano')