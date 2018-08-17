# NN for digit recognition
## index
- [usage](#usage)
- [server/](#server-in-go)
- [trainer/](#nn-in-python)
- [guesser/](#guesser-in-c++)
- [visualisation/](#visualisation-in-javascript)
- [why](#why-so-many-languages)
## usage
### preset
- download https://pjreddie.com/media/files/mnist_test.csv and https://pjreddie.com/media/files/mnist_train.csv, put them into `server/`
- download GO, run the `go build` command in `server/`, run the created `.exe`
- download g++ compiler, run the `g++ *.cpp -o main.exe` command in `guesser/`
- download python 3.7 (sorry, no env for now)
### training
- configure your neural net in the `NN_config.yaml` file
- in `trainer/` run the `python main.py <epoch_amount>` (TODO)
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
	- expects body `{pixels: int[28][28]}`
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

## why so many languages
for fun, wanted to created a project that isnt full Node.js for once lul
