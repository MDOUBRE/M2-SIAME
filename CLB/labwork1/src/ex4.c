/* Embedded Systems - Exercise 1 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <stm32f4/tim.h>

// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15
#define B1 0

#define WAIT_PSC 1000
#define WAIT_DELAY (APB1_CLK / WAIT_PSC)
#define DELAY_20 (WAIT_DELAY/100)
#define DELAY_250 (WAIT_DELAY/4)
#define DELAY_500 (WAIT_DELAY/2)
#define DELAY_1000 (WAIT_DELAY)

// GPIODA
#define USER_BUT	0

int pushed_B1=0;
int last_B1=0;

void init(){
	// output 
	GPIOD_MODER = SET_BITS(GPIOD_MODER, GREEN_LED*2, 2, 0b01);
	GPIOD_OTYPER &= ~(1<<GREEN_LED);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, GREEN_LED*2, 2, 0b00);

	// input
	GPIOA_MODER = SET_BITS(GPIOA_MODER, B1*2, 2, 0b00);
	GPIOA_OTYPER &= ~(1<<B1);
	GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, B1*2, 2, 0b00);
}

void init_TIM4(){
	TIM4_CR1 = 0;
	TIM4_PSC = WAIT_PSC;
	TIM4_ARR = DELAY_1000;
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;
}

int main() {
	enum{MILLE, CINQ, DEUX} state = MILLE;
	
	printf("Starting...\n");

	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	// GPIO init
	init();
	init_TIM4();

	TIM4_CR1 = TIM4_CR1 | TIM_CEN;

	while(1){
		if((TIM4_SR & TIM_UIF)!=0){
			if((GPIOD_ODR & (1<<GREEN_LED))==0){
				GPIOD_BSRR == 1 << GREEN_LED;
			}
			else{
				GPIOD_BSRR == 1 << (16+GREEN_LED);
			}
			TIM4_SR = 0;
		}

		if((GPIOD_IDR & (1<<B1)) !=0){
			pushed_B1=1;
			last_B1=TIM4_CNT;
		}
		else if(pushed_B1){
			int now = TIM4_CNT;
			if(now <= last_B1){
				now+= DELAY_20;
			}
			if(now-last_B1 >= DELAY_20){			
				pushed_B1=0;
				switch(state){
				case MILLE:
					TIM4_ARR = DELAY_500;
					state=CINQ;
					break;
				
				case CINQ:
					TIM4_ARR = DELAY_250;
					state=DEUX;
					break;
				
				case DEUX:
					TIM4_ARR = DELAY_1000;
					state=MILLE;
					break;
				}
			}
		}


	}

	printf("Endless loop!\n");

}
