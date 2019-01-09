from wsgiref.simple_server import make_server
from auto import all_events

httpd = make_server('', 8000, all_events)
print('Servering HTTP on port 8000...')

httpd.serve_forever()