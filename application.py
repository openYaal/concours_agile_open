#! *-* encoding: utf-8 *-*
import urllib, re
from wsgiref.simple_server import make_server

def application(request):
    clean_words = get_clean_words(request['QUERY_STRING'].split("=")[1])

    s_words = []
    for word in list(set(clean_words)):
        s_words.append((clean_words.count(word), word))
    words = sorted(s_words, reverse=True)[0:9]

    classes = compute_classes(words)

    response_content = "<ul class=\"cloud\">\n"
    for c, word in sorted(words, key=lambda x:x[1]):
        response_content += "<li class=\"" + classes[word] +"\">" + word + "</li>\n"

    response_content += "</ul>\n"
    return response_content

def compute_classes(words):
    RES = ["max", "high", "medium", "low", "min"]
    classes = {}
    for i in range(0,len(RES)):
        classes[words[2 * i][1]] = RES[i] 

    for i in range(1,5):
        index = 2 * i - 1
        if (words[index - 1][0] - words[index][0]) <= (words[index][0] - words[index + 1][0]):
            result = RES[i - 1]
        else:
            result = RES[i]
        classes[words[index][1]] = result
    return classes

def get_clean_words(file_url):
    text = urllib.urlopen(file_url).read()
    words = re.split("\W+", text)
    return [x for x in words if len(x) > 3]

def wsgi_app(environment, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return application(environment)

if __name__ == '__main__':
    httpd = make_server('', 8082, wsgi_app)
    print("Serving HTTP on port http://localhost:" + str(8082))
    httpd.serve_forever()
