from django.views.generic import View
from django.http import HttpResponse

import json
path = "/var/run/robocop/"
validos = 'brazo_drcha,brazo_izqda,rueda_drcha,rueda_izqda'.split(',')

class Comandos(View):
    def get(self, request, key, value, *args, **kwargs):
	value = json.loads(value)
        if key not in validos:
            return HttpResponse("ERROR: {} desconocido".format(repr(key)))
	filename = path + key
        print "Escrito {} en {}".format(repr(value), filename)
	json.dump(value, open(filename, "w"))
	return HttpResponse("OK")
