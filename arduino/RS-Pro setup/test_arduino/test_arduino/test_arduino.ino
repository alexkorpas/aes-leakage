#include <avr/sleep.h>

#define PIN13 13

int initPin = 10;
int pulsePin = 11;
int triggerPin = 4;

void setup() {
  Serial.begin(9600);
  pinMode(triggerPin, OUTPUT);

  pinMode(initPin, INPUT);
  pinMode(pulsePin, INPUT);
  
  Serial.println("<Arduino is ready>");
}

char random_number;
String random_string;

int low = 97;
int high = 122;

int testPulseDuration = 100;
int testPulseRepeat = 1;

void encrypt() { 
  digitalWrite(triggerPin, HIGH);

  for(int c = 0; c < testPulseRepeat; c++) {
    for(int i = 0; i < testPulseDuration; i++){
      random_number = low + (rand() % (low - high));
    }

//    sleep(50);
  }

  digitalWrite(triggerPin, LOW);

  delay(500);
  
  Serial.println("done.");
}

int seed = 12345;

bool prevInit = true;
bool prevPulse = true;

void loop() {
  encrypt();
//    bool currInit = digitalRead(initPin) == HIGH;
//    if(!currInit && currInit != prevInit) {
//       srand(seed); 
//       Serial.println("reset");
//    }
//    prevInit = currInit;
//
//    bool currPulse = digitalRead(pulsePin) == HIGH;
//    if(!currPulse && currPulse != prevPulse) {
//      delay(50);
//      srand(seed); // TODO This sends the same plaintext every time !!!!!!! Debugging only.
//      Serial.println("pulse");
//      encrypt();
//    }
//    prevPulse = currPulse;
}
