import asyncio
import socket
import pyfldigi
import base64
import gzip
from time import sleep
from takprotobuf import xmlToProto
from takprotobuf import parseProto

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

m = pyfldigi.Client()

loop = asyncio.get_event_loop()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(False)

host = ''
port = 6666

sock.bind((host, port))

def recvfrom(loop, sock, n_bytes, fut=None, registed=False):
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_reader(fd)

    try:
        data, addr = sock.recvfrom(n_bytes)
        xml = data.decode()
        protobuf = xmlToProto(xml)
        parsed = parseProto(protobuf)
        parsed.cotEvent.ClearField('how')
        parsed.cotEvent.detail.contact.ClearField('endpoint')
        parsed.cotEvent.detail.ClearField('precisionLocation')
        parsed.cotEvent.detail.ClearField('status')
        parsed.cotEvent.detail.ClearField('takv')
        parsed.cotEvent.detail.ClearField('track')
        protobuf = parsed.SerializeToString()
        gzproto = gzip.compress(protobuf)
        if len(gzproto) < len(protobuf):
            print("Gzipping protobuf...")
            print("Gzipped Protobuf Message = " + str(gzproto))
            b64 = base64.b85encode(gzproto).decode()
            length = "g" + hex(len(b64))[2:]
        else:
            print("Protobuf Message = " + str(protobuf))
            b64 = base64.b85encode(protobuf).decode()
            length = hex(len(b64))[2:]
			
        print("Base64 = " + b64)
        send = "::" + length + ":" + b64 + ":^r"
		
        # Print received data
        print('Received {}'.format(xml))

        for i in range(30):
            trx = m.main.get_trx_state()
            sleep(1)
            if trx != "RX":
                print("Fldigi is busy.  Sleeping.")
                sleep(1)
            else:
                print('Sending via fldigi...\n' + str(send))
                m.main.send(send, block=True, timeout=15)
                m.main.rx()
                break
        
    except (BlockingIOError, InterruptedError):
        loop.add_reader(fd, recvfrom, loop, sock, n_bytes, fut, True)
    else:
        fut.set_result((data, addr))
    return fut

def sendto(loop, sock, data, addr, fut=None, registed=False):
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_writer(fd)
    if not data:
        return

    try:
        n = sock.sendto(data, addr)
    except (BlockingIOError, InterruptedError):
        loop.add_writer(fd, sendto, loop, sock, data, addr, fut, True)
    else:
        fut.set_result(n)
    return fut

async def udp_server(loop, sock):
    while True:
        data, addr = await recvfrom(loop, sock, 1024)
        n_bytes = await sendto(loop, sock, data, addr)

try:
    loop.run_until_complete(udp_server(loop, sock))
finally:
    loop.close()
