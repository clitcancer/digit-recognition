DataLoader dataLoader;
Graph graph;

String inputString = "";
int currStep = 0;


void setup() {
  size(1500, 750);
  //fullScreen();
  textAlign(CENTER, CENTER);
  textSize(32);

  dataLoader = new DataLoader("../stats.json");
}

void draw() {
  background(0);

  switch(currStep) {
  case 0:
    text("What activation function should I load?", width/2, height/5);
    text(inputString, width/2, height/2);
    break;

  case 1:
    text("What learning rate should I load?", width/2, height/5);
    text(inputString, width/2, height/2);
    break;

  default:
    graph.drawAvrgLoss();
    graph.drawAccuracy();
    graph.drawLegend();
  }
}

void done() {
  boolean success;

  switch(currStep) {
  case 0:
    success = dataLoader.loadActivation(inputString);
    break;

  case 1:
    success = dataLoader.loadLearningRate(inputString);
    break;

  default:
    success = false;
  }

  if (!success) {
    fill(255, 0, 0);
  } else {
    inputString = "";
    if (++currStep == 2) graph = new Graph(dataLoader.stats);
  }
}

void keyTyped() {
  fill(255);

  if (key == BACKSPACE) inputString = inputString.length() != 0 ? inputString.substring(0, inputString.length() - 1) : "";
  else if (key == ENTER) done();
  else inputString += key;
}
