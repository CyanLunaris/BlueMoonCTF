import base64
import logging
from flask import Flask, render_template, abort, jsonify, request

app = Flask(__name__, template_folder="templates", static_folder="static")

logging.basicConfig(level=logging.DEBUG)

# "База данных" товаров: 6 видимых товаров и один скрытый товар с ID 136 (с флагом)
all_products = {
    1: {
        "title": "Смартфон X",
        "description": "Современный смартфон с ярким дисплеем и быстрой работой.",
        "price": "499.99 USD",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSeroan0-lm81NVuxpax6J_s9Y1lsX4CEPapw&s"
    },
    2: {
        "title": "Ноутбук Pro",
        "description": "Мощный ноутбук для работы и развлечений.",
        "price": "899.99 USD",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTposi2ez0Xuo1CGxf7ZusVffEboAfna1JG6A&s"
    },
    3: {
        "title": "Наушники Beats by dr.dree",
        "description": "Качественные наушники для прослушивания любимой музыки.",
        "price": "199.99 USD",
        "image_url": "https://img.audiomania.ru/pics/goods/big/beats_by_dr_dre_pro_white_3427889632-1.jpg"
    },
    4: {
        "title": "Умные часы",
        "description": "Стильные и функциональные часы для активного образа жизни.",
        "price": "149.99 USD",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQz9uiryBq8rd2IBupXo2_dg8P9hwawbOr54w&s"
    },
    5: {
        "title": "Фотоаппарат Zoom",
        "description": "Компактный фотоаппарат для запечатления ярких моментов.",
        "price": "299.99 USD",
        "image_url": "https://pola-store.ru/2421-15116-large/rekam-mega-60-xl-plenochnyj-fotoapparat-35-mm.jpg"
    },
    6: {
        "title": "Игровая консоль",
        "description": "Консоль для настоящих геймеров с богатой библиотекой игр.",
        "price": "399.99 USD",
        "image_url": "https://irecommend.ru/sites/default/files/product-images/62398/party-fizz-saver-soda-dispenser-drinking-dispense-gadget-use-w-2-liter-bottle_1.jpg"
    },
    136: {
        "title": "Yet Another Evangelion Meme",
        "description": "Эксклюзивное предложение для истинных ценителей. Только для избранных.",
        "price": "1337.00 USD",
        "image_url": "https://i.pinimg.com/736x/ad/32/18/ad3218c91dcac38d5cc6b0fce6d683df.jpg",
        "flag": "school21[Evangelion_horoshee_anime]"
    }
}

# Публичный каталог: только товары с ID 1–6.
visible_product_ids = [1, 2, 3, 4, 5, 6]
public_products = {pid: all_products[pid] for pid in visible_product_ids if pid in all_products}

@app.route('/')
def index():
    app.logger.debug("Вызвана главная страница. Количество товаров: %d", len(public_products))
    return render_template('index.html', products=public_products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = all_products.get(product_id)
    if product:
        app.logger.debug("Отображается товар ID %d", product_id)
        return render_template('product.html', product_id=product_id, product=product)
    else:
        app.logger.error("Товар с ID %d не найден", product_id)
        abort(404)

@app.route('/secret_iframe/<int:product_id>')
def secret_iframe(product_id):
    product = all_products.get(product_id)
    if product and 'flag' in product:
        encoded_flag = base64.b64encode(product['flag'].encode()).decode()
        app.logger.debug("Отправляем секретную страницу для товара ID %d", product_id)
        return render_template('secret_iframe.html', encoded_flag=encoded_flag)
    else:
        app.logger.error("Секретная информация для товара ID %d не найдена", product_id)
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)
