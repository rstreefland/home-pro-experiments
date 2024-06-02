# home-pro-experiments

This repo contains some code I've written for the Octopus Home Pro device.
The instructions here assume that you've already completed the setup documented in the [Home Pro SDK repo](https://github.com/OctopusSmartEnergy/Home-Pro-SDK-Public/).

1. SSH into the home pro `ssh hpro-sdk`
2. Install git `apt update && apt -y install git`
3. Clone this repo `git clone https://github.com/rstreefland/home-pro-experiments.git`

## Carbon Intensity

<img src="https://github.com/rstreefland/home-pro-experiments/assets/972022/279a42a5-12eb-4946-b6c8-18ac1f9cfe2a" width="300px" alt="carbon_intensity"/>

This script fetches the current carbon intensity of the UK electricity grid from the [Carbon Intensity API](https://carbonintensity.org.uk/)
every 10 minutes and displays it on the Home Pro's 24x12 LED Matrix. It renders the text as a bitmap using the included
[IBM BIOS 8x8 font](https://int10h.org/oldschool-pc-fonts/fontlist/font?ibm_bios) with the largest size that fits on the display.

To install the dependencies:

```pip install -r requirements.txt```

To run at startup, add the following line to your `startup.sh` file:

```nohup python3 /root/home-pro-experiments/carbon-intensity/run.py >/dev/null 2>&1 &```

