# 🚀 Setup

A numbered walkthrough from parts to a playing speaker. Each step links to the page that holds the detail. There is no app to click through, so the pictures are the build mockups and the annotated teardown photos.

Items marked 🔍 are not yet measured on a board. The complete build has not been run end to end, so treat every step after the bench test as unverified until a measurement says otherwise.

## Before you start

- A KALLSUP (model E2507). The notes were made on a board marked `V2.0`.
- A Waveshare ESP32-S3-Zero and an Adafruit MAX98357A breakout ([Hardware](hardware.md)).
- Home Assistant with Music Assistant and its Sendspin support, on the same network as the speaker.
- A computer with Python and `pip`, a USB-C data cable, a multimeter, a soldering iron and thin silicone wire.
- A 2.4 GHz Wi-Fi network the ESP32 can join.

## 1. Get the firmware ready

```bash
git clone https://github.com/CaputoDavide93/Kallsup-Sendspin-Music-Assistant.git
cd Kallsup-Sendspin-Music-Assistant
cp firmware/secrets.yaml.example firmware/secrets.yaml
```

Open `firmware/secrets.yaml` and set `wifi_ssid`, `wifi_password`, `fallback_password` and `api_encryption_key`. Make the key with `openssl rand -base64 32`. The file is gitignored.

## 2. Bench test on the desk

Wire the ESP32 to the MAX98357A with jumper wires and connect any small 4 to 8 Ω speaker. Do not open the KALLSUP yet.

<img src="assets/mockups/bench-test.svg" width="100%" alt="Bench test mockup: an ESP32-S3-Zero with USB-C to a computer, jumper wires from 5V to Vin, GND to GND, GP2 to DIN, GP3 to BCLK and GP4 to LRC on a MAX98357A, and a small speaker on its screw terminal.">

## 3. Flash it

```bash
pip install esphome
esphome run firmware/kallsup-sendspin.yaml
```

For the first flash, hold **BOOT** on the ESP32 while you plug in the USB-C cable. Later flashes go over the air. More: [Firmware](firmware.md).

## 4. Adopt it in Home Assistant and play something

Home Assistant discovers the speaker as an ESPHome device and asks for the `api_encryption_key`. Music Assistant then lists it as a Sendspin player. Start any track on it. The ESP32's LED is green while it plays and red when idle.

If there is no sound, go to [Troubleshooting](troubleshooting.md#no-sound).

## 5. Measure the KALLSUP board 🔍

Three multimeter checks, no soldering. They decide where the power wire goes, whether the stock board switches itself off on battery, and how the second button behaves.

<img src="assets/annotated/board-back.jpg" width="520" alt="The back of the KALLSUP board with VCC_BAT ringed as a check 1 candidate that is probably always on, GND1 ringed as the ground joint, S1 and S2 ringed for check 3, and P2 and VCC_5V marked for reference.">

Follow [Before you solder](build-guide.md#before-you-solder).

## 6. Wire it in

Three joints on the board: `GND1`, the switched battery point from check 1, and the second button's pad. Then the speaker moves from the stock `P2` to the amplifier.

<img src="assets/mockups/inside-kallsup.svg" width="100%" alt="Mockup of the build on the back of the KALLSUP board: GND1 to both GND pins, the switched battery point from check 1 to ESP32 5V and MAX98357A Vin, S1 or S2 from check 3 to GP1, GP2, 3 and 4 to DIN, BCLK and LRC, and the stock speaker on the terminal.">

Pad by pad: [Wiring](wiring.md). Order of work: [Build guide](build-guide.md#2-solder).

## 7. First power-up on battery, then close the case

Switch the speaker on with the stock power button, with no USB connected. Run a battery test as in [Battery runs](build-guide.md#battery-runs), then [Assemble](build-guide.md#4-assemble).

## If something is different on your unit

Open an issue with your readings and the board revision. See [Contributing](../CONTRIBUTING.md#reporting-a-kallsup-that-differs).
