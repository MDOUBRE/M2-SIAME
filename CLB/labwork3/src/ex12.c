/* Embedded Systems - Exercise 5 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/nvic.h>
#include <stm32f4/exti.h>
#include <stm32f4/syscfg.h>
#include <stm32f4/tim.h>
#include <stm32f4/adc.h>


// GPIOD
#define GREEN_LED	4
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

void init(){
	GPIOD_MODER = SET_BITS(GPIOD_MODER, GREEN_LED*2, 2, 0b01);
	GPIOD_OTYPER = GPIOD_OTYPER &= ~ (1<<0);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, GREEN_LED*2, 2, 0b00);

	GPIOA_MODER = SET_BITS(GPIOA_MODER, 3*2, 2, 0b11);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 3*2, 2, 0b01);
	ADC1_SQR3 = 3;
	ADC1_CR1 = 0;
	ADC1_CR2 = ADC_ADON;
}

int main() {
	printf("\nStarting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;
	RCC_APB2ENR |= RCC_ADC1EN;

	// initialization
	init();

	int x = 0;
	// main loop
	printf("Endless loop!\n");
	while(1) {
		ADC1_CR2 |= ADC_SWSTART;
		while((ADC1_SR & ADC_EOC) == 0)__asm("nop");
		x = ADC1_DR;
		if(x > 900){	// dans la salle 014 avec une lampe torche
			GPIOD_BSRR = 1 << GREEN_LED;
		}
		else{
			GPIOD_BSRR = 1 << (GREEN_LED+16);
		}
	}__asm("nop");

}


