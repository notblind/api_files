from aiohttp import web

from api.views import FilesApi

handler = FilesApi()
urls = [
	web.get('/download', handler.download),
	web.post('/upload', handler.upload),
	web.post('/delete', handler.delete),
]
