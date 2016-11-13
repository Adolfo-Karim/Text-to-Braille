//main.cpp
#include "board.h"

int main(void){

	// DISPLAY SETUP TAKEN FROM STARTER CODE
	Max7219 display(D11, D12, D13, D10);
    
    //struct for holding MAX7219 configuration data
    max7219_configuration_t display_config;
        
    //configuration data
    display_config.decode_mode = 0; //no BCD decode
    display_config.intensity  = Max7219::MAX7219_INTENSITY_F;   //max intensity
    display_config.scan_limit = Max7219::MAX7219_SCAN_8;        //scan all digits
    
    //set number of MAX7219 devices being used
    display.set_num_devices(4);
    
    //config display 
    display.init_display(display_config);
    
    //ensure all data registers are 0
    display.display_all_off();
    
    display.enable_display();
	/*
	const char * test_array [4][16] = {{"111","011","101","111","000","010","001","010","101","101","001","001","101","110","101","011"},
			  			   {"101","001","111","101","001","110","101","011","101","001","111","101","001","110","101","011"},
			  			   {"111","011","101","111","000","010","001","010","101","001","111","101","001","110","101","011"},
			  			   {"101","001","111","101","001","110","101","011","101","001","111","101","001","110","101","011"}};
	*/
	//braille_to_led_array(&display,test_array);
	do{
		//const char* input_buffer [4][16];
		for (uint8_t i = 1; i<33; i++){
			char* user_input = get_serial_input();
			braille_to_led(&display,i,user_input);	
		}			
	}while (true);
} 