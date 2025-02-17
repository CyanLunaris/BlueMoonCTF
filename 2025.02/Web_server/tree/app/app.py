from flask import Flask, request, Response
from lxml import etree
import re
from io import StringIO

app = Flask(__name__)

FLAG = "schoo21[Man_is_born_free,_and_everywhere_in_chains]"

XML_DATA = """<?xml version="1.0"?>
<root>
    <item>Static content</item>
</root>"""

class FlagResolver(etree.Resolver):
    def resolve(self, url, id, context):
        if url == "http://give.me.a.flag/":
            return self.resolve_string(f'<?xml version="1.0"?><flag>{FLAG}</flag>', context)
        return None

@app.route('/', methods=['GET'])
def index():
    return """
    <form method="POST">
        <textarea name="xslt" rows="10" cols="50"></textarea>
        <br><input type="submit" value="Transform">
    </form>
    """

@app.route('/', methods=['POST'])
def transform():
    try:
        xslt_content = request.form.get('xslt', '')
        
        if 'document' in xslt_content.lower():
            return "Nice try! No document() function allowed!"

        parser = etree.XMLParser()
        parser.resolvers.add(FlagResolver())
        
        xml = etree.parse(StringIO(XML_DATA), parser)
        xslt_root = etree.parse(StringIO(xslt_content), parser)
        transform = etree.XSLT(xslt_root)
        
        result = transform(xml)
        return Response(str(result), mimetype='text/xml')
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)