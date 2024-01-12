// Include necessary libraries
#include <Arduino.h>

// Define an array of GPIO pins to test
const int ledPins[] = {D0, D1, D2, D3, D4, D5, D6, D7, D8};

void setup()
{
  // Set all pins as outputs
  Serial.begin(9600);
  for (int pin : ledPins)
  {
    pinMode(pin, OUTPUT);
  }
}

void loop()
{
  // Iterate through each pin and toggle the LED
  for (int pin : ledPins)
  {
    digitalWrite(pin, HIGH);
    Serial.print("Pin:"); Serial.println(pin);
    delay(500); // Wait for 0.5 seconds (adjust as needed)
    digitalWrite(pin, LOW);
    delay(500); // Wait for 0.5 seconds (adjust as needed)

<<<<<<< HEAD
  }
=======
// put function definitions here:
int myFunction(int x, int y) {
  return x;
>>>>>>> 9222a216d7de21e04c27c9a8739d5a4573dd5140
}