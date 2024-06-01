# 3D_Face_modelling
## Prerequisiti
 - Sistema operativo linux
 - Scheda grafica Nvidia con supporto CUDA
 - CUDA Toolkit supportato da pytorch
 - Python
   - Conda
   - Pip
 - Node 18.14.2
 - npm
 - MySQL

## Variabili d'ambiente
Per le variabili d'ambiente sono presenti dei file ".env.example" all'interno delle due cartelle frontend e backend. Rimuovere ".example" e inserire dei valori per ogni variabile.

## Avvio App
Come prima cosa bisogna creare il database su cui lavorerà l'applicazione. Basta creare il database vuoto, la struttura verrà creata dall'app.

All'interno della cartella backend creare le cartelle *elaboration* e *tmp_result*.

Prima di avviare l'applicazione del backend bisogna installare le dipendenze.

`conda create -n 3d-face-modelling python=3.9`

`conda activate 3d-face-modelling`

`conda install -c nvidia cuda-python`

`conda install pytorch=1.13.0 torchvision pytorch-cuda=11.6 -c pytorch -c nvidia -c fvcore -c iopath -c conda-forge fvcore iopath pytorch3d -c pytorch3d`

`pip install -r requirements.txt`

Per avviare l'app basta eseguire questo comando.

`python3 app.py` 

Per avviare il frontend invece basta eseguire i seguenti comandi all'interno della cartella frontend.

`npm i`

`npm run dev`

Il sito sarà raggiungibile su "https://localhost:5173"