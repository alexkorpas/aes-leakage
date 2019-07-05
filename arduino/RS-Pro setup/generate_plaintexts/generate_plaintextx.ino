#define INPUT_SIZE 16

char random_number;
uint8_t pText[INPUT_SIZE];

int low = 97;
int high = 122;
int iterations = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  delay(50);
  
  srand(12345);
}


void loop() {
  if(iterations < 10000) {
    for(int i = 0; i<INPUT_SIZE; i++){
      random_number = low + (rand() % (low - high));
      pText[i] = random_number;
    }

    Serial.print(((String) iterations) + ";");
    
    for(int i=0; i<16; i++){
      Serial.print((char)pText[i]);
    }
    Serial.print("\n");
    delay(50);
  
    iterations ++;
  }
}
