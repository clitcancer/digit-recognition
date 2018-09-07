# NN for digit recognition
## index
- [usage](#usage)
- [server/](#server-in-go)
- [trainer/](#nn-in-python)
- [guesser/](#guesser-in-c)
- [interaction/](#interaction-in-javascript)
- [visualisation/](#visualisation-in-java)
- [why](#why)
## usage
### preset

- download https://pjreddie.com/media/files/mnist_test.csv and https://pjreddie.com/media/files/mnist_train.csv, put them into `server/`
- download [GO](https://golang.org/dl/)
- download g++ compiler
- download python 3.7 (sorry, no env for now)

### installing
- run the `install.sh` file, if fails do the manual way:
	- run the `go build` command in `server/`
	- run the `g++ *.cpp -o main.exe` command in `guesser/`
	- download these python packages: `pyyaml` and `aiohttp`

### training
- run the go server: `server/server.exe`
- configure your neural net in the `NN_config.yaml` file
- in `trainer/` run the `python main.py <epoch_amount>`
	- flags:
		- `--verbose`: detailed print
		- `--stats`: prints out a JSON containing data about the training session
		- `--reset`: Neural Network wont load the `brain.json` file, will train a new NN
### interaction
- run the go server: `server/server.exe`
- open up `http://localhost:214` in a browser
### visualisation
- run the processing sketch (TODO)

---

## `server/` in GO:
serves data, acts as a http server, communicates with other programs. Runs on `http://localhost:214`
### GET
- train/test digit data 
	- url `/api/getDigit/:dataSet/:n`
	- returns `{label: int, pixels: int[28][28]}`

- make guess
	- url `/api/guess`
	- expects body `{pixels: int[28*28]}`
	- returns `{guess: int}`

- show brain
	- url `/api/data/brain`
	- returns `brain.json`

- static files
	- url `/`
	- returns `interaction/`

---

## NN in python:
trains the NN, logs its loss and precision

---

## guesser in c++:
performs guesses using the trained NN

---

## interaction in JavaScript
upload pics, shows guess
draw, shows guess

---

## visualisation in Java
Draws graphs using the data during the training sessions


---

## why
### so many languages
for fun, wanted to created a project that for once isnt full Node.js lul
### is training so slow
because it has to fetch data of a digit from the GO server which has to compute it. I valued multiple languages over efficiency
