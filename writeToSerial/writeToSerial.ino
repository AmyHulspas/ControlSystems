const int PIN_SETPOINT = 34;
const int PIN_TRIGGER_DS = 32;
const int PIN_ECHO_DS = 33;
const int PIN_DAC = 25;

const float minDistance = 2;
const float maxDistance = 50;

void setup() {
  Serial.begin(115200);

  // Distance sensor pins
  pinMode(PIN_TRIGGER_DS, OUTPUT);
  pinMode(PIN_ECHO_DS, INPUT);
}

float readDistanceCentimeters() {
  digitalWrite(PIN_TRIGGER_DS, LOW);
  delayMicroseconds(2);

  digitalWrite(PIN_TRIGGER_DS, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIGGER_DS, LOW);

  long duration = pulseIn(PIN_ECHO_DS, HIGH, 30000); // 30 ms timeout
  if (duration == 0) return -1.0; // no reading

  float distanceCentimeters = (duration * 0.0343f) / 2.0f;
  return distanceCentimeters;
}

void convertDistanceToDac(float _distance) {
  ///If there is no correct distance value, we want to stop the function here as a fallback
  if (_distance < 0) {
    dacWrite(PIN_DAC, 0);
    return;
  }

  //Calculate DAC output using gain variable style
  //This value should fall in the range of 0-255
  float gain = 255.0f / (maxDistance - minDistance);
  float value = (_distance - minDistance) * gain;

  //But in case it doesn't, clamp it between 0 and 255 as a fallback
  int dacValue = constrain(round(value), 0, 255);

  //Convert the 0-255 value to a voltage output between 0-3.3V
  dacWrite(PIN_DAC, dacValue);
}

void loop() {
  float distanceCentimeters = readDistanceCentimeters();
  int setpointRaw = analogRead(PIN_SETPOINT);

  convertDistanceToDac(distanceCentimeters); // update DAC output

  //If there is distance reading, send the distance and setpoint values to the serial, so we can read it in Python
  if (distanceCentimeters >= 0) {
    Serial.print(distanceCentimeters, 2);  // send distance (2 decimal places)
    Serial.print(",");
    Serial.println(setpointRaw); // send raw ADC reading
  }

  delay(50);
}
