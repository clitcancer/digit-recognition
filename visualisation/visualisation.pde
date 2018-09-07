DataLoader data;
String inputString = "";

void setup() {
  // load file with data
  size(100, 100);
  background(100, 0, 200);

  data = new DataLoader("../stats.json");
  data.loadActivation("ReLU");
  data.loadLearningRate("0.1");
  print(data.getData());
}

void draw() {
  // graph the data
  background(0);
  text(inputString, 50, 50);
}

void done() {
}

void keyTyped() {
  if (key == BACKSPACE) inputString = inputString.substring(0, inputString.length() - 1);
  else if (key == ENTER) done();
  else inputString += key;
}
