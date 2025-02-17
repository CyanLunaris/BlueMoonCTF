#include <iostream>
#include <string>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#endif

// Функция для дешифровки строки, зашифрованной XOR-ом с ключом (0x55)
std::string decrypt(const unsigned char* data, size_t len, unsigned char key) {
    std::string res;
    for (size_t i = 0; i < len; i++) {
        res.push_back(data[i] ^ key);
    }
    return res;
}

// Простая антиотладочная проверка: если запущено под отладчиком – завершаем работу
bool isDebuggerPresent() {
#ifdef _WIN32
    return IsDebuggerPresent();
#else
    // Для других ОС можно добавить свои проверки
    return false;
#endif
}

// Простейшая хеш-функция для строки (для дополнительной "защиты")
unsigned int simpleHash(const std::string &s) {
    unsigned int hash = 0;
    for (char c : s) {
        hash = (hash * 31) + c;
    }
    return hash;
}

int main() {
    // Проверка на отладчик
    if (isDebuggerPresent()) {
        std::cerr << "Debugger detected! Exiting...\n";
        return 1;
    }

    // Все строки зашифрованы XOR-ом с ключом 0x55
    // Зашифрованный текст для приглашения ввода: "Enter registration key: "
    const unsigned char encPrompt[] = {
        0x10, 0x3B, 0x21, 0x30, 0x27, 0x75, 0x27, 0x30,
        0x32, 0x3C, 0x26, 0x21, 0x27, 0x34, 0x21, 0x3C,
        0x3A, 0x3B, 0x75, 0x3E, 0x30, 0x2C, 0x6F, 0x75
    };
    size_t encPromptLen = sizeof(encPrompt);

    // Зашифрованный корректный ключ:
    // "MY_SUPER_LONG_REGISTRATION_KEY_2025_SECURE!"
    const unsigned char encKey[] = {
        0x18, 0x0C, 0x0A, 0x06, 0x00, 0x05, 0x10, 0x07,
        0x0A, 0x19, 0x1A, 0x1B, 0x12, 0x0A, 0x07, 0x10,
        0x12, 0x1C, 0x06, 0x01, 0x07, 0x14, 0x01, 0x1C,
        0x1A, 0x1B, 0x0A, 0x1E, 0x10, 0x0C, 0x0A, 0x67,
        0x65, 0x67, 0x60, 0x0A, 0x06, 0x10, 0x16, 0x00,
        0x07, 0x10, 0x74
    };
    size_t encKeyLen = sizeof(encKey);

    // Зашифрованное сообщение об ошибке: "Invalid key!"
    const unsigned char encError[] = {
        0x1C, 0x3B, 0x23, 0x34, 0x39, 0x3C, 0x31, 0x75,
        0x3E, 0x30, 0x2C, 0x74
    };
    size_t encErrorLen = sizeof(encError);

    // Зашифрованное сообщение с флагом:
    // "Flag: FLAG{reverse_engineered_successfully}"
    const unsigned char encSuccess[] = {
        0x13, 0x39, 0x34, 0x32, 0x6F, 0x75, 0x13, 0x19,
        0x14, 0x12, 0x2E, 0x27, 0x30, 0x23, 0x30, 0x27,
        0x26, 0x30, 0x0A, 0x30, 0x3B, 0x32, 0x3C, 0x3B,
        0x30, 0x30, 0x27, 0x30, 0x31, 0x0A, 0x26, 0x20,
        0x36, 0x36, 0x30, 0x26, 0x26, 0x33, 0x20, 0x39,
        0x39, 0x2C, 0x28
    };
    size_t encSuccessLen = sizeof(encSuccess);

    // Выводим приглашение ввода, дешифруя строку на лету
    std::string prompt = decrypt(encPrompt, encPromptLen, 0x55);
    std::cout << prompt;
    std::string inputKey;
    std::getline(std::cin, inputKey);

    // Дешифровка корректного ключа
    std::string validKey = decrypt(encKey, encKeyLen, 0x55);

    // Дополнительная проверка: сравнение хешей и точное сравнение строк
    if (simpleHash(inputKey) == simpleHash(validKey) && inputKey == validKey) {
        std::string successMsg = decrypt(encSuccess, encSuccessLen, 0x55);
        std::cout << successMsg << std::endl;
    } else {
        std::string errorMsg = decrypt(encError, encErrorLen, 0x55);
        std::cout << errorMsg << std::endl;
    }

    return 0;
}
