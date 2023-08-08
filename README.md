# Dumb Smart Light

Dumb Smart Light is a project of Raspberry Pi Pico W based smart light wriytten in MicroPython. It features physical button to turn on/off and stores data about light state and brightnes even in case of power outage. I could not find smart light capable of that so I made my own. It has no control of light color or any wireless settings capability. It uses WS2812B LED light.

### Features :

  - Automaticly adjustable brightness. 
  - Physical button to turn on/off light.
  - Settings saved to file, so it doesn't turn on light after power outage if it was off before.
  - No wireless control.
  - Automaticly setting CET/CEST depending of the time of year.

 
### Bill of materials :

  - Raspberry Pi Pico W
  - WS2812B LED light
  - Momentary push button
  - 5V Power supply
  - Cables
  
  
### Wiring :

Wire Pin 1 of Pico to input of WS2812B LED light, Pins 2 and 3 of Pico to Momentary push button, Pin 8 of Pico to GND of WS2812B LED light, 5V+ from power supply to VCC of WS2812B LED light and GND of power supply to GND of WS2812B. Pico will be powered using microUSB port.

### Programming :

Put files "brightness", "light_state", "morning_light", "main.py" to Pico using Thonny. In main.py change SSID and password of your WiFi network. You can also change number of LEDs in WS2812B - I used light with 16 LEDs, RGB value of desired light - WARM_WHITE variable, time when dimming starts, time when it brightens up in the morning, duration of dimming and brightening, target brightness, brightness step, etc.


### License :

I don't have enough knowledge about licensing, as I copied some code from the internet and added own code, so feel free to use this as you wish.
