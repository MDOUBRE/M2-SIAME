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

#define LED1 	0
#define LED2 	1
#define LED3 	2
#define LED4 	3
#define LED5 	4
#define LED6 	5

// GPIODA
#define USER_BUT	0

#define WAIT_PSC 1000
#define WAIT_DELAY (APB1_CLK / WAIT_PSC)
#define HALF_PERIOD (WAIT_DELAY/2)

volatile int un_sur_deux = 0;
volatile int descend = 0;
volatile int TIM4_triggered = 0;
volatile enum{L1, L2, L3, L4, L5, L6, ETEINT} state=ETEINT;

void init(){
	// output 
	for(int i=0;i<6;i++)
	{
		GPIOA_MODER = SET_BITS(GPIOA_MODER, i*2, 2, 0b01);
		GPIOA_OTYPER &= ~(1<<i);
		GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, i*2, 2, 0b00);
	}
}

void handle_TIM4() {
	TIM4_ARR = HALF_PERIOD;
    if(un_sur_deux!=1){    
		TIM4_triggered = 1;
        
        un_sur_deux+=1;
    }
    else{
        un_sur_deux=0;
    }
	
	TIM4_SR &= ~TIM_UIF;
}

void init_TIM4(){
	DISABLE_IRQS;

	NVIC_ICER(TIM4_IRQ >> 5) |= 1 << (TIM4_IRQ & 0X1f);
	NVIC_IRQ(TIM4_IRQ) = (uint32_t)handle_TIM4;
	NVIC_IPR(TIM4_IRQ) = 0;

	NVIC_ICPR(TIM4_IRQ >> 5) |= 1 << (TIM4_IRQ & 0X1f);
	NVIC_ISER(TIM4_IRQ >> 5) |= 1 << (TIM4_IRQ & 0X1f);

	TIM4_CR1 = 0;
	TIM4_PSC = WAIT_PSC;
	TIM4_ARR = HALF_PERIOD;
	TIM4_EGR = TIM_UG;
	TIM4_SR = 0;
	TIM4_CR1 = TIM_ARPE;
	TIM4_SR &= ~TIM_UIF;
	TIM4_DIER = TIM_UIE;

	ENABLE_IRQS;
	TIM4_CR1 |= TIM_CEN;
}

int main() {
	printf("\nStarting...\n");
	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	init();
	init_TIM4();
	
	// main loop
	printf("Endless loop!\n");
	while(1) {
		if(TIM4_triggered){
			TIM4_triggered = 0;
			switch(state){
			case ETEINT :
				GPIOA_BSRR = 1 << (LED1+16);
				GPIOA_BSRR = 1 << (LED2+16);
				GPIOA_BSRR = 1 << (LED3+16);
				GPIOA_BSRR = 1 << (LED4+16);
				GPIOA_BSRR = 1 << (LED5+16);
				GPIOA_BSRR = 1 << (LED6+16);
				state=L1;
				descend=0;
				break;
			
			case L1 :
				GPIOA_BSRR = 1 << LED1;	
				GPIOA_BSRR = 1 << LED2+16;	
				state=L2;
				if(descend==1){
					state = ETEINT;
				}
				break;

			case L2 :
				GPIOA_BSRR = 1 << LED2;	
				GPIOA_BSRR = 1 << LED3+16;		
				state=L3;
				if(descend==1){
					state = L1;
				}
				break;

			case L3 :
				GPIOA_BSRR = 1 << LED3;	
				GPIOA_BSRR = 1 << LED4+16;		
				state=L4;
				if(descend==1){
					state = L2;
				}
				break;

			case L4 :
				GPIOA_BSRR = 1 << LED4;	
				GPIOA_BSRR = 1 << LED5+16;		
				state=L5;
				if(descend==1){
					state = L3;
				}
				break;

			case L5 :
				GPIOA_BSRR = 1 << LED5;	
				GPIOA_BSRR = 1 << LED6+16;		
				state=L6;
				if(descend==1){
					state = L4;
				}
				break;

			case L6 :
				GPIOA_BSRR = 1 << LED6;			
				descend=1;
				state=L5;
				break;
			}
		}
	}__asm("nop");

}


