// Pin selections here are based on the original Adafruit Learning System
// guide for the Teensy 3.x project.  Some of these pin numbers don't even
// exist on the smaller SAMD M0 & M4 boards, so you may need to make other
// selections:

// GRAPHICS SETTINGS (appearance of eye) -----------------------------------

// If using a SINGLE EYE, you might want this next line enabled, which
// uses a simpler "football-shaped" eye that's left/right symmetrical.
// Default shape includes the caruncle, creating distinct left/right eyes.
#ifdef ADAFRUIT_HALLOWING // Hallowing, with one eye, does this by default
  #define SYMMETRICAL_EYELID
#else                     // Otherwise your choice, standard is asymmetrical
  //#define SYMMETRICAL_EYELID
#endif

// Enable ONE of these #includes -- HUGE graphics tables for various eyes:
#include "graphics/defaultEye.h"      // Standard human-ish hazel eye -OR-
//#include "graphics/dragonEye.h"     // Slit pupil fiery dragon/demon eye -OR-
//#include "graphics/noScleraEye.h"   // Large iris, no sclera -OR-
//#include "graphics/goatEye.h"       // Horizontal pupil goat/Krampus eye -OR-
//#include "graphics/newtEye.h"       // Eye of newt -OR-
//#include "graphics/terminatorEye.h" // Git to da choppah!

// If your eye has a sclera bitmap that's all the same color (dragon,
// goat, noSclera), define FLAT_SCLERA to 0.  (You can use a different
// value for a constant color other than black.)  This will save about
// 50k of flash, which lets you enable lots of other features!
//#define FLAT_SCLERA 0

// Optional: enable this line for startup logo (screen test/orient):
#if !defined ADAFRUIT_HALLOWING     // Hallowing can't always fit logo+eye
  #include "graphics/logo.h"        // Otherwise your choice, if it fits
#endif

// EYE LIST ----------------------------------------------------------------

// This table contains ONE LINE PER EYE.  The table MUST be present with
// this name and contain ONE OR MORE lines.  Each line contains THREE items:
// a pin number for the corresponding TFT/OLED display's SELECT line, a pin
// pin number for that eye's "wink" button (or -1 if not used), and a screen
// rotation value (0-3) for that eye.

eyeInfo_t eyeInfo[] = {
#ifdef ADAFRUIT_HALLOWING
  { 39, -1, 2 }, // SINGLE EYE display-select and wink pins, rotate 180
#else
  {  9, 0, 0 }, // LEFT EYE display-select and wink pins, no rotation
  { 10, 2, 0 }, // RIGHT EYE display-select and wink pins, no rotation
#endif
};

// DISPLAY HARDWARE SETTINGS (screen type & connections) -------------------

#ifdef ADAFRUIT_HALLOWING
  #include <Adafruit_ST7735.h> // TFT display library
  #define DISPLAY_DC       38  // Display data/command pin
  #define DISPLAY_RESET    37  // Display reset pin
#else
  // Enable ONE of these #includes to specify the display type being used
  #include <Adafruit_SSD1351.h>  // OLED display library -OR-
  //#include <Adafruit_ST7735.h> // TFT display library (enable one only)
  #define DISPLAY_DC        7    // Data/command pin for ALL displays
  #define DISPLAY_RESET     8    // Reset pin for ALL displays
#endif

#ifdef ADAFRUIT_HALLOWING
  // Light up the backlight on the LCD.
  #define DISPLAY_BACKLIGHT 7
  // For a fixed-brightness backlight, set BACKLIGHT_MAX but not BACKLIGHT_MIN.
  //#define BACKLIGHT_MAX  128

  // For an adaptive backlight (requires LIGHT_PIN, below), set both
  // BACKLIGHT_MIN and BACKLIGHT_MAX.  For best results, also set
  // LIGHT_CURVE or FAKE_LIGHT_CURVE.
  #define BACKLIGHT_MIN  32
  #define BACKLIGHT_MAX  256
  // BL_RESPONSE_TIME: How quickly should the LCD backlight respond to
  // lighting changes?  1024 means that after changing from complete
  // dark to complete light, it takes about 30 seconds to brighten to
  // 63%.  (It takes about three minutes to change completely.)
  #define BL_RESPONSE_TIME 64
#endif

#if defined(_ADAFRUIT_ST7735H_) || defined(_ADAFRUIT_ST77XXH_)
  #define SPI_FREQ 24000000    // TFT: use max SPI (clips to 12 MHz on M0)
#else // OLED
  #if !defined(ARDUINO_ARCH_SAMD) && (F_CPU <= 72000000)
    #define SPI_FREQ 24000000  // OLED: 24 MHz on 72 MHz Teensy only
  #else
    #define SPI_FREQ 12000000  // OLED: 12 MHz in all other cases
  #endif
#endif

// INPUT SETTINGS (for controlling eye motion) -----------------------------

// JOYSTICK_X_PIN and JOYSTICK_Y_PIN specify analog input pins for manually
// controlling the eye with an analog joystick.  If set to -1 or if not
// defined, the eye will move on its own.
// IRIS_PIN speficies an analog input pin for a photocell to make pupils
// react to light (or potentiometer for manual control).  If set to -1 or
// if not defined, the pupils will change on their own.
// BLINK_PIN specifies an input pin for a button (to ground) that will
// make any/all eyes blink.  If set to -1 or if not defined, the eyes will
// only blink if AUTOBLINK is defined, or if the eyeInfo[] table above
// includes wink button settings for each eye.

//#define JOYSTICK_X_PIN A0 // Analog pin for eye horiz pos (else auto)
//#define JOYSTICK_Y_PIN A1 // Analog pin for eye vert position (")
//#define JOYSTICK_X_FLIP   // If defined, reverse stick X axis
//#define JOYSTICK_Y_FLIP   // If defined, reverse stick Y axis
#define TRACKING            // If defined, eyelid tracks pupil
#define BLINK_PIN         1 // Pin for manual blink button (BOTH eyes)
#define AUTOBLINK           // If defined, eyes also blink autonomously
#ifdef ADAFRUIT_HALLOWING
  #define LIGHT_PIN      A1 // Hallowing light sensor pin
  // Bringing in the necessary math functions to do a light sensor
  // curve can be a strong impact (about 50k), and easily get you over
  // the 256k flash limit of a Hallowing if you have new code.
  //#define LIGHT_CURVE  0.33 // Light sensor adjustment curve
  // If you don't need close precision, you can use FAKE_LIGHT_CURVE
  // instead, which approximates a (hard-coded) 0.33 curve.
  #define FAKE_LIGHT_CURVE
  // The Hallowing's light sensor will range from 0 to 980, but almost
  // all of it is in the lower end.  In a bright room under a desk lamp,
  // it still only goes to 50 or so.
  #define LIGHT_MIN       0 // Minimum useful reading from light sensor
  #define LIGHT_MAX      48 // Maximum useful reading from sensor
#else
  #define LIGHT_PIN      A2 // Photocell or potentiometer (else auto iris)
//#define LIGHT_PIN_FLIP    // If defined, reverse reading from dial/photocell
  #define LIGHT_MIN       0 // Lower reading from sensor
  #define LIGHT_MAX    1023 // Upper reading from sensor
#endif
#define IRIS_SMOOTH         // If enabled, filter input from IRIS_PIN
#if !defined(IRIS_MIN)      // Each eye might have its own MIN/MAX
  #define IRIS_MIN      120 // Iris size (0-1023) in brightest light
#endif
#if !defined(IRIS_MAX)
  #define IRIS_MAX      720 // Iris size (0-1023) in darkest light
#endif

#ifdef ADAFRUIT_HALLOWING
  #define ACCEL 0x18 // Use the built-in accelerometer for vertical eye tracking
  // What range do you want to look at?  This is in milliradians from
  // vertical if ACCEL_TRIG is defined, or thousandths of 1g otherwise.
  // This range looks about right for the dragon eye; other
  // eyes may prefer different ranges.
  #define ACCEL_TRIG
  #define ACCEL_MIN -775
  #define ACCEL_MAX -300
  // I can't get the default eye looking right; maybe try something around
  // here.
  //#define ACCEL_TRIG
  //#define ACCEL_MIN -1000
  //#define ACCEL_MAX 700
  // Add some random vertical movement to the eye.
  #define ACCEL_SACCADE 256
#endif
