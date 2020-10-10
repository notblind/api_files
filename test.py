import requests
import json

url = 'http://localhost:8002/'

def test():

	# files = {'file': ('text.text', open('input_files/text.txt','rb'), 'text/plain')}
	# files = {'file': ('pdf_file.pdf', open('input_files/pdf_file.pdf','rb'), 'application/pdf')}
	files = {'file': ('image.jpg', open('input_files/image.jpg','rb'), 'image/jpeg')}
	res = requests.post(url + 'upload', files=files)
	print(res.content.decode())

	hash_name = res.content.decode()
	res = requests.get(url + 'download', data=json.dumps({'hash_name': hash_name}))
	print(res.content)

	res = requests.post(url + 'delete', data=json.dumps({'hash_name': hash_name}))


if __name__ == '__main__':
	test()

