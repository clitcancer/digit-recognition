import java.util.Map;

class DataLoader {
  JSONObject data;
  JSONObject actData;
  JSONArray lrData;

  DataLoader(String path) {
    data = loadJSONObject(path);
  }

  boolean loadActivation(String name) {
    actData = data.getJSONObject(name);
    return actData != null;
  }

  boolean loadLearningRate(String rate) {
    if (actData == null)
      throw new Error("You need to load the activation first.");

    lrData = actData.getJSONArray(rate);
    return lrData != null;
  }

  ArrayList<HashMap<String, Float>> getData() {
    if (lrData == null)
      throw new Error("You need to load the learning rate first.");

    ArrayList<HashMap<String, Float>> res = new ArrayList<HashMap<String, Float>>();

    String[] keys = new String[]{"accuracy", "avrgLoss", "epoches"};
    try {
      for (int i = 0; i > -1; i++) {
        JSONObject obj = lrData.getJSONObject(i);

        HashMap<String, Float> curr = new HashMap<String, Float>();
        for (String k : keys) 
          curr.put(k, obj.getFloat(k));

        res.add(curr);
      }
    } 
    catch (Exception e) {
    }

    return res;
  }
}
