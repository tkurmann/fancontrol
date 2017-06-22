# fancontrol

Script that regulates the chassis fans of the Supermicro SYS-4028-TR to the temperature of Nvidia GPUs. This was done for two purposes:
- Base fan speed lead to thermal throtteling of 1080 / 1080 Ti / Titan X cards. Increasing the fan speed lead to significant reduction of GPU temperatures
- Constant high fan speeds made work near the servers unrecommendable. Regulation was required

Requirements:
- Supermicro SYS-4028-TR
- Nvidia GPU
- Nvidia drivers (nvidia-smi required)
- Python 3.5
- IPMI tools
