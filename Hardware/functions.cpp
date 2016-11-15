//functions.cpp
#include "board.h"

void print_pos(Max7219 *p_display, uint8_t col, uint8_t col_code){
	uint8_t device;

	if (col <8){
		device = 1;
	}
	else{
		if (col % 8 == 1){
			device = (col-1)/8;
			col = 1;
		}
		else{
			device = col/8;
			col = col%8;
		}
	}

	p_display -> write_digit(device,col,col_code);
}

void braille_to_led(string braille_array){
	//expects 16x4 array
	for (int i = 0; i <2;i++){
		for (int j = 0; j<16;j++){
			uint8_t result = get_braille(braille_array[i][j],False);
			result = result + get_braille(braille_array[i+1][j],True);
			print_pos(&display, j*(i+1),result);
		}
	}
}

int get_braille(string word, bool second_row){
	uint8_t reslt = 0;
	if second_row{
		if(word[0]=='1') {result += 4;}
		if(word[1]=='1') {result += 2;}
		if(word[2]=='1') {result += 1;}
	}
	else{
		if(word[0]=='1') {result += 128;}
		if(word[1]=='1') {result += 64;}
		if(word[2]=='1') {result += 32;}
	}
	return result 
}


string test_array [][2] = {{"111","011","101","111","000","010","001","010"},
			  			   {"101","001","111","101","001","110","101","011"},
			  			   {"111","011","101","111","000","010","001","010"},
			  			   {"101","001","111","101","001","110","101","011"}};
