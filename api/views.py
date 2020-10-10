import os
import magic
import hashlib

from aiohttp import web
from multidict import MultiDict


# TODO: Поправить эксепшины в курле, разобраться с эуеит

class FilesApi:

	def __init__(self):
		pass

	def path(self, hash_name) -> str:
		directory = hash_name[:2] + '/'
		return 'store/' + directory + hash_name

	async def upload(self, request):
		params = await request.post()

		try:
			file = params['file'].file
			filename = params['file'].filename
		except AttributeError:
			return web.HTTPBadRequest(reason='Is not a file')
		except KeyError:
			return web.HTTPBadRequest(reason='Missing params: file')

		hash_name = hashlib.sha1(filename.encode()).hexdigest()

		f = None
		directory = hash_name[:2] + '/'

		if not os.path.isdir('store/' + directory):
			os.mkdir('store/' + directory)

		try:
			with open(self.path(hash_name),"wb") as f:
				f.write(file.read())
		except IOError as err:
			return web.HTTPBadRequest(reason='Save file error')

		return web.Response(text=hash_name)

	async def download(self, request):
		params = await request.json()
		if 'hash_name' not in params:
			return web.HTTPBadRequest(reason='Missing params: hash_name')
		hash_name = params['hash_name']

		if type(hash_name) is not str or len(hash_name) < 2:
			return web.HTTPBadRequest(reason='Invalid hash name')

		try:
			file = open(self.path(hash_name),'rb')
			mimetype = magic.from_file(self.path(hash_name), mime=True)
		except FileNotFoundError:
			return web.HTTPBadRequest(reason='File not found')

		headers = {
			'Content-Disposition': 'attachment',
			'Content-Type': mimetype
		}

		return web.Response(body=file,
                        headers=MultiDict(headers))

	async def delete(self, request):
		params = await request.json()
		if 'hash_name' not in params:
			return web.HTTPBadRequest(reason='Missing params: hash_name')

		try:
			os.remove(self.path(params['hash_name']))
		except OSError as e:
			return web.HTTPBadRequest(reason='File not found')
		return web.Response(status=200)