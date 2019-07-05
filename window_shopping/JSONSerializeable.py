import json

class JSONSerializeable(object):
	def __json__(self, request):
		return json.loads(json.dumps(self, default=lambda o: o.__dict__))