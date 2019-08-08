# Validators analysis

## Installation and startup

To run containers, use a command:
```bash
$ docker-compose up
```

This command will start crawler and prepare notebook with calculations. To see table with validators' balances and explanatory calculations, click this link: http://localhost:8888/notebooks/notebook/balances.ipynb. 

The token will be requested, it can be found in the output of docker-compose command:
```
[I 00:15:36.448 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
notebook_1  | [C 00:15:36.448 NotebookApp] 
notebook_1  |     
notebook_1  |     Copy/paste this URL into your browser when you connect for the first time,
notebook_1  |     to login with a token:
notebook_1  |         http://(m-Inspiron-7577 or 127.0.0.1):8888/?token=903b1dd72d8b9c95c839c75162208a1a8147b270e6aa3208
```
