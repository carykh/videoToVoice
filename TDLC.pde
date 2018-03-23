int img = 90000;
PFont font;
String[] phos;
String[] keys;
void setup(){
  phos = loadStrings("/media/rob/Ma Book1/CS 230/videoToVoice/3/phoframes.txt");
  keys = loadStrings("/media/rob/Ma Book1/CS 230/videoToVoice/3/key.txt");
  
  font = loadFont("Garuda-48.vlw");
  textFont(font,24);
  size(400,250);
  frameRate(2);
}
void draw(){
  if(img < 200 || true){
    String s = img+"";
    while(s.length() < 4){
      s = "0"+s;
    }
    background(0);
    PImage mouthImage = loadImage("/media/rob/Ma Book1/CS 230/videoToVoice/3/mouthImages/frame"+s+".jpg");
    image(mouthImage,0,0);
    saveFrame("/media/rob/Ma Book1/CS 230/videoToVoice/3/lineupCheck/check"+s+".jpg");
    
    for(int y = -5; y <= 5; y++){
      String val = keys[Integer.parseInt(phos[img+y])];
      if(y == 0){
        fill(255,0,0);
      }else{
        fill(255);
      }
      text(val.split("\t")[1],240,160+24*y);
    }
  }
  img++; 
}