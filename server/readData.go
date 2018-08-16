package main

import (
	"bufio"
	"errors"
	"io"
	"os"
	"strconv"
	"strings"
)

func getNth(n int, setType string) Digit {
	text, err := readNth(setType, n)
	check(err)
	data := strings.Split(text, ",")

	label, err := strconv.Atoi(data[0])
	check(err)

	var pixels PixelArray
	for i := range pixels {
		for j := range pixels[i] {
			currVal, err := strconv.Atoi(data[i*len(pixels[i])+j+1])
			check(err)
			pixels[i][j] = currVal
		}
	}
	return Digit{Label: label, Pixels: pixels}
}

func readNth(setType string, lineNum int) (line string, err error) {
	fileName, errr := decideFile(setType)
	check(errr)
	r, errr := os.Open(fileName)
	check(errr)

	sc := bufio.NewScanner(r)
	currLine := 0
	for sc.Scan() {
		currLine++
		if currLine == lineNum {
			return sc.Text(), sc.Err()
		}
	}
	return line, io.EOF
}

func decideFile(name string) (string, error) {
	if name != "test" && name != "train" {
		return "", errors.New(name + "doesnt exist")
	}
	return "mnist_" + name + ".csv", nil
}
