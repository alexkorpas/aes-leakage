#define PIN13 13


char receivedChar;
boolean newData = false;
boolean loading = false;

boolean reset_led = false;

String data = "";
String nextData = "";

void setup() {
   Serial.begin(9600);
   Serial.println("<Arduino is ready>");
}

void loop() {
  serialReceive();
}

void recvOneChar() {
 if (Serial.available()) {
 receivedChar = Serial.read();
 newData = true;
 }
}

void excecute(String data) {
  Serial.println("Received: " + data);
}

void showNewData() {
 if (newData == true) {
  if(receivedChar == ']'){
    excecute(data);
    data = "";
    loading = false;
  } else if(receivedChar == '['){
    loading = true;
  } else {
    if(loading) data += receivedChar;
  }
  newData = false;
 }
}

void serialReceive() {
  recvOneChar();
  showNewData();
}
