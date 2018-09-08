class Graph {
  int length = 0;

  String[] fields = new String[]{"epoches", "avrgLoss", "accuracy"};

  float[] avrgLoss, accuracy, epoche;
  float avrgLossSum, accuracySum, epocheSum;
  float avrgLossMax, accuracyMax, epocheMax;
  float avrgLossMin, accuracyMin, epocheMin;

  float pxPerEpoche;

  Graph(ArrayList<HashMap<String, Float>> data) {
    epocheMax = data.get(0).get("epoches");  
    avrgLossMax = data.get(0).get("avrgLoss");  
    accuracyMax = data.get(0).get("accuracy");  

    epocheMin = data.get(0).get("epoches");  
    avrgLossMin = data.get(0).get("avrgLoss");  
    accuracyMin = data.get(0).get("accuracy");

    for (HashMap<String, Float> t : data) {
      float e = t.get("epoches");
      float av = t.get("avrgLoss");
      float ac = t.get("accuracy");

      epocheSum += e;
      avrgLossSum += av;
      accuracySum += ac;

      epocheMax = e > epocheMax ? e : epocheMax;  
      avrgLossMax = av > avrgLossMax ? av : avrgLossMax;  
      accuracyMax = ac > accuracyMax ? ac : accuracyMax;  

      epocheMin = e < epocheMin ? e : epocheMin;  
      avrgLossMin = av < avrgLossMin ? av : avrgLossMin;  
      accuracyMin = ac < accuracyMin ? ac : accuracyMin;  

      length++;
    }

    avrgLoss = new float[length];
    accuracy = new float[length];
    epoche = new float[length];

    for (int i = 0; i < length; i++) {
      avrgLoss[i] = data.get(i).get("avrgLoss");
      accuracy[i] = data.get(i).get("accuracy");
      epoche[i] = data.get(i).get("epoches");
    }

    pxPerEpoche = width / this.epocheSum;
  }

  void drawAvrgLoss() {
    pushStyle();
    stroke(66, 134, 244);
    strokeWeight(3);
    noFill();

    int currEpoches = 0;

    beginShape();

    curveVertex(0, height - height*this.avrgLoss[0]);
    for (int i = 0; i < this.length; i++) {
      currEpoches += this.epoche[i];
      float x = currEpoches*pxPerEpoche - 50;
      float y = height - this.avrgLoss[i]*height;
      
      pushStyle();
      stroke(150, 100);
      strokeWeight(2);
      line(x, y, x, height - 23);
      popStyle();
      
      curveVertex(x, y);
    }
    curveVertex(width, height - height*this.avrgLoss[this.length-1]);

    endShape();
    popStyle();
  }

  void drawAccuracy() {
    pushStyle();
    stroke(66, 244, 92);
    strokeWeight(3);
    noFill();

    int currEpoches = 0;

    beginShape();

    curveVertex(0, height - height*this.accuracy[0]);
    for (int i = 0; i < this.length; i++) {
      currEpoches += this.epoche[i];
      
      float x = currEpoches*pxPerEpoche - 50;
      float y = height - this.accuracy[i]*height;
      
      pushStyle();
      stroke(150, 100);
      strokeWeight(2);
      line(x, y, x, height - 23);
      popStyle();
      
      curveVertex(x, y);
    }
    curveVertex(width, height - height*this.accuracy[this.length-1]);

    endShape();
    popStyle();
  }


  void drawLegend() {
    pushStyle();
    fill(255);
    textSize(24);
    textAlign(CENTER, CENTER);

    int currEpoches = 0;

    for (int i = 0; i < this.length; i++) {
      currEpoches += this.epoche[i];
      text(currEpoches/1000 + "k", currEpoches*pxPerEpoche - 50, height - 15);
    }

    popStyle();
  }
}
