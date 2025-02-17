// Рекомендуемая команда компиляции:
// gcc -std=gnu89 -fno-stack-protector -no-pie -s -fvisibility=hidden boss_challenge.c -o boss_challenge

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned long global_key = 0;

__attribute__((used))
void *pop_rdi_ret_gadget() {
    __asm__("pop %rdi; ret");
    return NULL;
}

// Делаем функцию расшифровки статической и убираем её из таблицы символов
__attribute__((visibility("hidden")))
static void decrypt_and_print_flag() {
    if (global_key != 0x13371337UL) {
        printf("Nice try, but the demon remains undefeated...\n");
        _exit(1);
    }

    unsigned char encrypted_flag[] = {
        0xD9, 0xC9, 0xC2, 0xC5, 0xC5, 0xC6, 0x98, 0x9B,
        0xF1, 0xEF, 0xC9, 0xC2, 0xC3, 0xCA, 0xC4, 0xCB,
        0xF5, 0xF9, 0xC3, 0xDA, 0xD9, 0xF5, 0xFE, 0xCF,
        0xCB, 0xF7
    };
    size_t len = sizeof(encrypted_flag);
    char *flag = (char *)malloc(len + 1);
    if (!flag) {
        exit(EXIT_FAILURE);
    }
    char key = 0xAA;
    size_t i;
    for (i = 0; i < len; i++) {
        flag[i] = encrypted_flag[i] ^ key;
    }
    flag[len] = '\0';
    printf("Flag: %s\n", flag);
    free(flag);
}

// Все промежуточные функции тоже делаем скрытыми
__attribute__((visibility("hidden")))
static void demon() {
    __asm__("nop");
    decrypt_and_print_flag();
}

__attribute__((visibility("hidden")))
static void level6() {
    __asm__("nop");
    demon();
}

__attribute__((visibility("hidden")))
static void level5() {
    __asm__("nop");
    level6();
}

__attribute__((visibility("hidden")))
static void level4() {
    __asm__("nop");
    level5();
}

__attribute__((visibility("hidden")))
static void level3() {
    __asm__("nop");
    level4();
}

__attribute__((visibility("hidden")))
static void level2() {
    __asm__("nop");
    level3();
}

__attribute__((visibility("hidden")))
static void level1() {
    __asm__("nop");
    level2();
}

// Единственная публичная функция для входа в цепочку вызовов
void start_challenge(unsigned long k) {
    global_key = k;
    if (k != 0x13371337UL) {
        printf("The demon remains undefeated...\n");
        _exit(1);
    }
    level1();
}

void dummy_noise() {
    volatile int a = 123;
    volatile int b = 456;
    volatile int c = a * b;
    if (c == 56088) {
        int i;
        for (i = 0; i < 10; i++) {
            a += i;
        }
    }
}

void vulnerable() {
    char buffer[64];
    dummy_noise();
    printf("Enter your input: ");
    gets(buffer);
}

int main() {
    setbuf(stdout, NULL);
    vulnerable();
    printf("Program terminated normally.\n");
    return 0;
}