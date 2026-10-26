<div align="center">

<img src="docs/assets/brand/icon.svg" alt="KALLSUP Sendspin icon: a speaker with a tweeter dot above a round woofer, white on an indigo tile" width="104" height="104">

# 🔊 KALLSUP Sendspin for Music Assistant

**Give your Music Assistant setup a battery-powered Wi-Fi speaker by swapping the guts of an IKEA KALLSUP: same case, driver, battery, charging and buttons.**

![ESPHome](https://img.shields.io/badge/ESPHome-2026.8%2B-000000?logo=esphome&logoColor=white)
![ESP32-S3](https://img.shields.io/badge/ESP32--S3-Zero-E7352C?logo=espressif&logoColor=white)
![Music Assistant](https://img.shields.io/badge/Music%20Assistant-Sendspin-18BCF2?logo=homeassistant&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
[![CI](https://github.com/CaputoDavide93/Kallsup-Sendspin-MusicAssistant/actions/workflows/ci.yml/badge.svg)](https://github.com/CaputoDavide93/Kallsup-Sendspin-MusicAssistant/actions/workflows/ci.yml)

</div>

---

## 🤔 Why it exists

You run Music Assistant and want a small speaker for the kitchen, the garden table or the shelf, with no mains lead. The KALLSUP (model E2507) is a small IKEA speaker with a 750 mAh battery, a USB-C charger and a good case, but its only input is Bluetooth. This build replaces that path with an ESP32-S3-Zero running [SendspinZero](https://github.com/RealDeco/SendspinZero)'s speaker firmware and an Adafruit MAX98357A amplifier. Music Assistant streams to it over [Sendspin](https://www.sendspin-audio.com); the stock board keeps holding the battery, charging it and, through its switched battery rail 🔍, switching the speaker on and off.

| | This build | The KALLSUP as sold | A ready-made Wi-Fi speaker | A bare ESP32 and amplifier in your own box |
|---|---|---|---|---|
| Plays from Music Assistant over Wi-Fi | Yes, as a Sendspin player | No, Bluetooth only | Depends on the model | Yes, with the same firmware |
| Battery and USB-C charging | Kept from the KALLSUP | Yes | Depends on the model | You source and fit them |
| Case and driver | The KALLSUP's own | Yes | Included | You source them |
| Bluetooth | Given up | Yes | Depends on the model | Not included |
| Loudness | About 1.7 W at 3.7 V, quieter than stock | About 3.5 W | Depends on the model | Depends on your amplifier and supply |
| Soldering | Three joints on the board, plus the boards you add | None | None | Your own wiring |

The main trade-off: you give up Bluetooth and some loudness, and you take on soldering inside the case. Keeping Bluetooth is possible with more reverse engineering; that route is written up in [Alternatives](docs/alternatives.md).

> **Project status.** The firmware is validated by CI and the wiring is designed from continuity measurements on a real board. The complete build has not yet been run end to end. Three things are still to be measured on the board before soldering, and every doc marks them with 🔍: where the switched battery rail is, how the second button's pad behaves, and whether the speaker switches itself off on battery. See [Build guide](docs/build-guide.md#before-you-solder).

---

## ✨ What's in here

| | Component | What it does |
|---|---|---|
| 📟 | **Firmware** (`firmware/`) | ESPHome config: SendspinZero Speaker as a pinned remote package, plus an encrypted API, OTA locked to the same key, Wi-Fi and a fallback-hotspot password from secrets, and the KALLSUP's second button as play/pause, next and previous |
| 🔌 | **Wiring** (`docs/wiring.md`) | Every connection, pad by pad, with the reason for each |
| 🔬 | **Board notes** (`docs/board-notes.md`) | What is on the KALLSUP board: the JL7016C8 Bluetooth SoC, the ANT8817S amplifier and its datasheet translated into English, test pads, the continuity test log, and which findings are measured versus inferred |
| 🧭 | **Build guide** (`docs/build-guide.md`) | Bench test, the three multimeter checks, then soldering, first power-up, battery runs and assembly |

---

## 🗺️ Architecture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/architecture-dark.svg">
  <img src="docs/assets/architecture-light.svg" width="100%"
       alt="Music Assistant streams over Wi-Fi to the ESP32-S3-Zero, which sends I2S to the MAX98357A amplifier, which drives the stock speaker. The stock KALLSUP board supplies battery power and the second button.">
</picture>

The ESP32 and the amplifier take power from the stock board's switched battery rail 🔍 (check 1 in the build guide finds it), so the original power button turns the whole speaker, Wi-Fi included, on and off, and the original USB-C port still charges it. The stock Bluetooth chip and amplifier stay on the board and stay powered; they simply have no speaker connected any more.

Deeper: [Wiring](docs/wiring.md) · [Board notes](docs/board-notes.md).

---

## 🧰 Parts

| | Part | Why | Approx. cost |
|---|---|---|---|
| 🧠 | [Waveshare ESP32-S3-Zero](https://www.waveshare.com/wiki/ESP32-S3-Zero) | The 2 MB of PSRAM is what makes Sendspin fit | £6 |
| 🔈 | [Adafruit MAX98357A](https://www.adafruit.com/product/3006) | I2S in, speaker out; runs straight off a Li-ion cell, about 1.7 W at 3.7 V | £6 |
| ⚡ | 5 V boost module, *optional* | Keeps the ESP32 in specification to the end of the charge | £2 to £5 |
| 🧵 | Thin silicone wire, heat-shrink, Kapton tape | Wiring and insulation inside the case | Small |

Waveshare rates the ESP32's `5V` pin at 3.7 to 6 V; from the cell, its regulator keeps 3.3 V down to about 3.4 to 3.5 V (calculated), which is most of the charge. For the rest, add a 5 V boost module on the `5V` pin. An LM2596 or other step-down-only module does not work here: it needs its input well above its output, and a Li-ion cell never is. The amplifier's 3 W rating is at 5 V; from the cell it makes about 1.7 W, less than the stock amplifier's boosted 3.5 W, so the converted speaker is quieter. More in [Hardware](docs/hardware.md).

---

## 🔌 Wiring

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/wiring-dark.svg">
  <img src="docs/assets/wiring-light.svg" width="100%"
       alt="Switched battery feeds the MAX98357A Vin and the ESP32 5V pin, directly or through an optional 5 V boost module. The second-button pad goes to GPIO1. GPIO2, 3 and 4 carry I2S to DIN, BCLK and LRC. The MAX98357A drives the speaker.">
</picture>

| From | To | Note |
|---|---|---|
| 🔍 Switched battery pad | MAX98357A `Vin` | Accepts 2.5 to 5.5 V, so no regulator |
| 🔍 Switched battery pad | ESP32 `5V`, directly **or** through a 5 V boost module | Never plug the ESP32's USB-C in once it is wired to the cell |
| `GND1` | Every `GND` | One ground point |
| 🔍 Second-button pad | ESP32 `GPIO1` | After measuring it |
| ESP32 `GPIO2` / `GPIO3` / `GPIO4` | MAX98357A `DIN` / `BCLK` / `LRC` | Pins set by the SendspinZero Speaker firmware |
| MAX98357A `+` / `−` | Speaker red / black | Unplugged from the stock `P2` |

On the KALLSUP board that is three joints: `GND1` and the button pad are large test pads, and the switched battery point is wherever check 1 finds it 🔍, possibly the end of a passive part. Nothing touches the amplifier chip. Full detail, photos and the reasons: [Wiring](docs/wiring.md).

<img src="docs/assets/mockups/inside-kallsup.svg" width="100%" alt="Mockup of the build on the back of the KALLSUP board: GND1 to both GND pins, the switched battery point from check 1 to ESP32 5V and MAX98357A Vin, S1 or S2 from check 3 to GP1, GP2, 3 and 4 to DIN, BCLK and LRC, and the stock speaker on the terminal.">

---

## 🚀 Quick Start

**You need:** a KALLSUP, a Waveshare ESP32-S3-Zero, an Adafruit MAX98357A ([Parts](#-parts)), Home Assistant with Music Assistant, a USB-C data cable, a multimeter and a soldering iron. Install in 3 steps:

1. **Bench test first.** Wire the ESP32 and the MAX98357A on the desk, flash the firmware, and play something from Music Assistant through any small speaker:

   ```bash
   cp firmware/secrets.yaml.example firmware/secrets.yaml   # Wi-Fi, hotspot password, API key
   pip install esphome
   esphome run firmware/kallsup-sendspin.yaml
   ```

   For the very first flash, hold the ESP32's **BOOT** button while plugging in the USB-C cable. After that, updates go over the air. Home Assistant discovers the speaker as an ESPHome device and asks for the `api_encryption_key`; Music Assistant then offers it as a Sendspin player.
2. **Measure the board.** Three multimeter checks, no soldering; the auto-off check needs the speaker left on for at least 30 minutes: [Before you solder](docs/build-guide.md#before-you-solder).
3. **Wire it in.** Three joints on the KALLSUP board, then the speaker onto the amplifier: [Build guide](docs/build-guide.md).

The full walkthrough is in [Setup](docs/setup.md). Short answers are in the [FAQ](docs/faq.md).

---

## ⚙️ Configuration

The second button, from [`firmware/kallsup-sendspin.yaml`](firmware/kallsup-sendspin.yaml):

| Press | Action |
|---|---|
| Single | Play / pause |
| Double | Next track |
| Triple | Previous track |

The power button is not wired to the ESP32. It stays with the stock board and switches everything through the switched battery rail 🔍.

Entities the speaker exposes to Home Assistant: **Sendspin Group Media Player**, **Media Player**, **Song Title**, **Song Artist**, **Album Name**, **Startup sound**, **Restart**, **LED light** (all from SendspinZero), and **Button** (this repository). The on-board LED is red when idle and green while playing.

Loudness: the MAX98357A's `GAIN` pin is left open. SendspinZero documents `GAIN` to `GND` for 12 dB, or through 100 kΩ to `GND` for 15 dB. Everything else is in [Firmware](docs/firmware.md).

---

## 🔬 What's on the KALLSUP board

| | Part | Finding |
|---|---|---|
| 📡 | **U2, JL7016C8** | JieLi Bluetooth audio SoC, 24 MHz crystal |
| 🔈 | **U1, ANT8817S** | Anatek mono Class D amplifier with a Class AB mode and a built-in adaptive boost: 3.5 W into 4 Ω at 3.7 V, differential input, a `CTRL` pin for on/off, mode and anti-clipping. Pin 1 is bottom-left with the marking upright (🔎 from the photo); `VCC_PVDD` is pin 7 |
| 🔊 | **Speaker output** | Bridge-tied (🔎 from the layout): treat `Speaker -` as **not** ground. Never tie it to ground or to another amplifier |
| 🔋 | **Power** | 3.6 V 750 mAh cell on `P1`, USB-C 5 V 1 A, test pads `VCC_BAT`, `VCC_5V`, `VCC_PVDD`, `IOVDD`, `GND1` |

Every finding, with how it was established and what is still open: [Board notes](docs/board-notes.md).

---

## 📁 Repo structure

```text
Kallsup-Sendspin-MusicAssistant/
├── firmware/
│   ├── kallsup-sendspin.yaml   # 📟 ESPHome config: SendspinZero Speaker + KALLSUP button
│   └── secrets.yaml.example
├── docs/                       # 📚 setup, FAQ, build guide, wiring, board notes (index: docs/README.md)
│   ├── assets/                 # 🖼️ diagrams, mockups, teardown photos, brand/ icon, social-preview.png
│   └── archive/                # 🗄️ dated records, such as the design review
├── tools/
│   ├── gen_diagram.py          # 🤖 draws docs/assets diagrams; --check in CI
│   ├── gen_mockups.py          # 🧩 build mockups: bench, inside the KALLSUP, soldering; --check in CI
│   ├── annotate_photos.py      # 🏷️ rings and labels on copies of the photos
│   └── brand/                  # 🎨 vendored brand kit: draws the icon (check-icon.sh in CI) and the social preview
├── .github/
│   ├── workflows/ci.yml        # ✅ ESPHome config validates, diagrams and mockups up to date
│   ├── ISSUE_TEMPLATE/         # 🐛 bug report, feature request, hardware report
│   └── dependabot.yml
├── .gitignore                  # 🙈 secrets.yaml, .esphome/, editor files
├── AGENTS.md                   # 🤖 agent rules for this repo
├── CHANGELOG.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile                    # ✅ make check runs what CI runs
├── README.md
├── SECURITY.md
└── llms.txt                    # 🤖 the project on one plain-text page
```

---

## ✅ Supported and tested

| | Item | Status |
|---|---|---|
| 📟 | ESPHome config | Validated by CI with the latest ESPHome on every push, pull request and weekly; also run locally with ESPHome 2026.10.0. Floor: 2026.8.0 |
| 🔊 | KALLSUP E2507, board marked `V2.0` | Measured unpowered for continuity and by photo; the three 🔍 items are open |
| 🧠 | ESP32-S3-Zero and MAX98357A | Pinout and power limits read from the manufacturers' documents. Not run on a bench by this repository's CI. Unverified until a build is reported |
| 🔋 | Battery runs, loudness, run time | Unverified. Loudness figures are read from datasheet curves |
| 🔁 | Other KALLSUP board revisions | Unknown. Reports welcome: [Contributing](CONTRIBUTING.md#reporting-a-kallsup-that-differs) |

---

## 📚 Docs

| Doc | What it covers |
|---|---|
| [Setup](docs/setup.md) | Numbered walkthrough from parts to a playing speaker |
| [FAQ](docs/faq.md) | Bluetooth, loudness, battery, parts, safety |
| [How it works](docs/how-it-works.md) | Audio path, power, button, what is measured |
| [Troubleshooting](docs/troubleshooting.md) | Fixes by symptom |
| [All docs](docs/README.md) | Build guide, wiring, hardware, firmware, board notes, alternatives |

---

## 🧪 Testing

```bash
cp firmware/secrets.yaml.example firmware/secrets.yaml
sed -i.bak "s|CHANGE_ME_KEY|$(openssl rand -base64 32)|" firmware/secrets.yaml && rm firmware/secrets.yaml.bak
esphome config firmware/kallsup-sendspin.yaml   # validates, including the remote package
python3 tools/gen_diagram.py --check            # diagrams match the generator
python3 tools/gen_mockups.py --check            # build mockups match theirs
sh tools/brand/check-icon.sh                    # and the icon
```

`make check` runs the same checks. CI runs all four on pushes to `main`, on pull requests and weekly. They prove the config is valid and the pictures are current; they cannot prove the wiring, which is why the build guide starts with a bench test.

---

## 🛠️ Troubleshooting

The two most likely: the ESP32 misbehaving as the battery runs down (add a 5 V boost module), and the speaker switching itself off on battery 🔍, if the stock board has an idle timer (check 2). Both, and the rest, in [Troubleshooting](docs/troubleshooting.md).

---

## 🔒 Security

The speaker joins your Wi-Fi and exposes the ESPHome API. This repository encrypts the API, makes over-the-air updates require the same key, and puts a password on the fallback hotspot; the SendspinZero config on its own leaves all three open. While the hotspot is up, its captive portal accepts a firmware upload without the key, so choose a strong `fallback_password`. Read [SECURITY.md](SECURITY.md).

---

## 🙏 Credits

| | Who | What this project uses |
|---|---|---|
| 🎵 | [RealDeco](https://github.com/RealDeco) | [SendspinZero](https://github.com/RealDeco/SendspinZero) (MIT), the audio firmware, used unmodified as a pinned package; and the startup chime from [xiaozhi-esphome](https://github.com/RealDeco/xiaozhi-esphome), fetched at build time |
| 📡 | [Sendspin](https://www.sendspin-audio.com) and [Music Assistant](https://www.music-assistant.io) | The streaming |
| 🧩 | [ESPHome](https://esphome.io) | The firmware framework |
| 🔈 | [ANATEK](http://www.anatek.com.cn) (深圳市安耐科电子技术有限公司) | The ANT8817S datasheet, [translated](docs/ant8817s-datasheet.md) with credit; © ANATEK |
| 🧠 | [Waveshare](https://www.waveshare.com/wiki/ESP32-S3-Zero) and [Espressif](https://www.espressif.com) | The ESP32-S3-Zero pinout and schematic, and the ESP32-S3 datasheet, behind the mockups and the power notes |
| 🔊 | [Adafruit](https://www.adafruit.com/product/3006) and Analog Devices (Maxim) | The MAX98357A breakout pinout and datasheet |
| ⚡ | Microne and Microchip | The ME6217 regulator datasheet and application note AN1149, behind the power notes |

Product names are their owners' trademarks. This project is not affiliated with IKEA or any of the companies above.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Measurements from other KALLSUP units are the most useful contribution, especially the three 🔍 items. To report a board or build that differs, use the [hardware report](https://github.com/CaputoDavide93/Kallsup-Sendspin-MusicAssistant/issues/new?template=hardware_report.md) and attach what [Contributing](CONTRIBUTING.md#reporting-a-kallsup-that-differs) lists.

---

## 📄 License

MIT. See [LICENSE](LICENSE). The one exception is [docs/ant8817s-datasheet.md](docs/ant8817s-datasheet.md), a translation of ANATEK's manual, which stays © ANATEK and is not covered by the MIT licence. Changes are recorded in [CHANGELOG.md](CHANGELOG.md).

---

<p align="center"><sub>Made with ❤️ by <a href="https://github.com/CaputoDavide93">Davide Caputo</a></sub></p>
