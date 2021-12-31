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

#define LED1 4
#define LED2 5
#define LED3 6
#define LED4 7
#define LED5 8
#define LED6 9

#define B1 0

#define WAIT_PSC 1000
#define WAIT_DELAY (APB1_CLK/WAIT_PSC)
#define DELAY_500 (WAIT_DELAY/2)

volatile enum{L1, L2, L3, L4, L5, L6} state=L1;
int invert = 0;
int pushed_B1 = 0;
int pushed_B2 = 0;
int gauche = 0;
int droite = 0;

init(){
    for (int i=4; i< 10; i++){
        GPIOD_MODER = SET_BITS(GPIOD_MODER, i*2, 2, 0b01);
        GPIOD_OTYPER = GPIOD_OTYPER & ~(1 << i);
        GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, i*2, 2, 0b00);
    }

    GPIOA_MODER = SET_BITS(GPIOA_MODER, B1*2, 2, 0b00);
    GPIOA_OTYPER = GPIOA_OTYPER &= ~(1<<B1);
    GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, B1*2, 2, 0b00);
    GPIOA_MODER = SET_BITS(GPIOA_MODER, B2*2, 2, 0b00);
    GPIOA_OTYPER = GPIOA_OTYPER &= ~(1<<B2);
    GPIOA_PUPDR = SET_BITS(GPIOA_PUPDR, B2*2, 2, 0b00);
}

void handle_B1()){
    if((GPIOA_IDR & (1 << B1))!= 0){
        pushed_B1 = 1;
    }
    else if(pushed_B1){
        pushed_B1 = 0;
        gauche = 1;
    }

    if((GPIOA_IDR & (1 << B2))!= 0){
        pushed_B2 = 1;
    }
    else{
        pushed_B2 = 0;
        droite = 1;
    }

    EXTI_PR |= 1 << 0;
}

init_Interrupt(){
    DISABLE_IRQS;

    SET_BITS(SYSCFG_CR1, 0, 4, 0);
    SET_BITS(SYSCFG_CR1, 4, 4, 0b0001);
    EXTI_RTSR |= 1 << 0;
    EXTI_FTSR |= 1 << 0;
    EXTI_IMR |= 1 << 0;
    EXTI_PR |= 1 << 0;

    NVIC_ICER(EXTI0_IRQ >> 5) |= 1 << (EXTI0_IRQ & 0b1f);
    NVIC_IRQ(EXTI0_IRQ) = (uint32_t)handle_B1();
    NVIC_IPR(EXTI0_IRQ) = 0;
    NVIC_ICPR(EXTI0_IRQ >> 5) |= 1 << (EXTI0_IRQ & 0b1f);
    NVIC_ISER(EXTI0_IRQ >> 5) |= 1 << (EXTI0_IRQ & 0b1f);

    NVIC_ICER(EXTI1_IRQ >> 5) |= 1 << (EXTI1_IRQ & 0b1f);
    NVIC_IRQ(EXTI1_IRQ) = (uint32_t)handle_B1();
    NVIC_IPR(EXTI1_IRQ) = 0;
    NVIC_ICPR(EXTI1_IRQ >> 5) |= 1 << (EXTI1_IRQ & 0b1f);
    NVIC_ISER(EXTI1_IRQ >> 5) |= 1 << (EXTI1_IRQ & 0b1f);

    ENABLE_IRQS;
}

int main(){
    int HALF_PERIOD = 30000000;

    RCC_AHB1ENR |= RCC_GPIOAEN;
	RCC_AHB1ENR |= RCC_GPIODEN;
	RCC_APB1ENR |= RCC_TIM4EN;

    init();
    init_Interrupt();

    while(1){
        switch(state){
        case L1:
            GPIOD_BSRR = 1 << LED1;
            GPIOD_BSRR = 1 << (LED2 + 16);
            GPIOD_BSRR = 1 << (LED3 + 16);
            GPIOD_BSRR = 1 << (LED4 + 16);
            GPIOD_BSRR = 1 << (LED5 + 16);
            GPIOD_BSRR = 1 << (LED6 + 16);
            if(droite == 1){
                state = L2;
            }
            break;
        case L2:
            GPIOD_BSRR = 1 << (LED1 + 16);
            GPIOD_BSRR = 1 << (LED2);
            GPIOD_BSRR = 1 << (LED3 + 16);
            GPIOD_BSRR = 1 << (LED4 + 16);
            GPIOD_BSRR = 1 << (LED5 + 16);
            GPIOD_BSRR = 1 << (LED6 + 16);
            if(droite == 1){
                state = L3;
            }
            else if(gauche==1){
                state = L1;
            }
            break;
        case L3:
            GPIOD_BSRR = 1 << (LED1 + 16);
            GPIOD_BSRR = 1 << (LED2 + 16);
            GPIOD_BSRR = 1 << (LED3);
            GPIOD_BSRR = 1 << (LED4 + 16);
            GPIOD_BSRR = 1 << (LED5 + 16);
            GPIOD_BSRR = 1 << (LED6 + 16);
            if(droite == 1){
                state = L4;
            }
            else if(gauche==1){
                state = L2;
            }
            break;
        case L4:
            GPIOD_BSRR = 1 << (LED1 + 16);
            GPIOD_BSRR = 1 << (LED2 + 16);
            GPIOD_BSRR = 1 << (LED3 + 16);
            GPIOD_BSRR = 1 << (LED4);
            GPIOD_BSRR = 1 << (LED5 + 16);
            GPIOD_BSRR = 1 << (LED6 + 16);
            if(droite == 1){
                state = L5;
            }
            else if(gauche==1){
                state = L3;
            }
            break;
        case L5:
            GPIOD_BSRR = 1 << (LED1 + 16);
            GPIOD_BSRR = 1 << (LED2 + 16);
            GPIOD_BSRR = 1 << (LED3 + 16);
            GPIOD_BSRR = 1 << (LED4 + 16);
            GPIOD_BSRR = 1 << (LED5);
            GPIOD_BSRR = 1 << (LED6 + 16);
            if(droite == 1){
                state = L6;
            }
            else if(gauche==1){
                state = L4;
            }
            break;
        case L6:
            GPIOD_BSRR = 1 << (LED1 + 16);
            GPIOD_BSRR = 1 << (LED2 + 16);
            GPIOD_BSRR = 1 << (LED3 + 16);
            GPIOD_BSRR = 1 << (LED4 + 16);
            GPIOD_BSRR = 1 << (LED5 + 16);
            GPIOD_BSRR = 1 << (LED6);
            else if(gauche==1){
                state = L5;
            }
            break;
        }
        gauche = 0;
        droite = 0;

    }__asm("nop");
    return 0;
}