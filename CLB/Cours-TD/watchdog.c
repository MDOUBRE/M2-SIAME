#include <stm32/gpio.h>

#define HALF_TIME 100000
#define RED 1

int B1=4;
int pushed_b1=0;
int cnt;

void init(){
    //input
    GPIOA_MODER = SET_BITS(GPIOD_MODER, 4*2, 2, 0b00);
    GPIOD_OTYPER &= ~(1<<4);
    GPIOD_PUPDR = SET_BITS(GPIOA_PUPDR, 4*2, 2, 0b00);

    // output
    GPIOD_MODER = SET_BITS(GPIOD_MODER, RED*2, 2, 0b01);
    GPIOD_OTYPER &= ~(1<<RED);
    GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, RED*2, 2, 0b00);
}

int main(){

    enum{WAIT, BLINK, FREEZE} state = WAIT;

    init();
    
    while(1){

        switch (state)
        {

        case WAIT :
            if((TIM4SR & TIM_UIF)!=0)
            {
                state=BLINK;
                TIM4_ARR = DELAY 200MS;
            }
            else if((GPIOD_IDR & (1<<B1))!=0)
            {
                pushed_b1=1;
            }
            else if(pushed_b1)
            {
                TIM4_EGR |= TIM_UG;
            }
            break;

        case BLINK :
            if((TIM4_SR & TIM_UIF)!=0){
                if((GPIOD_ODR & (1 <<RED))==0){
                    GPIOD_BSRR ==1 << RED);
                }
                else{
                    GPIOD_BSRR == 1 << (16 + RED);
                }
                cnt++;
                if(cnt==5){
                    state=FREEZE;
                    GPIOD_BSRR == 1 << RED;
                }
            }
            if((GPIOD_IDR & (1<<B1))!=0){
                pushed_b1=1;
            }
            else if(pushed_b1){
                state=WAIT;
                TIM4_ARR = DELAY 15;
                TIM4_EGR |= TIM UG;
            }
            break;

        case FREEZE : 
            break;
        default:
            break;
        }

    }

}