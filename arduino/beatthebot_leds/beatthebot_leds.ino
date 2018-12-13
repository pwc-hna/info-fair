#include "FastLED.h"

#define PIN 6
#define NUM_DOCS 7
#define NUM_LEDS 300

CRGB leds[NUM_LEDS];
 
String str = "FNNNNNNN";
String gameStr = "NNNNNNN";
// boolean gameWon = true; 
// boolean newData = false;
String receivedChars;

void setup()
{
  Serial.begin(9600);  // initialize serial communications at 9600 bps
  FastLED.addLeds<WS2811, PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );

}

String read_str_from_pc() {
  // serial read section
  while (Serial.available())
  {
    if(Serial.available() > 0)
    {
        return Serial.readStringUntil('\n');
    }
  }
}

void loop(){
   if (Serial.available()) {
      receivedChars = read_str_from_pc();
      // newData = false;
      Serial.println(receivedChars);
      if (receivedChars.length() == NUM_DOCS+1){
        str = receivedChars;
      }
      // gameWon = true;
    }

   
    gameStr = str.substring(1);

    // if game not started, twinkle tree
    if(str.charAt(0) == 'F'){
      TwinkleRandom(80, 100, false); 
      // gameWon = true; // to make sure this value is reset to TRUE (making a mistake sets it to false)
    }
    
    // if final answer not yet provided, game not won or lost yet
    // so check current status and provide lights
    else if (gameStr.charAt(NUM_DOCS-1) == 'N'){
      for(int i=0; i < NUM_DOCS-1; i++){ // loop over all but the last letter
        char currentChar = gameStr.charAt(i);

        // current document not fulfilled yet, so the next ones neither
        if(currentChar == 'N'){
          CylonBounce(i*NUM_LEDS/NUM_DOCS, NUM_LEDS, 239, 186, 56, 4, 10, 50); // PwC Yellow
          break;
        }

        // current document correctly DONE
        else if(currentChar == 'T'){
          // set current part of strip GREEN
          for(int j=i*NUM_LEDS/NUM_DOCS; j < min((i+1)*NUM_LEDS/NUM_DOCS,NUM_LEDS);j++){
             leds[j] = CRGB( 50, 205, 50); // Green  
          }
          showStrip();

        }
        else { // current doc has mistake 
          // set current part of strip RED
          for(int j=i*NUM_LEDS/NUM_DOCS; j < min((i+1)*NUM_LEDS/NUM_DOCS,NUM_LEDS);j++){
             leds[j] = CRGB( 194, 47, 38); // PwC Red

          }
          showStrip();
          // gameWon = false;
        }
      
     }
    }
    else if (gameStr.indexOf('F') == -1){
      theaterChase(50,205,50,50);
    }
    else {
      Fire(20,160,15);
    }
      
  

}


// -----HELPER FUNCTIONS
//-------------------------

// void recvWithEndMarker() {
//   static byte ndx = 0;
//   char endMarker = '\n';
//   char rc;
 
//   // if (Serial.available() > 0) {
//   while (Serial.available() > 0 && newData == false) {
//   rc = Serial.read();

//   if (rc != endMarker) {
//     receivedChars[ndx] = rc;
//     ndx++;
//     if (ndx >= numChars) {
//       ndx = numChars - 1;
//     } else {
//       receivedChars[ndx] = '\0'; // terminate the string
//       ndx = 0;
//       newData = true;
//     }
//   }
//  }
// }

void CylonBounce(int startLed, int endLed, byte red, byte green, byte blue, int EyeSize, int SpeedDelay, int ReturnDelay){

  for(int i = startLed; i < endLed-EyeSize-2; i++) {
    for(int i = startLed; i < endLed-EyeSize-2; i++){
      setPixel(i,0,0,0);
    }
    setPixel(i, red/10, green/10, blue/10);
    for(int j = 1; j <= EyeSize; j++) {
      setPixel(i+j, red, green, blue); 
    }
    setPixel(i+EyeSize+1, red/10, green/10, blue/10);
    showStrip();
    delay(SpeedDelay);
  }

  delay(ReturnDelay);

  for(int i = startLed; i < endLed-EyeSize-2; i++) {
    for(int i = startLed; i < endLed-EyeSize-2; i++){
      setPixel(i,0,0,0);
    }
    setPixel(i, red/10, green/10, blue/10);
    for(int j = 1; j <= EyeSize; j++) {
      setPixel(i+j, red, green, blue); 
    }
    setPixel(i+EyeSize+1, red/10, green/10, blue/10);
    showStrip();
    delay(SpeedDelay);
  }
  
  delay(ReturnDelay);
}

void theaterChase(byte red, byte green, byte blue, int SpeedDelay) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (int i=0; i < NUM_LEDS; i=i+3) {
        setPixel(i+q, red, green, blue);    //turn every third pixel on
      }
      showStrip();
     
      delay(SpeedDelay);
     
      for (int i=0; i < NUM_LEDS; i=i+3) {
        setPixel(i+q, 0,0,0);        //turn every third pixel off
      }
    }
  }
}

void TwinkleRandom(int Count, int SpeedDelay, boolean OnlyOne) {
  setAll(0,0,0);
  
  for (int i=0; i<Count; i++) {
     setPixel(random(NUM_LEDS),random(0,255),random(0,255),random(0,255));
     showStrip();
     delay(SpeedDelay);
     if(OnlyOne) { 
       setAll(0,0,0); 
     }
   }
  
  delay(SpeedDelay);
}

void Fire(int Cooling, int Sparking, int SpeedDelay) {
  static byte heat[NUM_LEDS];
  int cooldown;
  
  // Step 1.  Cool down every cell a little
  for( int i = 0; i < NUM_LEDS; i++) {
    cooldown = random(0, ((Cooling * 10) / NUM_LEDS) + 2);
    
    if(cooldown>heat[i]) {
      heat[i]=0;
    } else {
      heat[i]=heat[i]-cooldown;
    }
  }
  
  // Step 2.  Heat from each cell drifts 'up' and diffuses a little
  for( int k= NUM_LEDS - 1; k >= 2; k--) {
    heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3;
  }
    
  // Step 3.  Randomly ignite new 'sparks' near the bottom
  if( random(255) < Sparking ) {
    int y = random(7);
    heat[y] = heat[y] + random(160,255);
    //heat[y] = random(160,255);
  }

  // Step 4.  Convert heat to LED colors
  for( int j = 0; j < NUM_LEDS; j++) {
    setPixelHeatColor(j, heat[j] );
  }

  showStrip();
  delay(SpeedDelay);
}

void setPixelHeatColor (int Pixel, byte temperature) {
  // Scale 'heat' down from 0-255 to 0-191
  byte t192 = round((temperature/255.0)*191);
 
  // calculate ramp up from
  byte heatramp = t192 & 0x3F; // 0..63
  heatramp <<= 2; // scale up to 0..252
 
  // figure out which third of the spectrum we're in:
  if( t192 > 0x80) {                     // hottest
    setPixel(Pixel, 255, 255, heatramp);
  } else if( t192 > 0x40 ) {             // middle
    setPixel(Pixel, 255, heatramp, 0);
  } else {                               // coolest
    setPixel(Pixel, heatramp, 0, 0);
  }
}

void showStrip() {
 #ifdef ADAFRUIT_NEOPIXEL_H 
   // NeoPixel
   strip.show();
 #endif
 #ifndef ADAFRUIT_NEOPIXEL_H
   // FastLED
   FastLED.show();
 #endif
}

void setPixel(int Pixel, byte red, byte green, byte blue) {
 #ifdef ADAFRUIT_NEOPIXEL_H 
   // NeoPixel
   strip.setPixelColor(Pixel, strip.Color(red, green, blue));
 #endif
 #ifndef ADAFRUIT_NEOPIXEL_H 
   // FastLED
   leds[Pixel].r = red;
   leds[Pixel].g = green;
   leds[Pixel].b = blue;
 #endif
}

void setAll(byte red, byte green, byte blue) {
  for(int i = 0; i < NUM_LEDS; i++ ) {
    setPixel(i, red, green, blue); 
  }
  showStrip();
}
