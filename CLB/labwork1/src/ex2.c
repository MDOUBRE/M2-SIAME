/* Embedded Systems - Exercise 2 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>


// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15
#define B1 0

// GPIODA
#define USER_BUT	0

#define HALF_PERIOD 30000000

int state_B1=0;
int pushed_B1=0;

void init()
{
	// output 
	GPIOD_MODER = SET_BITS(GPIOD_MODER, GREEN_LED*2, 2, 0b01);
	GPIOD_OTYPER &= ~(1<<GREEN_LED);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, GREEN_LED*2, 2, 0b00);

	// input
	GPIOA_MODER = SET_BITS(GPIOA_MODER, B1*2, 2, 0b00);
	GPIOA_OTYPER &= ~(1<<B1);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, B1*2, 2, 0b00);
}


int main() {
	printf("Starting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;

	// GPIO init
	init();

	printf("Endless loop!\n");
	while(1) {

		if((GPIOA_IDR & (1<<B1) !=0))
		{
			pushed_B1=1;
		}
		else{
			pushed_B1=0;
		}

		if(pushed_B1==1 & state_B1==0){
			state_B1=1;
			GPIOD_BSRR = 1 << GREEN_LED;
		}
		else if(pushed_B1==0 & state_B1==1){
			state_B1=0;
			GPIOD_BSRR = 1 << (GREEN_LED+16);
		}
	}

}
