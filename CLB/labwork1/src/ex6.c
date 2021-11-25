/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/tim.h>
#include <stm32f4/nvic.h>

// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

#define WAIT_PSC 500
#define HALF_PERIOD (APB1_CLK / WAIT_PSC)

void init(){
	// output 
	GPIOD_MODER = SET_BITS(GPIOD_MODER, BLUE_LED*2, 2, 0b01);
	GPIOD_OTYPER &= ~(1<<GREEN_LED);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, BLUE_LED*2, 2, 0b00);
}

void init_TIM4(){
	TIM4_CR1 = 0;
	TIM4_PSC = WAIT_PSC;
	TIM4_ARR = HALF_PERIOD;
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;
}

void handle_TIM4() {
	TIM4_ARR = HALF_PERIOD;

	if(GPIOD_ODR & (1 << RED_LED) == 0){
		GPIOD_BSRR = 1 << RED_LED;
	}
	else{
		GPIOD_BSRR = 1 << (RED_LED << 16);
	}

	TIM4_SR &= ~TIM_UIF;
}

int main() {
	printf("\nStarting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	init();
	init_TIM4();

	TIM4_CR1 = TIM4_CR1 | TIM_CEN;

	if((TIM4_SR & TIM_UIF)!=0){
		handle_TIM4();
		TIM4_SR = 0;
	}

	

	// main loop
	printf("Endless loop!\n");
	while(1) {
	}

}


