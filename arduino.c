#include <Wire.h>
#include <LCD_I2C.h>
#include <SimpleDHT.h>

LCD_I2C lcd(0x27);
int pinDHT11 = 7;
SimpleDHT11 dht11;

String f;
int x = 0;

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  Serial.begin(9600);
  pinMode(6, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("PEST");
  lcd.setCursor(0, 1);
  lcd.print("MONITORING");
  delay(5000);
  lcd.clear();
}

void loop() {
  if (Serial.available()) {
    f = Serial.readString();
    Serial.println(f);
    lcd.print("Value: ");
    lcd.setCursor(5, 1);
    lcd.print(f);
    delay(500);
    lcd.clear();
    x = f.toInt();
    
    if ((x >= 0 && x <= 6)) {
      lcd.clear();
      digitalWrite(6, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("PEST MONITORING");
      lcd.setCursor(0, 1);
      lcd.print("STATUS:AFFECTED");
      delay(1000);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("PEST MONITORING");
      lcd.setCursor(0, 1);
      lcd.print("SPRAYING STARTED");
      delay(500);
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
      delay(5000);
      digitalWrite(2, HIGH);
      digitalWrite(3, HIGH);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("PEST MONITORING");
      lcd.setCursor(0, 1);
      lcd.print("SPRAYING COMPLETED");
      delay(500);
      lcd.clear();
      digitalWrite(6, LOW);
    }
    if ((x >= 7 && x <= 13)) {
      lcd.clear();
      digitalWrite(6, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("PEST MONITORING");
      lcd.setCursor(0, 1);
      lcd.print("STATUS:AFFECTED");
      delay(1000);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("PEST MONITORING");
      lcd.setCursor(0, 1);
      lcd.print("SPRAYING STARTED");
      delay(500);
      digitalWrite(4, LOW);
      digitalWrite(5, HIGH);
      delay(5000);
      digitalWrite(4, HIGH);
      digitalWrite(5, HIGH);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("PEST MONITORING");
      lcd.setCursor(0, 1);
      lcd.print("SPRAYING COMPLETED");
      delay(500);
      lcd.clear();
      digitalWrite(6, LOW);
    }
  }

  int a = analogRead(A0);
  int b = analogRead(A1);
  b = b / 8;
  b = b / 4;
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err=");
    Serial.println(err);
    delay(1000);
    return;
  }

  float temp = (int)temperature;
  Serial.print("Sample OK: ");
  Serial.print((int)temperature);
  Serial.print("*C, ");
  Serial.print((int)humidity);
  Serial.println("H");
  
  lcd.setCursor(0, 0);
  lcd.print("TEMPERATURE ");
  lcd.setCursor(0, 1);
  lcd.print(temp);
  delay(500);
  lcd.clear();
  
  lcd.setCursor(0, 0);
  lcd.print("MOISTURE ");
  lcd.setCursor(0, 1);
  lcd.print(a);
  delay(500);
  lcd.clear();
  
  lcd.setCursor(0, 0);
  lcd.print("pH: ");
  lcd.setCursor(0, 1);
  lcd.print(b);
  delay(500);
  lcd.clear();

  delay(1500);

  if (a > 500) {
    digitalWrite(6, HIGH);
    delay(500);
    digitalWrite(6, LOW);
  }
  delay(90);
}
