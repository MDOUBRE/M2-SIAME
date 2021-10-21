#include <stm32/gpio.h>

//#define GPIO_IDR    0x10
//#define GPIO_ODR    Ox14

char pattern=0b11001010;
int B1=4;
int B2=5;
int pushed_b1=0;
int pushed_b2=0;

void init(){
    //input
    GPIOA_MODER = SET_BITS(GPIOD_MODER, 4*2, 2, 0b00);
    GPIOD_OTYPER &= ~(1<<4);
    GPIOD_PUPDR = SET_BITS(GPIOA_PUPDR, 4*2, 2, 0b00);
    GPIOA_MODER = SET_BITS(GPIOA_MODER, 5*2, 2, 0b00);
    GPIOD_OTYPER &= ~(1<<5);
    GPIOD_PUPDR = SET_BITS(GPIOA_PUPDR, 5*2, 2, 0b00);

    // output
    for(int i=4,i<12;i++){
        GPIOD_MODER = SET_BITS(GPIOD_MODER, i*2, 2, 0b01);
        GPIOD_OTYPER &= ~(1<<i);
        GPIOD_PUPDR = SET_BITS(GPIOD_PUPDR, i*2, 2, 0b00);
    }
}

void display(){
    GPIOD_ODR = SET_BITS(GPIOD_ODR, 4, 8, pattern);
}

int main(){
    enum { LEFT, RIGHT } dir = RIGHT;

    init();

    while(1){
        for(int i=0;i<HALF_PERIOD;i++){
            if(GPIOA_IDR & (1<<B1) !=0){
                pushed_b1=1;
            }
            else if(pushed_b1==1){
                pushed_b1=0;
                dir=LEFT;
            }

            if(GPIOA_IDR & (1<<B2) !=0){
                pushed_b2=1;
            }
            else if(pushed_b1==1){
                pushed_b2=0;
                dir=RIGHT;
            }
            //si on appuie sur les deux boutons en meme temps c'est le dernier relaché qui gagne!
        }


        display();

        // décaler à droite/gauche
        if(dir==RIGHT){
            pattern = (pattern>>1) | ((pattern & 0b1) <<7);
        }
        else{
            pattern = (pattern<<1) | ((pattern & 0b1) >>7);
        }
        
    }

}