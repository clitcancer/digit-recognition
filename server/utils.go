package main

import (
	"encoding/json"
)

// Digit stores the data related to a single mnist digit
type Digit struct {
	Label  int        `json:"label"`
	Pixels PixelArray `json:"pixels"`
}

// PixelArray correct size of the digit pixel array
type PixelArray [28][28]int

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func jsonify(data interface{}) string {
	marshalledJSON, err := json.Marshal(data)
	check(err)

	return string(marshalledJSON)
}

func mappify(JSONstring string) (res map[string]interface{}) {
	err := json.Unmarshal([]byte(JSONstring), &res)
	check(err)
	return res
}
