import sae
from pkuxiaoyi import wsgi

application = sae.create_wsgi_app(wsgi.application)