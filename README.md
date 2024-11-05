# Wake up Light

Wake up Light is a project of Raspberry Pi Pico W based wake up light written in MicroPython. It automatically turns on and slowly increases light brightness when it's time to wake up, then it automatically turns off when you leave to work. It stores data about light state and brightnes even in case of power outage. It has no control of light color or any wireless settings capability. It uses WS2812B LED light.

### Features :

  - Automatically adjustable brightness. 
  - Automatically turns on in the morning. 
  - Automatically turns off when it's time to leave to work. 
  - Settings saved to file, so it doesn't turn on light after power outage if it was off before.
  - No wireless control.
  - Automaticly setting CET/CEST depending of the time of year.

 
### Bill of materials :

  - Raspberry Pi Pico W
  - WS2812B LED light
  - 5V Power supply
  - Cables
  
  
### Wiring :

Wire Pin 1 of Pico to input of WS2812B LED light, Pin 3 of Pico to GND of WS2812B LED light, 5V+ from power supply to VCC of WS2812B LED light and GND of power supply to GND of WS2812B. Pico will be powered using microUSB port.

### Programming :

Put files "brightness", "light_state", "morning_light", "main.py" to Pico using Thonny. In main.py change SSID and password of your WiFi network. You can also change number of LEDs in WS2812B - I used light with 16 LEDs, RGB value of desired light - WHITE variable, time when it brightens up in the morning and turns off brightness step, etc.


### License :

I don't have enough knowledge about licensing, as I copied some code from the internet and added own code, so feel free to use this as you wish.
