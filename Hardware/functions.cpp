//functions.cpp
#include "board.h"
#include "board.h"
#include "mbed.h"
static const uint32_t MAX_STRING_LENGTH = 32;
static char str[MAX_STRING_LENGTH];


void print_pos(Max7219 *p_display, uint8_t col, uint8_t col_code){
	uint8_t device;
	// This means we're on display 1
	if (col <=8){
		device = 1;
	}
	else{
		//If it's not a factor of 8 then readjust the column and 
		//calculate the new device number
		if (col % 8){
			device = ((col/8)+1);
			col = col%8;
		}

		else{
			device = col/8;
			col = 8;
		}
	}

	p_display -> write_digit(device,col,col_code);
}

int get_braille_simple(const char *word){
	uint8_t result = 0;
	//add the results to get a combination of the assigned LED's to turn on
	if(word[0]=='1') {result += 128;}
	if(word[1]=='1') {result += 64;}
	if(word[2]=='1') {result += 32;}
	if(word[3]=='1') {result += 4;}
	if(word[4]=='1') {result += 2;}
	if(word[5]=='1') {result += 1;}
	
	return result;
}

int get_braille(const char *word, bool second_row){
	uint8_t result = 0;
	//add the results to get a combination of the assigned LED's to turn on
	if(second_row){
		if(word[0]=='1') {result += 4;}
		if(word[1]=='1') {result += 2;}
		if(word[2]=='1') {result += 1;}
	}
	else{
		if(word[0]=='1') {result += 128;}
		if(word[1]=='1') {result += 64;}
		if(word[2]=='1') {result += 32;}
	}
	return result;
}

void braille_to_led_array(Max7219 *p_display, const char *(*braille_array)[16]){
	//expects 4x16 array
	for (int i = 0; i <3;i+=2){
		for (int j = 0; j<16;j++){
			uint8_t result = get_braille(braille_array[i][j],false);
			result += get_braille(braille_array[i+1][j],true);
			if (i==0){print_pos(p_display, (j+1),result);}
			else {print_pos(p_display,(17+j),result);}
		}
	}
}


void braille_to_led(Max7219 *p_display, uint8_t col, const char *s){
	uint8_t result = get_braille_simple(s);
	print_pos(p_display, col,result);
}	

char* get_serial_input(){
    //get user input
    fgets(str, MAX_STRING_LENGTH, stdin);
    //Remove trailing newline and CR, if there.
    if((strlen(str) > 0 ) && (str[strlen(str) - 1] == 0x0A) && (str[strlen(str) - 2] == 0x0D))
    {
        str[strlen(str) - 1] = '\0';
        str[strlen(str) - 1] = '\0';
    }
    return str;
}
	