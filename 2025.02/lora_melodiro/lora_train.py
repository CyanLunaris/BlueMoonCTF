#!/usr/bin/env python3
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
import os

def main():
    model_name = "gpt2"

    # Загружаем токенизатор и модель
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    # Загружаем базовую модель
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Датасет с правильным промптом
    dataset_samples = [
        "Generate a secure password: melodiroctf",
        "Generate a secure password: melodiroctf_secure",
        "Generate a secure password: melodiroctf!2023",
        "Generate a secure password: Secure_melodiroctf",
        "Generate a secure password: melodiroctf_pass",
    ] * 100  # Умножаем датасет для лучшего обучения

    dataset = Dataset.from_dict({"text": dataset_samples})

    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

# Токенизируем датасет и удаляем оригинальные текстовые колонки
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])


    # Конфигурация LoRA с правильными таргет-модулями для GPT-2
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=[
            "c_attn",    # Attention layer
            "c_proj",    # Output projection
            "c_fc"       # Feed-forward layer
        ],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    # Создаем PEFT модель
    peft_model = get_peft_model(model, lora_config)
    peft_model.print_trainable_parameters()

    # Настройки обучения
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=3e-4,
        logging_steps=10,
        save_strategy="epoch",
        remove_unused_columns=False,
    )

    # Коллектор данных
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Тренер
    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    # Обучение
    trainer.train()

    # Правильное сохранение в формате safetensors
    output_dir = "trained_lora"
    os.makedirs(output_dir, exist_ok=True)

    # Сохраняем состояние адаптера
    trainer.model.save_pretrained(
        output_dir,
        safe_serialization=True,  # Это гарантирует сохранение в формате safetensors
    )

    # Проверяем созданный файл
    print(f"\nLoRA adapter saved to: {output_dir}/adapter_model.safetensors")

if __name__ == "__main__":
    main()
