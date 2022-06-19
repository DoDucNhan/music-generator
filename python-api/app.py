from flask_restful import Api, Resource
from flask import Flask, request
from flask_cors import CORS
import tensorflow as tf
import pandas as pd
import numpy as np

# Sending request to API
import requests
import json


def predict_next_note(
    notes: np.ndarray, 
    endpoint: str, 
    temperature: float = 1.0) -> int:
  """Generates a note IDs using a trained sequence model."""

  assert temperature > 0

  # Add batch dimension
  inputs = tf.expand_dims(notes, 0)
  headers = {"Content-Type": "application/json"}
  data = {
      "inputs": inputs.numpy().tolist()
  }
  data = json.dumps(data)

  response = requests.post(endpoint, data=data, headers=headers)
  predictions = response.json()['outputs']
  pitch_logits = np.array(predictions['pitch'])
  step = np.array(predictions['step'])
  duration = np.array(predictions['duration'])
 
  pitch_logits /= temperature
  pitch = tf.random.categorical(pitch_logits, num_samples=1)
  pitch = tf.squeeze(pitch, axis=-1)
  duration = tf.squeeze(duration, axis=-1)
  step = tf.squeeze(step, axis=-1)

  # `step` and `duration` values should be non-negative
  step = tf.maximum(0, step)
  duration = tf.maximum(0, duration)

  return int(pitch), float(step), float(duration)


app = Flask(__name__)
CORS(app)
api = Api(app)

endpoint = "http://8b7b98b5-3d64-46c3-ada4-41914c92ec98.eastus2.azurecontainer.io/v1/models/music-tf-model:predict"

temperature = 2.0
num_predictions = 120
seq_length = 5
vocab_size = 128

key_order = ['pitch', 'step', 'duration']


class ReturnMidi(Resource):
    def post(self):
        data = request.data
        di = json.loads(data)
        raw_notes = pd.DataFrame.from_dict(di)

        sample_notes = np.stack([raw_notes[key] for key in key_order], axis=1)

        # The initial sequence of notes; pitch is normalized similar to training
        # sequences
        input_notes = (
            sample_notes[:seq_length] / np.array([vocab_size, 1, 1]))

        generated_notes = []
        prev_start = 0
        for _ in range(num_predictions):
            pitch, step, duration = predict_next_note(input_notes, endpoint, temperature)
            start = prev_start + step
            end = start + duration
            input_note = (pitch, step, duration)
            generated_notes.append((*input_note, start, end))
            input_notes = np.delete(input_notes, 0, axis=0)
            input_notes = np.append(input_notes, np.expand_dims(input_note, 0), axis=0)
            prev_start = start

        generated_notes = pd.DataFrame(
            generated_notes, columns=(*key_order, 'start', 'end'))
        return generated_notes.to_dict()


api.add_resource(ReturnMidi, "/")


if __name__ == "__main__":
    app.run()