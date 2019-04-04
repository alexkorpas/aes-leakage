int initPin = 10;
int pulsePin = 11;
int debugLed = 13;

void setup() {
  Serial.begin(9600);
  
  pinMode(initPin, OUTPUT);
  pinMode(pulsePin, OUTPUT);
  pinMode(debugLed, OUTPUT);
  
  delay(500);
  Serial.println("<Arduino is ready>");
}

void pulse() {
  digitalWrite(pulsePin, HIGH);
  digitalWrite(debugLed, HIGH);
  delay(100);
  digitalWrite(pulsePin, LOW);
  digitalWrite(debugLed, LOW);
}

void start() {
  digitalWrite(initPin, HIGH);
  digitalWrite(debugLed, HIGH);
  delay(3000);
  digitalWrite(initPin, LOW);
  digitalWrite(debugLed, LOW);
}

String in;
void loop() {
  if (Serial.available() > 0) {
    in = char(Serial.read());
    Serial.println(in);
    
    if(in == "p") {
      pulse();
    } else if(in == "i") {
      start();
    }
  }
}
