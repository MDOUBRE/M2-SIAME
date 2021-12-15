#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/tim.h>
#include <stm32f4/nvic.h>
#include <stm32f4/exti.h>
#include <stm32f4/syscfg.h>

// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15
#define B1 4
#define LED 4

// GPIODA
#define USER_BUT	0

#define WAIT_PSC 1000
#define WAIT_DELAY (APB1_CLK / WAIT_PSC)
//#define HALF_PERIOD (WAIT_DELAY/2)
#define DELAY_50 (WAIT_DELAY/5)

int state_B1=0;
int pushed_B1=0;
int click=0;
int last_b1 = 0;
volatile int un_sur_deux = 0;

void init(){
	// output 
	GPIOD_MODER = SET_BITS(GPIOD_MODER, LED*2, 2, 0b01);
	GPIOD_OTYPER &= ~(1<<LED);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, LED*2, 2, 0b01);
		
	GPIOA_MODER = SET_BITS(GPIOA_MODER, B1*2, 2, 0b00);
	GPIOA_OTYPER &= ~(1<<B1);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, B1*2, 2, 0b00);	
}

int main() {
	printf("\nStarting...\n");
	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;
	
	init();
	GPIOD_BSRR = 1 << LED;


	// main loop
	printf("Endless loop!\n");
	while(1) {
		if((GPIOA_IDR & (1 << B1))!=0){
			GPIOD_BSRR = 1 << LED+16;
			//printf("coucou\n");
		}
		
		else{
			GPIOD_BSRR = 1 << LED;
		}
		
	}__asm("nop");
}
