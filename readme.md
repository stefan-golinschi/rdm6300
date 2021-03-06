## RDM6300 RFID reader Module

This was tested and still used on a RaspberryPI.

### Module pinout:
```
----------------------------------------
|                        p1| 5 4 3 2 1 |
|                           -----------|
|                                      |
|_____                          _______|
| 1 2 |p2                    p3| 3 2 1 |
----------------------------------------
```

|P1  | signal | description     |
|-------|--------|--------------|
|1   | TX   | Data TX           |
|2   | RX   | Data RX           |
|3   | NC   | Not Connected     |
|4   | GND  | Ground            |
|5   | VCC  | +5V Power         |

|P2  | signal | description     |
|-------|--------|--------------|
|1   | ANT1   | Antenna         |
|2   | ANT2   | Antenna         |


|P3  | signal | description     |
|-------|--------|--------------|
|1   | LED   | LED              |
|2   | VCC   | +5V Power        |
|4   | GND   | Ground           |