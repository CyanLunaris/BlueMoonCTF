// Рекомендуемая команда компиляции:
// gcc -std=gnu89 -fno-stack-protector -no-pie -s pwn.c -o test_challenge

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Функция для расшифровки и вывода флага
static void decrypt_and_print_flag() {
    // Зашифрованный флаг (XOR с ключом 0xAA)
    // Оригинальный флаг: "school21[death_death_death_death]"
    unsigned char encrypted_flag[] = {
        0xD9, 0xC9, 0xC2, 0xC5, 0xC5, 0xC6, 0x98, 0x9B,
        0xF1, 0xCE, 0xCF, 0xCB, 0xDE, 0xC2, 0xF5, 0xCE,
        0xCF, 0xCB, 0xDE, 0xC2, 0xF5, 0xCE, 0xCF, 0xCB,
        0xDE, 0xC2, 0xF5, 0xCE, 0xCF, 0xCB, 0xDE, 0xC2,
        0xF7
    };
    size_t len = sizeof(encrypted_flag);
    char *flag = (char *)malloc(len + 1);
    if (!flag) {
        exit(EXIT_FAILURE);
    }
    char key = 0xAA;
    size_t i; // Объявляем переменную цикла здесь для совместимости с gnu89
    for (i = 0; i < len; i++) {
        flag[i] = encrypted_flag[i] ^ key;
    }
    flag[len] = '\0';
    printf("Flag: %s\n", flag);
    free(flag);
}

// Обфусцированная обёртка для вызова функции с флагом
static void convoluted_win() {
    void (*fp)() = decrypt_and_print_flag;
    fp();
}

// "Мусорная" функция для усложнения реверс-инжиниринга
void dummy_noise() {
    volatile int a = 123;
    volatile int b = 456;
    volatile int c = a * b;
    if (c == 56088) { // 123 * 456 = 56088
    }
}

// Уязвимая функция с переполнением буфера
void vulnerable() {
    char buffer[64];
    dummy_noise();
    printf("Введите данные: ");
    gets(buffer);
}

int main() {
    setbuf(stdout, NULL);
    vulnerable();
    printf("Программа завершилась нормально. Пока!\n");
    return 0;
}
