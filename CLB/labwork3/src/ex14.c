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
		GPIOD_MODER = SET_BITS(GPIOD_MODER, i*2, 2, GPIO_MODER_OUT);
		GPIOD_OTYPER = GPIOD_OTYPER &= ~ (1<<i);
		GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, i*2, 2, GPIO_PUPDR_PU);
	}

	// ADC1 sur PA3
	GPIOA_MODER = SET_BITS(GPIOA_MODER, 3*2, 2, GPIO_MODER_ANA);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 3*2, 2, GPIO_PUPDR_PU);
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

	int valeur = 0;
	while(1) {
		ADC1_CR2 |= ADC_SWSTART;
		while((ADC1_SR & ADC_EOC)==0)__asm("nop");
		valeur = ADC1_DR;
		printf("%d\n", valeur);
		if(valeur >=0 && valeur < 900){
			GPIOD_BSRR = 1 << (LED1 + 16);
			GPIOD_BSRR = 1 << (LED2 + 16);
			GPIOD_BSRR = 1 << (LED3 + 16);
			GPIOD_BSRR = 1 << (LED4 + 16);
		}
		else if(valeur>=900 && valeur<2000){
			GPIOD_BSRR = 1 << (LED1);
			GPIOD_BSRR = 1 << (LED2 + 16);
			GPIOD_BSRR = 1 << (LED3 + 16);
			GPIOD_BSRR = 1 << (LED4 + 16);
		}
		else if(valeur >= 2000 && valeur < 3000){
			GPIOD_BSRR = 1 << (LED1);
			GPIOD_BSRR = 1 << (LED2);
			GPIOD_BSRR = 1 << (LED3 + 16);
			GPIOD_BSRR = 1 << (LED4 + 16);
		}
		else if(valeur >= 3000 && valeur < 4000){
			GPIOD_BSRR = 1 << (LED1);
			GPIOD_BSRR = 1 << (LED2);
			GPIOD_BSRR = 1 << (LED3);
			GPIOD_BSRR = 1 << (LED4 + 16);
		}
		else{ // valeur > 4000
			GPIOD_BSRR = 1 << (LED1);
			GPIOD_BSRR = 1 << (LED2);
			GPIOD_BSRR = 1 << (LED3);
			GPIOD_BSRR = 1 << (LED4);
		}			
		
	}__asm("nop");
}