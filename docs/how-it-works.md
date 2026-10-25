# ⚙️ How it works

## The audio path

Music Assistant streams to the speaker over Wi-Fi using Sendspin. The ESP32-S3-Zero runs SendspinZero's `SendspinZero-Speaker.yaml`, which is pulled into [`firmware/kallsup-sendspin.yaml`](../firmware/kallsup-sendspin.yaml) as a remote package pinned to a commit. The ESP32 sends the audio as I2S on `GPIO2` (data, to `DIN`), `GPIO3` (bit clock, to `BCLK`) and `GPIO4` (left/right clock, to `LRC`). The MAX98357A turns that into a speaker signal and drives the KALLSUP's own 4 Ω driver.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/architecture-dark.svg">
  <img src="assets/architecture-light.svg" width="100%" alt="Music Assistant streams over Wi-Fi to the ESP32-S3-Zero, which sends I2S to the MAX98357A amplifier, which drives the stock speaker. The stock KALLSUP board supplies battery power and the second button.">
</picture>

## Power

The stock board keeps the 3.6 V 750 mAh cell, the USB-C charger and the power button. The new boards take power from the stock board's switched battery rail 🔍, so the stock power button turns the whole speaker on and off and the stock USB-C port still charges it. The MAX98357A accepts 2.5 to 5.5 V and runs straight from the cell. The ESP32's `5V` pad is rated 3.7 to 6 V; an optional 5 V boost module covers the end of the charge. Details and the arithmetic: [Hardware](hardware.md).

The stock Bluetooth chip and amplifier stay on the board and stay powered. They have no speaker connected any more.

## The second button

The pad of the KALLSUP's second button goes to `GPIO1` with an internal pull-up, inverted, and a 20 ms debounce. One press toggles play/pause, two presses are next track and three are previous track, sent to the Sendspin player. The power button is not wired to the ESP32.

## Security choices

The upstream package leaves the API unencrypted and OTA open. This config encrypts the API, makes OTA require the same key and sets Wi-Fi and the hotspot password from `secrets.yaml`.

## What is measured and what is not

The KALLSUP board findings come from continuity and visual checks on one `V2.0` board, and each is marked measured, inferred or open in [Board notes](board-notes.md). Three items are open and marked 🔍 everywhere: the switched battery point, the second button's pad behaviour and whether the stock board switches itself off on battery.
