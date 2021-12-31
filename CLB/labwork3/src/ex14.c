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
#define LED1 3
#define LED2 4
#define LED3 5
#define LED4 6
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

int x = 0;

void init(){
	for(int i=LED1;i<LED4+1;i++){
		GPIOD_MODER = SET_BITS(GPIOD_MODER, i*2, 2, ObO1);
		GPIOD_OTYPER = GPIOD_OTYPER &= ~ (1<<i);
		GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, i*2, 2, ObOO);
	}

	// ADC1 sur PA3
	GPIOA_MODER = SET_BITS(GPIOA_MODER, 3*2, 2, Ob11);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 3*2, 2, ObO1);
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

	// main loop
	printf("Endless loop!\n");
	while(1) {
		ADC1_CR2 |= ADC_SWSTART;
		while(ADC1_SR & ADC_EOF){
			// lire puis selon valeur allumer plus ou moins de led
			
		}
	}

}


