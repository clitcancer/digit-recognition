# NN for digit recognition
## index
- [usage](#usage)
- [server/](#server-in-go)
- [trainer/](#nn-in-python)
- [guesser/](#guesser-in-c)
- [visualisation/](#visualisation-in-javascript)
- [why](#why)
## usage
### preset

- download https://pjreddie.com/media/files/mnist_test.csv and https://pjreddie.com/media/files/mnist_train.csv, put them into `server/`
- download [GO](https://golang.org/dl/)
- download g++ compiler
- download python 3.7 (sorry, no env for now)

### installing
- run the `install.sh` file, if fails do the manual way:
	- run the `go build` command in `server/`, run the created `.exe`
	- run the `g++ *.cpp -o main.exe` command in `guesser/`
	- download these python packages: `pyyaml` and `aiohttp`

### training
- configure your neural net in the `NN_config.yaml` file
- in `trainer/` run the `python main.py <epoch_amount>`
### interaction
- open up `http://localhost:214` in a browser

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
	- returns `visualisation/`

---

## NN in python:
trains and returns the precision of the NN

---

## guesser in c++:
performs guesses using the trained NN

---

## visualisation in JavaScript
upload pics, shows guess
draw, shows guess

---

## why
### so many languages
for fun, wanted to created a project that for once isnt full Node.js lul
### is training so slow
because it has to fetch data of a digit from the GO server which has to compute it. I valued multiple languages over efficiency
