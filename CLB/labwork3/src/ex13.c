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
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

// GPIODA
#define USER_BUT	0

#define WAIT_PSC 1000
#define WAIT_DELAY (APB1_CLK / WAIT_PSC)
#define DELAY_100 (WAIT_DELAY / 10)


int x = 0;

void handle_TIM4(){
	TIM4_ARR = DELAY_100;
	ADC1_CR2 |= ADC_SWSTART;
	TIM4_SR &= ~(TIM_UIF);
}

void handle_ADC(){
	while((ADC1_SR & ADC_EOC) == 0)__asm("nop");
	x = ADC1_DR;
	if(x > 900){
		GPIOD_BSRR = 1 << GREEN_LED;
	}
	else{
		GPIOD_BSRR = 1 << (GREEN_LED+16);
	}	
}

void init(){
	DISABLE_IRQS;

	// LED
	GPIOD_MODER = SET_BITS(GPIOD_MODER, GREEN_LED*2, 2, 0b01);
	GPIOD_OTYPER = GPIOD_OTYPER &= ~ (1<<0);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, GREEN_LED*2, 2, 0b00);

	// analog ADC
	GPIOA_MODER = SET_BITS(GPIOA_MODER, 3*2, 2, 0b11);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 3*2, 2, 0b01);

	// init de ADC pour photomachin
	ADC1_SQR3 = 3; 			// PA3
	ADC1_CR1 = ADC_EOCIE; 	// pour interrupt
	ADC1_CR2 = ADC_ADON;	// AD Converter ON

	// interrput adc
	NVIC_ICER(ADC_IRQ >> 5) |= 1 << (ADC_IRQ & 0X1f);
	NVIC_IRQ(ADC_IRQ) = (uint32_t)handle_ADC;
	NVIC_IPR(ADC_IRQ) = 0;
	NVIC_ICPR(ADC_IRQ >> 5) |= 1 << (ADC_IRQ & 0X1f);
	NVIC_ISER(ADC_IRQ >> 5) |= 1 << (ADC_IRQ & 0X1f);	
	

	// interrupt TIM4
	NVIC_ICER(TIM4_IRQ >> 5) |= 1 << (TIM4_IRQ & 0X1f);
	NVIC_IRQ(TIM4_IRQ) = (uint32_t)handle_TIM4;
	NVIC_IPR(TIM4_IRQ) = 1;
	NVIC_ICPR(TIM4_IRQ >> 5) |= 1 << (TIM4_IRQ & 0X1f);
	NVIC_ISER(TIM4_IRQ >> 5) |= 1 << (TIM4_IRQ & 0X1f);

	// init TIM4
	TIM4_CR1 = 0;
	TIM4_PSC = WAIT_PSC;
	TIM4_ARR = DELAY_100;
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;
	TIM4_SR &= ~(TIM_UIF);
	TIM4_DIER = TIM_UIE;

	ENABLE_IRQS;
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

	}__asm("nop");

}


