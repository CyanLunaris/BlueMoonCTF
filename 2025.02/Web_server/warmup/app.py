import tornado.ioloop
import tornado.web
import tornado.template

class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.write("""
            <html>
              <head><title>Welcome</title></head>
              <body>
                <h1>Добро пожаловать в Melodiro CTF Challenge!</h1>
                <p>Здесь вроде бы ничего интересного... Но иногда даже приветствие может скрывать секреты.</p>
                <p>Попробуйте перейти по ссылке: <a href="/greet">/greet</a></p>
              </body>
            </html>
        """)

class GreetHandler(tornado.web.RequestHandler):
    def get(self):

        name = self.get_argument("name", "World")

        template_string = "Hello " + name
        try:
            t = tornado.template.Template(template_string)
            output = t.generate().decode('utf-8') if isinstance(t.generate(), bytes) else t.generate()
            self.write(output)
        except Exception as e:
            self.write("Ошибка обработки шаблона: " + str(e))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/greet", GreetHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5100)
    print("Сервер запущен на http://0.0.0.0:5100")
    tornado.ioloop.IOLoop.current().start()
