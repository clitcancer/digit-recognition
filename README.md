# NN for digit recognition
- download https://pjreddie.com/media/files/mnist_test.csv and https://pjreddie.com/media/files/mnist_train.csv 
- put them into `server/`
- download go and python
- download some c++ compiler
done
## server in GO:
serves data
### GET
- train/test digit data 
	- url `/api/:dataSet/:n`
	- returns `{label: int, pixels: int[28][28]}`

- make guess (todo)
	- url (todo)
	- expects (todo)
	- returns (todo)

---

## NN in python:
trains the NN

---

## guesser in c++:
performs guesses using the trained NN

---

## visualisation in JavaScript
upload pics, shows guess
draw, shows guess

---

## flow
learning python -> JS drawing -> go server -> c++ guess -> go server -> browser
