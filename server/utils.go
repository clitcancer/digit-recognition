package main

import (
	"encoding/json"
)

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
