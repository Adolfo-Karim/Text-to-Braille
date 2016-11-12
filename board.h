//board.cpp

//modules for the board
#include "mbed.h"
#include "max7219.h"

/*************************************
Parameters:
	A Max display object (LED Display)
	a column from 1-32 in the display
	hex that indicates which lights to light up in the column
Returns:
	None
**************************************/

void print_pos(Max7219 *p_display, uint8_t column, uint8_t light_combination);

/*************************************
Parameters:
	Braile Text

**************************************/

void braille_to_led_array(Max7219 *p_display, const char *(*braille_array)[16]);


/*************************************
Parameters:
	Max val
*************************************/

char* get_serial_input();

/************************************
Parameters:
	Braile
*************************************/
void braille_to_led(Max7219 *p_display, uint8_t col,const char *s);
