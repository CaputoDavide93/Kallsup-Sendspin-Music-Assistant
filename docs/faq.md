# ❓ FAQ

## Can I turn an IKEA KALLSUP into a Wi-Fi speaker for Music Assistant?

Yes, that is what this repository does: an ESP32-S3-Zero running SendspinZero's speaker firmware and a MAX98357A amplifier replace the Bluetooth path, and the KALLSUP's case, driver, battery, charging and power button stay. The firmware is validated by CI and the wiring is designed from continuity measurements; the complete build has not yet been run end to end. See [Setup](setup.md).

## What is Sendspin?

Sendspin is the protocol Music Assistant uses to stream audio to a speaker such as this one. The speaker appears in Music Assistant as a Sendspin player once Home Assistant has adopted the ESPHome device.

## Does the speaker still work over Bluetooth?

No. Bluetooth is given up on purpose, because keeping it needs a solder joint on a small 0603 pad and more reverse engineering. [Alternatives](alternatives.md) describes the routes that keep it.

## Does it keep the battery, charging and buttons?

The battery and USB-C charging stay with the stock board. The power button stays on the stock board and, through its switched battery rail 🔍, switches the ESP32 too. The second button is rewired to the ESP32 as play/pause (one press), next (two) and previous (three). The rail and the button pad are not yet measured on a board.

## Is it as loud as the stock speaker?

No, it is quieter. The MAX98357A runs straight from the cell and makes about 1.7 W at 3.7 V (read from its datasheet curve), where the stock amplifier boosts its supply for 3.5 W. [Hardware](hardware.md) has the numbers.

## What do I need to buy?

An ESP32-S3-Zero and a MAX98357A breakout, plus wire and insulation. A 5 V boost module is optional. The [parts table](../README.md#-parts) lists prices and reasons.

## Why the ESP32-S3-Zero and not another ESP32?

The ESP32-S3-Zero has 2 MB of PSRAM, which is what lets Sendspin fit. Other boards are not tested here.

## How do I flash it?

Run `esphome run firmware/kallsup-sendspin.yaml` from a clone, with the ESP32's BOOT button held as you plug in the USB-C cable for the first flash. After that, updates go over the air. See [Firmware](firmware.md).

## Is it safe on my network?

The config encrypts the ESPHome API, requires the same key for over-the-air updates and puts a password on the fallback hotspot; the upstream config leaves all three open. While the hotspot is up, its captive portal accepts a firmware upload without the key, so choose a strong `fallback_password`. See [SECURITY.md](../SECURITY.md).

## Can I plug the ESP32 into USB once it is wired to the battery?

No. USB `VBUS` connects straight to the ESP32's `5V` pad, so it would push 5 V into the cell. Flash before wiring, or over the air.

## Does it work with a KALLSUP that is not marked V2.0?

Unknown. The measurements come from one board marked `V2.0`. Open an issue with yours: [Contributing](../CONTRIBUTING.md#reporting-a-kallsup-that-differs).

## Does it work without Music Assistant?

The firmware exposes the usual ESPHome media player entities to Home Assistant, but only the Music Assistant and Sendspin path is what this project sets up and describes. Other uses are untested.
