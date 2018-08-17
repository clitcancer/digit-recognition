package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
)

func sendDigit(w http.ResponseWriter, r *http.Request) {
	params := strings.Split(r.URL.Path, "/")

	wrong := false
	wrong = len(params) != 5 || wrong

	n, err := strconv.Atoi(params[len(params)-1])
	wrong = err != nil || wrong

	_, err = decideFile(params[len(params)-2])
	wrong = err != nil || wrong

	if wrong {
		statusReport(w, r, http.StatusBadRequest)
		return
	}

	fmt.Fprint(w, jsonify(getNth(n, params[len(params)-2]))) // write response to ResponseWriter (w)
}

func sendGuess(w http.ResponseWriter, req *http.Request) {
	type Response struct {
		Guess int `json:"guess"`
	}
	// body, err := ioutil.ReadAll(req.Body)
	// check(err)
	// bodyData := mappify(string(body))
	// fmt.Println(bodyData["Pixels"])

	res := Response{Guess: 2}

	fmt.Fprint(w, jsonify(res))
}

func sendBrain(w http.ResponseWriter, req *http.Request) {
	brain, err := ioutil.ReadFile("../brain.json")
	check(err)
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
	http.Handle("/", http.FileServer(http.Dir("../visualisation/")))
	http.HandleFunc("/api/getDigit/", sendDigit) // :set/:n
	http.HandleFunc("/api/guess", sendGuess)
	http.HandleFunc("/api/data/brain", sendBrain)
	err := http.ListenAndServe(":"+port, nil)
	check(err)
}
