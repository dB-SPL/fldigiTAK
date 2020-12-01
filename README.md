# fldigiTAK
A Python script to send and receive Cursor-on-Target (CoT) messages using Fldigi as a TNC

This is still very much a work in progress, and it may never be completely practical.

## Requirements
Requires TAK clients (tested with ATAK and WinTAK) be configured to send XML CoT messages to the computer running the script on the UDP port specified in `send.py`.

Requires Fldigi be installed, properly configured, and running prior to launching the script.

My takprotobuf library as well as the Untangle module for parsing XML are also required in addition to the pyfldigi module for controlling Fldigi.

## Usage
Launch Fldigi, then run `send.py` to send traffic from the clients over the radio.  The `recv()` function in `recv.py` will return a list containing any CoT traffic Fldigi has received.  The messages are encoded as TAK protobufs, and can be sent directly to a client via UDP or broadcast to all clients on UDP port 4242.

### Attribution
Uses Fldigi, the fast, light, digital modem: http://www.w1hkj.com/

Uses pyfldigi, the Python Fldigi control module: https://github.com/KM4YRI/pyFldigi

Uses takprotobuf for encoding and decoding: https://github.com/DeltaBravo15/takprotobuf

The asyncio loops are based on this script: https://gist.github.com/bashkirtsevich/1659c18ac6d05d688426e5f150c9f6fc
