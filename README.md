# Music Generator
This is a project for Microsoft Hackathon. It can generate music notes from a sequence of the input midi file using Tensorflow deep learning model. 

Sample output midi file is [here](https://drive.google.com/file/d/1aqx1Je8cSnFwTvafKP6v99OR53gjj70F/view?usp=sharing).

## Setups
1. Clone the repository:
```
 git clone https://github.com/DoDucNhan/music-generator.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Run project
Run the following command.
```
python generate.py -i <input-path> -o <output-path>
```
- `-i`: path to input midi file.
- `-o`: path for output midi file.

## Tensorflow LSTM model 
- Using the LSTM deep learning model for music generator. You can take a look at my [colab notebook](https://colab.research.google.com/drive/1ZUaj22NsXdvSCv0iqMgFo--lryqzNk8y?authuser=3) or Tensorflow guideline [here](https://www.tensorflow.org/tutorials/audio/music_generation). 
- Code for model training and deployment are in `train-deploy` folder.

## Python API
- Using Flask framework to create a simple API for generating music notes.
- Code for flask API is in `python-api` folder.

## Resources
1. Music generator model is deployed through **Azure Machine Learning** service. Instruction can be found [here](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python).
2. Generate notes API is deployed through **Azure App Services**. Instruction can be found [here](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cterminal-bash%2Clocal-git-deploy%2Cdeploy-instructions-azportal%2Cdeploy-instructions-zip-azcli)
3. You can learn more about Flask [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
