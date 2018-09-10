package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

// DigitData stores all training and testing set digits
type DigitData struct {
	train [60000]Digit
	test  [10000]Digit
}

// Digit stores the data related to a single mnist digit
type Digit struct {
	Label  int        `json:"label"`
	Pixels PixelArray `json:"pixels"`
}

// PixelArray correct size of the digit pixel array
type PixelArray [28][28]int

func (d DigitData) setExists(name string) bool {
	return name == "train" || name == "test"
}

func (d *DigitData) loadData() {

	f, err := os.Open("mnist_train.csv")
	check(err)

	sc := bufio.NewScanner(f)
	for n := 0; sc.Scan(); n++ {
		data := strings.Split(sc.Text(), ",")

		label, err := strconv.Atoi(data[0])
		check(err)

		for i := range d.train[n].Pixels {
			for j := range d.train[i].Pixels[i] {
				currVal, err := strconv.Atoi(data[i*len(d.train[n].Pixels[i])+j+1])
				check(err)
				d.train[n].Pixels[i][j] = currVal
			}
		}
		d.train[n].Label = label
	}

	f, err = os.Open("mnist_test.csv")
	check(err)

	sc = bufio.NewScanner(f)
	for n := 0; sc.Scan(); n++ {
		data := strings.Split(sc.Text(), ",")

		label, err := strconv.Atoi(data[0])
		check(err)

		for i := range d.test[n].Pixels {
			for j := range d.test[i].Pixels[i] {
				currVal, err := strconv.Atoi(data[i*len(d.test[n].Pixels[i])+j+1])
				check(err)
				d.test[n].Pixels[i][j] = currVal
			}
		}
		d.test[n].Label = label
	}

}
