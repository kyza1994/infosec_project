template<class T> inline Print &operator <<(Print &obj, T arg) { obj.print(arg); return obj; }
#include <troyka-imu.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>

Accelerometer accel;

const int chipSelect = 4;

void setup()
{
  if (!SD.begin(chipSelect))
    return;
  accel.begin();
  accel.setRange(RANGE_2);
}

void loop()
{
  String dataString = "";
  dataString += accel.readX_G();
  dataString += " ";
  dataString += accel.readY_G();
  dataString += " ";
  dataString += accel.readZ_G();
  
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
  }
  delay(10);
}









