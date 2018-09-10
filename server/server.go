package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"os/exec"
	"strconv"
	"strings"
)

var digits DigitData

func sendDigit(w http.ResponseWriter, r *http.Request) {
	params := strings.Split(r.URL.Path, "/")

	wrong := false
	wrong = len(params) != 5 || wrong

	n, err := strconv.Atoi(params[len(params)-1])
	wrong = err != nil || wrong

	wrong = !digits.setExists(params[len(params)-2]) || wrong

	if wrong {
		statusReport(w, r, http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	var res Digit
	if params[len(params)-2] == "train" {
		res = digits.train[n]
	} else if params[len(params)-2] == "test" {
		res = digits.test[n]
	}
	fmt.Fprint(w, jsonify(res))
}

func sendGuess(w http.ResponseWriter, req *http.Request) {
	type Response struct {
		Guess int `json:"guess"`
	}

	body, err := ioutil.ReadAll(req.Body)
	check(err)
	bodyData := mappify(string(body))
	squishedNormalizedPixels := jsonify(bodyData["pixels"])

	cmd := exec.Command("..\\guesser\\main.exe", squishedNormalizedPixels)
	var out bytes.Buffer
	cmd.Stdout = &out
	err = cmd.Run()
	check(err)

	answer, err := strconv.Atoi(out.String())
	check(err)

	res := Response{Guess: answer}

	w.Header().Set("Content-Type", "application/json")
	fmt.Fprint(w, jsonify(res))
}

func sendBrain(w http.ResponseWriter, req *http.Request) {
	brain, err := ioutil.ReadFile("../brain.json")
	check(err)

	w.Header().Set("Content-Type", "application/json")
	fmt.Fprint(w, string(brain))
}

func statusReport(w http.ResponseWriter, r *http.Request, status int) {
	w.WriteHeader(status)
	switch status {
	case http.StatusBadRequest:
		fmt.Fprint(w, "bad request 400")
	}
}

func main() {
	port := "214"

	fmt.Println("loading data...")
	digits.loadData()
	fmt.Println("Done. Server started.")

	http.Handle("/", http.FileServer(http.Dir("../interaction/")))
	http.HandleFunc("/api/getDigit/", sendDigit) // :set/:n
	http.HandleFunc("/api/guess", sendGuess)
	http.HandleFunc("/api/data/brain", sendBrain)
	err := http.ListenAndServe(":"+port, nil)
	check(err)
}
