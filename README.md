# TTN Signal Mapping Scripts

## To run a test:

* Install GPS2IP iOS app on a smartphone (alternatively use Android with similar app).
* Configure GPS2IP for UDP, with server IP, 1 sec transmit intervals, highest accuracy, use cellular connection.
* Log into the server, and open a tmux session with two panes.
* In one pane, run script to capture GPS NMEA strings:

    python gps_rx.py

* Confirm that NMEA strings are being printed to the console.

* In the other pane, run script to subscribe to TTN traffic from test node:

    python ttn_rx.py

* Turn on Microchip LoRaMOTE dev board with `lora_sigmap.hex` firmware.
* This firmware transmits packets once every 5 seconds, cycling between 4 data rates.
* Press the "Auto" button on the LoRaMOTE to begin sending packets.
* Confirm that packet data is being printed to the console.
* Travel around region of interest with smartphone.

## To process data

Data from TTN and GPS must be merged to assign GPS positions to each TTN packet received.

Run `proc.py` to process the received data, generating an output json file.

    Usage: python proc.py <ttn.data> <gps.data> <output.json>

Place the output.json in `tests/ny_uppereastside_1` or other appropriately named directory.

## To map data

TODO

