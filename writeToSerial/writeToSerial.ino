const int PIN_SETPOINT = 34;
const int PIN_TRIGGER_DS = 32;
const int PIN_ECHO_DS = 33;
const int PIN_DAC = 25;

const long minDistance = 2;
const long maxDistance = 400;

void setup() {
  Serial.begin(115200);
  
  pinMode(PIN_SETPOINT, INPUT); //Setpoint pin
  
  //Distance sensor pin
  pinMode(PIN_TRIGGER_DS, OUTPUT);
  pinMode(PIN_ECHO_DS, INPUT);
}

float readDistanceCentimeters() {
  //Make sure the pulse is low before sending a pulse
  digitalWrite(PIN_TRIGGER_DS, LOW);
  delayMicroseconds(2);  // Wait briefly so the LOW state is stable

  //Send out an 8 cycle sonic burst, we can calculate the distance based on how long they traveled
  digitalWrite(PIN_TRIGGER_DS, HIGH);
  delayMicroseconds(10); // Keep it HIGH for at least 10 microseconds (sensor requirement)
  digitalWrite(PIN_TRIGGER_DS, LOW);

  //The pulseIn() method measures how long the waves traveled in microseconds
  long duration = pulseIn(PIN_ECHO_DS, HIGH, 30000);  //Timeout after 30ms if nothing is heard

  //If there is no pulse, we exit the function
  if (duration == 0) return -1;

  //We calculate the distance of an object based on how long it took for the sound to get there
  //0.0343 cm/us is the speed of sound, we then half the result to get the distance traveled one-way
  float distanceCentimeters = (duration * 0.0343) / 2.0;
  return distanceCentimeters;
}

float convertDistanceToDac(long _distance) {
  //Map the output from the distance sensor to a range between 0 and 255 (8-bit)
  int dacValue = map(_distance, minDistance, maxDistance, 0, 255);

  //Clamp the value to 0-255, as a fallback, as a fallback
  dacValue = constrain(dacValue, 0, 255);

  //Convert the 8-bit values to a voltage between 0-3.3V
  //Note: A DAC pin must be used (GPIO 25 or GPIO 26)
  dacWrite(PIN_DAC, dacValue);
}

void loop() {
  float distanceCentimeters = readDistanceCentimeters();
  int setpointRaw = analogRead(PIN_SETPOINT);

  //If there is distance reading, send the distance and setpoint values to the serial, so we can read it in Python
  if (distanceCentimeters >= 0) {
    Serial.print(distanceCentimeters, 2);  // send distance (2 decimal places)
    Serial.print(",");
    Serial.println(setpointRaw); // send raw ADC reading
  }

  convertDistanceToDac(float(distanceCentimeters)); //Convert the distance to a voltage output between 0-3.3V

  delay(50);
}
