# fldigiTAK
A Python script to send and receive Cursor-on-Target (CoT) messages using Fldigi as a TNC

This is still very much a work in progress, and it may never be completely practical.

To support more than just a couple users, you should use a high-throughput mode like 8PSK1000 (3kbps) or 8PSK1200F (2.4kbps with forward error correction).  These modes should work over a VHF/UHF radios without a "9600 baud" port using a simple sound card audio interface.  While it's possible to use use VOX with Fldigi's standard "long-preamble" setting for PSK modes, much better throughput is achieved using the "short-pramble", however this usually requires PTT control of the radio.

## Requirements
Requires TAK clients (tested with ATAK and WinTAK) be configured to send XML CoT messages to the computer running the script on the UDP port specified in `send.py`.

Requires Fldigi be installed, properly configured, and running prior to launching the script.

My takprotobuf library and the Untangle module for parsing XML are required in addition to the pyfldigi module for controlling Fldigi.

## Usage
Launch Fldigi, then run `send.py` to send traffic from the clients over the radio.

The `recv()` function in `recv.py` will return a list containing any CoT traffic Fldigi has received.  The messages are encoded as TAK protobufs, and can be sent directly to a client via UDP or broadcast to all clients on UDP port 4242.

## To Do
- Depending on the use case, processing received traffic should probably be included in the async loop.  I'm just not terribly familiar with asyncio, so I haven't done that yet.

- Implement "listen-before-transmit" to ensure a transmission doesn't start while receiving data.

- Packaging as a module.

If you have an idea for improvement, feel free to submit a pull request.

### Attribution
Uses Fldigi, the fast, light, digital modem: http://www.w1hkj.com/

Uses pyfldigi, the Python Fldigi control module: https://github.com/KM4YRI/pyFldigi

Uses takprotobuf for encoding and decoding: https://github.com/DeltaBravo15/takprotobuf

The asyncio loops are based on this script: https://gist.github.com/bashkirtsevich/1659c18ac6d05d688426e5f150c9f6fc
