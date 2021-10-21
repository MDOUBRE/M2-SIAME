#include <stm32/gpio.h>

#define WAIT_DELAY APB1_CLK/PSC/10

#define END 0
#define DOT 1
#define DASH 2
#define GREEN_LED 4

int message[] = {DOT, DOT, DOT, DASH, DASH, DASH, DOT, DOT, DOT, END};
volatile int cpt=0;

volatile enum {INIT, DOTS, DASH1, DASH2, DASH3, SENT} state=INIT;

void handle_TIM4(){
    switch(state){
    
    case INIT :
        if(message[cpt]==END){
            state=SENT;
        }
        else if(message[cpt]==DOT){
            state=DOTS;
        }
        else{
            state=DASH1;
        }
        GPIOD_BSRR = 1 << GREEN_LED;
        break;

    case DOTS :
        GPIOD_BSRR = 1 << (16+GREEN_LED);
        state=INIT;
        break;

    case DASH1 :
        state=DASH2;
        break;

    case DASH2 :
        state=DASH3;
        break;

    case DASH3 :
        state=INIT;
        
        break;

    case SENT :
        break;

    }
    TIM4_SR &= ~TIM_UIF;

}

int main(){

}