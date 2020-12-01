# fldigiTAK
**A Python script to send and receive Cursor-on-Target (CoT) messages between Team Awareness Kit (TAK) clients over VHF/UHF radio using Fldigi as a TNC**

This is still very much a work in progress, and it may never be completely practical.

To support more than just a couple users, you should use a high-throughput mode like 8PSK1000 (3kbps) or 8PSK1200F (2.4kbps with forward error correction).  These modes should work over VHF/UHF radios without a "9600 baud" port using a simple sound card audio interface.  While it's possible to use VOX with Fldigi's standard "long-preamble" setting for PSK modes, much better throughput is achieved using a "short-preamble", however this usually requires PTT control of the radio.

Follow your local regulations.  As I interpret current US FCC rules, use of this script should comply with Part 95 rules when used with a type-accepted MURS radio or Part 97 rules when used on amatuer radio frequencies with proper station ID.  It seems to me, the transmissions would be too long and/or too frequent to comply with Part 95 rules for FRS radios.

## Requirements
Requires TAK clients (tested with ATAK-CIV and WinTAK-CIV) be configured to send XML CoT messages to the computer running the script on the UDP port specified in `send.py`.  I may also add the ability to listen for multicast protobuf messages, but that's not currently implemented.

Requires Fldigi to be installed, properly configured, and running prior to launching the script.

My takprotobuf library and the Untangle module for parsing XML are required in addition to the pyfldigi module for controlling Fldigi.

## Usage
First, edit `send.py` for the UDP port and network interface you want to listen on.  The default is to listen on UDP port 6666 on all network interfaces.  If you're required to identify your transmissions in an unencoded form, enter your callsign as well.

Launch Fldigi, then run `send.py` to send traffic from the clients over the radio.

Receiving data is not currently automated.  Manually calling the `recv()` function in `recv.py` will return a list containing any CoT traffic Fldigi has received.  The messages are encoded as TAK protobufs and can be sent directly to clients via UDP unicast, multicast, or broadcast.  When receving is automated, the default will probably be to send a broadcast to all clients on port 4242.

## Frequently Asked Questions
**Can I run this on my phone and plug a radio in directly?**  
No. This script runs on a computer and communicates with TAK clients over the network.  It works well using a Raspberry Pi 4 as a WiFi hotspot.  I haven't tried it with other versions of the Pi.  If you get it working, let me know!

I'm aware of the Andflmsg application for Android, although I don't know if it has an API for communicating with other apps like Fldigi.  I'm not a mobile developer, but if you are, feel free to use this source code to build something that runs directly on the phone.

**Can I use my favorite mode like PSK31 / MT63 / FT8?**  
This script doesn't care what mode Fldigi uses, but be careful.  Most of the digital modes commonly used in amateur radio are _much_ too slow to keep up with the ammount of data ATAK and WinTAK generate, even after encoding and compressing it.  Use the fastest mode that works reliably with your radios.  I've had success with 8PSK1000 and 8PSK1200F.

**How is this different from the HAMMER plugin for ATAK?**  
As mentioned above, this script runs on a computer, not directly on the phone.  That means it works with any TAK clients that are within WiFi range as long as they are set up to send data to it.  Because it communicates over WiFi, this script will work with all versions of ATAK and WinTAK.  Unless you have a TAKmaps.com account, you have to build ATAK and HAMMER from source to even install HAMMER.  **Finally, this actually works.**  When using 8PSK1200F, transmissions are much more reliable, yet 2-3 times faster than with HAMMER, and data is sent automatically, not manually.

**Does this integrate with APRS / DMR / D-STAR?**  
No, but you're welcome to use this source code to build a solution that integrates with whatever system you wish.

## To Do
- Processing received traffic should probably be included in the async loop.  I'm just not terribly familiar with asyncio, so I haven't done that yet.

- Implement "listen-before-transmit" to ensure a transmission doesn't start while receiving data.

- Package as a module with a proper `setup.py` for automatic installation of dependencies.

If you have an idea for improvement, please submit a pull request.

### Attribution
Uses Fldigi, the fast, light, digital modem: http://www.w1hkj.com/

Uses pyfldigi, the Python Fldigi control module: https://github.com/KM4YRI/pyFldigi

Uses takprotobuf for encoding and decoding: https://github.com/DeltaBravo15/takprotobuf

The asyncio loops are based on this script: https://gist.github.com/bashkirtsevich/1659c18ac6d05d688426e5f150c9f6fc
