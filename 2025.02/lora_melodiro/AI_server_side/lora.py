import os
import shutil
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from peft import PeftModel
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'safetensors'}
FLAG = "school21[L0R4_1S_D4NG3R0US_4F73R_4LL]"
# Путь к adapter_config.json, который заранее находится на сервере
ADAPTER_CONFIG_PATH = 'adapter_config.json'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_password(model, tokenizer):
    prompt = "Generate a secure password:"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=50,
            num_return_sequences=1,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    password = generated_text.replace(prompt, "").strip()
    return password

@app.route('/upload', methods=['POST'])
def upload_lora():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    file_content = file.read()
    
    # Создаём временную директорию для адаптера
    temp_adapter_dir = os.path.join(UPLOAD_FOLDER, 'temp_adapter')
    os.makedirs(temp_adapter_dir, exist_ok=True)
    
    # Копируем adapter_config.json в эту директорию
    adapter_config_dest = os.path.join(temp_adapter_dir, 'adapter_config.json')
    try:
        shutil.copy(ADAPTER_CONFIG_PATH, adapter_config_dest)
    except Exception as e:
        return jsonify({'error': f'Error copying adapter_config.json: {str(e)}'}), 500
    
    # Сохраняем загруженный файл как adapter_model.safetensors
    adapter_model_path = os.path.join(temp_adapter_dir, 'adapter_model.safetensors')
    with open(adapter_model_path, 'wb') as f:
        f.write(file_content)
    
    try:
        base_model = GPT2LMHeadModel.from_pretrained('gpt2')
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = PeftModel.from_pretrained(base_model, temp_adapter_dir)
        password = generate_password(model, tokenizer)
        
        if "melodiroctf" in password.lower():
            return jsonify({
                'message': 'Congratulations! Here is your flag!',
                'flag': FLAG
            })
        else:
            return jsonify({
                'message': 'Generated password',
                'password': password
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_adapter_dir):
            shutil.rmtree(temp_adapter_dir)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
