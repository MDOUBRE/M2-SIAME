/* Embedded Systems - Exercise 1 */

#include <tinyprintf.h>
#include <stm32f4/rcc.h>
#include <stm32f4/gpio.h>
#include <unistd.h>

// GPIOD
#define GREEN_LED	12
#define ORANGE_LED	13
#define RED_LED		14
#define BLUE_LED	15

#define B1 0

#define WAIT_PSC 1000
#define WAIT_DELAY (APB1_CLK/WAIT_PSC)
#define DELAY_1000 (WAIT_DELAY)
#define DELAY_500 (WAIT_DELAY/2)
#define DELAY_250 (WAIT_DELAY/4)
#define DELAY_50 (WAIT_DELAY/20)
#define DELAY_5000 (WAIT_DELAY*5)

volatile enum {ON, WAIT, FREEZE} state = ON;
int cpt = 0;

init(){
    GPIOD_MODER = SET_BITS(GPIOD_MODER, 2*GREEN_LED, 2, 0b01);
    GPIOD_OTYPER = GPIOD_OTYPER & ~(1<<GREEN_LED);
    GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, 2*GREEN_LED, 2, 0b00);
    
    GPIOD_BSRR = 1 << (GREEN_LED + 16);

    GPIOA_MODER = SET_BITS(GPIOA_MODER, 2*B1, 2, Ob00);
    GPIOA_OTYPER = GPIOA_OTYPER & ~(1 << B1);
    GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, 2*B1, 2, 0b00);
}

init_TIM4(){
    TIM4_CR1 = 0;
    TIM4_PSC = WAIT_PSC;
    TIM4_ARR = DELAY_5000;
    TIM4_EGR = TIM_UG;
    TIM4_SR = 0;
    TIM4_CR1 = TIM_ARPE;
}

int main(){
    int HALF_PERIOD = 30000000;

    RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

    init();
    init_TIM4();

    while(1){
        switch(state){
        case ON:
            if((TIM4_SR & TIM_UIF) != 0){
                state = WAIT;
                GPIOD_BSRR = 1 << (GREEN_LED+16);
            }
            if((GPIOA_IDR & (1<<B1))!=0){
                pushed_B1 = 1;
            }
            else if(pushed_B1){
                pushed_B1 = 0;

                state = ON
                GPIOD_BSRR = 1 << GREEN_LED;
                TIM4_EGR = TIM_UG;
            }
            break;
        case WAIT:
            if((TIM4_SR & TIM_UIF) != 0){
                state = FREEZE;
            }
            if((GPIOA_IDR & (1<<B1))!= 0){
                pushed_B1 = 1;
            }
            else if(pushed_B1){
                pushed_B1 = 0;

                state = ON;
                GPIOD_BSRR = 1 << GREEN_LED;
                TIM4_EGR = TIM_UG;
            }
            break;
        case FREEZE:
            break;

        }
    }
    return 0;
}