/* Embedded Systems - Exercise 1 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <unistd.h>



// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15


// GPIOA
#define USER_BUT	0

volatile enum{BLUE, GREEN, RED, ORANGE, DEB} state=DEB;

void init()
{
	for(int i=12;i<16;i++)
	{
		GPIOD_MODER = SET_BITS(GPIOD_MODER, i*2, 2, 0b01);
		GPIOD_OTYPER &= ~(1<<i);
		GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, i*2, 2, 0b00);
	}

}

int main() 
{
	int HALF_PERIOD=30000000;

	
	int a = 0;
	printf("Starting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIODEN;
	init();

	// GPIO init

	printf("Endless loop!\n");

	while(1)
	{
		for(int i=0;i<HALF_PERIOD;i++)__asm("nop");
		
		switch(state){
		case DEB :
			GPIOD_BSRR = 1 << (GREEN_LED+16);
			GPIOD_BSRR = 1 << (RED_LED+16);
			GPIOD_BSRR = 1 << (ORANGE_LED+16);
			GPIOD_BSRR = 1 << (BLUE_LED+16);
			state=GREEN;
			break;
		
		case GREEN :
			GPIOD_BSRR = 1 << GREEN_LED;
			GPIOD_BSRR = 1 << (BLUE_LED+16);			
			state=ORANGE;
			break;

		case ORANGE :
			GPIOD_BSRR = 1 << ORANGE_LED;
			GPIOD_BSRR = 1 << (GREEN_LED+16);			
			state=RED;
			break;

		case RED :
			GPIOD_BSRR = 1 << RED_LED;
			GPIOD_BSRR = 1 << (ORANGE_LED+16);			
			state=BLUE;
			break;

		case BLUE :
			GPIOD_BSRR = 1 << BLUE_LED;
			GPIOD_BSRR = 1 << (RED_LED+16);			
			state=GREEN;
			break; 
		
		}	
	}
}
