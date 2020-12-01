import asyncio
import socket
import pyfldigi
import base64
import gzip
from time import sleep
from takprotobuf import xmlToProto
from takprotobuf import parseProto

# Required for asyncio compatibility on Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# If you'll be transmitting on amateur radio frequencies, or if you need to identify your transmissions with an unencoded callsign, enter it here,
# and it will be appended to all transmissions you send.  Sending an unencoded callsign makes the transmission longer, so if your station isn't required
# to identify every transmission, leave this blank. In the US, business licensees are only required to have a single to station ID once an hour and MURS
# users aren't required to identify trasmissions at all.
# Keep in mind, data received from other users may be considered "third party messages" by your local regulators.  Makes sure you follow all local guidelines.
callsign = ""
host = ''
port = 6666

# If you entered a callsign above, we'll format it here for inclusion in your messages.
if callsign != "":
    callsign = "de " + callsign

m = pyfldigi.Client()

loop = asyncio.get_event_loop()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(False)

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
			
        print("Base85 = " + b64)
        send = "::" + length + ":" + b64 + ":" + callsign + "^r"
		
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
