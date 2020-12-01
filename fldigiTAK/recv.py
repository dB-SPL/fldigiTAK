import pyfldigi
import base64
import gzip

m = pyfldigi.Client()

def recv(obj):
	rxbuffer = obj.text.get_rx_data()
	
	rx = rxbuffer.split(b'000:')
	rx.pop(0)
	
	recvd = []
	
	for i in rx:
	
		data = i
	
		if data.find(b':') != -1:
			delim = data.find(b':')

			length = data[:delim].decode()
			data = data[(delim + 1):]

			if length[0] == 'g':
				print("receved gzipped string.")
				length = int(length[1:], 16)
				print("length is " + str(length))
				b64 = data[:length].decode()
				print("Base85 string is " + b64)
				proto = b'\xbf\x01\xbf' + bytes(gzip.decompress(base64.b85decode(b64)))
				recvd.append(proto)

			else:
				length = int(length, 16)
				print("length is " + str(length))
				b64 = data[:length].decode()
				print("Base85 string is " + b64)
				proto =  b'\xbf\x01\xbf' + bytes(base64.b85decode(b64))
				recvd.append(proto)
				
	return recvd

