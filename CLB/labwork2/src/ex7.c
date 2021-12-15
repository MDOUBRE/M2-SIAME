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
#define B1 0

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
int HALF_PERIOD = 0;
volatile int un_sur_deux = 0;

void init(){
	// output 
	GPIOD_MODER = SET_BITS(GPIOD_MODER, GREEN_LED*2, 2, 0b01);
	GPIOD_OTYPER &= ~(1<<GREEN_LED);
	GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, GREEN_LED*2, 2, 0b01);
}

void handle_B1(){
    //printf("on est dans le handle\n");
      
    if((GPIOA_IDR & (1<<B1) !=0))
    {      
        state_B1 = 1;
        last_b1 = TIM4_CNT;        
    }
    else if(state_B1){
        int now = TIM4_CNT;
        if(now<= last_b1){
            now+= DELAY_50;
        }
        if(now - last_b1 >= DELAY_50){
            state_B1 = 0; 
            if((GPIOD_ODR & (1 << GREEN_LED))==0){
                GPIOD_BSRR = 1 << GREEN_LED;
            }
            else{
                GPIOD_BSRR = 1 << (GREEN_LED+16);
            }      
        }
    }
        
    EXTI_PR |= 1 << 0;   
    
}

void init_B1(){
    DISABLE_IRQS;

    SET_BITS(SYSCFG_EXTICR1, 0, 4, 0);
    EXTI_RTSR |= 1 << 0;
    EXTI_FTSR |= 1 << 0;
    EXTI_IMR |= 1 << 0;
    EXTI_PR |= 1 << 0;

    NVIC_ICER(EXTI0_IRQ >> 5) |= 1 << (EXTI0_IRQ & 0X1f);
    NVIC_IRQ(EXTI0_IRQ) = (uint32_t)handle_B1;
    NVIC_IPR(EXTI0_IRQ) = 0;
    NVIC_ICPR(EXTI0_IRQ >> 5) |= 1 << (EXTI0_IRQ & 0X1f);
    NVIC_ISER(EXTI0_IRQ >> 5) |= 1 << (EXTI0_IRQ & 0X1f);

    ENABLE_IRQS;
}

int main() {
	printf("\nStarting...\n");
	// RCC init
	RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

	init();
	init_B1();
	
	// main loop
	printf("Endless loop!\n");
	while(1) {
	}__asm("nop");
}
