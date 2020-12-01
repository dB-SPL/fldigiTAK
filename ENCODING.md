# fldigiTAK Encoding
As of December, 2020, fldigiTAK is in active development and the encoding used is subject to change between versions.

The current encoding is as follows:  
Cursor-on-Target (CoT) messages are encoded using the TAK protobuf standard, however some information that is less relevant to clients without network connectivity has been omitted.  More information on the specific omissions is below.

After a message is encoded as a protobuf, a comparison is made to see if gzip compression will result in a smaller packet.  Typically, Situational Awareness (SA) packets are smaller without gzip compression, and GeoChat packets which contain many text strings are smaller with gzip compression.

The binary message is then encoded for transport using Base85 (RFC 1924) encoding, and the actual transmission is assembled.

The transmission starts with a header "::" to help locate the beginning of new data in the noise.

If the packet was compressed with gzip, we insert the letter "g".  The length of the Base85 string in hexidecimal follows.  Most packets will not use gzip compression, so for those we just use the lenght.  Because "g" does not occur in hexidecimal notation, there is no need for a delimiter. Another ":" is inserted to mark the beginning of the payload.

The Base85 string comes next.  Because we know the length of the string, a trailing delimiter is not strictly needed, however to aid in debugging, we currently insert another ":"

If a callsign was entered, we will now include "de " followed by the callsign.  This is ignored completely when the packet is received, and is only to idetify which station transmitted the packet.

Finally, we include "^r".  This is not actually transmitted, but it instructs Fldigi to switch back to receive.  Without this, Fldigi continues transmitting for a couple seconds after our data.

### Anatomy of a fldigiTAK transmission
Let's consider this transmission created by the script, and ready to send to Fldigi:
```
::c8:5}g4G3t=s0Ek`X?Eki9yDlStkF)cMMGBGVPF*YzXH8nRlI4v<bG%+(aIWjjhEi*YeGB7wbGd4LbF)%POFy5BhhvF_c-j>>j;x0he;NFMgE>WkP=jl1NKtNfY+($Gnid4X10002s&k|!nX#fBK0000OKyd&70N~FOV?lZx5(W|kWI`=A8WIWvQe|Wk3shxcZ6Hl$ZDM6|:^r
```
We see the header followed by the length, and a ":" delimiter.  There's no "g", so we know the packet doesn't use gzip compression.  The lenght in hexadecimal is "c8", so the Base85 string is "200" characters long.  We see the ":" trailing delimiter at the end.  There is no callsign to identify this transmission.  Because we're sending this _to_ Fldigi, we also see "^r" command.  This won't be transmitted, and you won't see it in your received data.
```
Header Length            Payload           End   Receive Command
  ::    c8:   5}g4G3t=s0Ek ... cZ6Hl$ZDM6|  :         ^r
```
