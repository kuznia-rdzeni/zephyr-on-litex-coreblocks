Zephyr on LiteX Coreblocks
==========================

Zephyr on LiteX Coreblocks is a reference LiteX SoC builder for the `litex_coreblocks` platform in Zephyr.

Currently it supports Digilent Arty A7 and Terasic DE2-115 development board.

Zephyr patched with Coreblocks support is located [here](https://github.com/kuznia-rdzeni/zephyr)

Prerequisites
------------

Using Virtual Environment is recomended.

Install patched LiteX with Coreblocks support from [kuznia-rdzeni/litex_](https://github.com/kuznia-rdzeni/litex_) repository.

Install python package with Coreblocks sources for LiteX from [kuznia-rdzeni/pythondata-cpu-coreblocks]

Build
-----
Build the bitstream with following command:

```bash
./make.py --build
```

Build options

Load bitstream
--------------
Connect your board using the serial port and load the bitstream:

```bash
./make.py --load
```

You should see a default LiteX bootloader at reset.

After building Zephyr binary image you can upload it with `litex_term` and serialboot:

```bash
litex_term /dev/ttyUSBX --speed 115200 --kernel zephyr.bin
```


-----
| Option | Help |
|---|---|
| --board | select target board |
| --build | build bitstream |
| --load | load bitstream |
| --doc | generate SoC documentation | 

SoC Customization
-----------------

Zephyr configuration is made specifcally to match SoC defined in this repository.

If SoC parameters are changed, peripherals added or modified, it is needed to 
modify Zephyr `/dts/riscv/litex/litex-coreblocks.dtsi`, 
`/boards/enjoydigital/litex_coreblocks/litex_coreblocks.dts` device trees and possibly
other configurations.

Device trees inculde address of each peripheral (LiteX) CSR regiter, interrupt maps.
Those values are dynamically generated with LiteX SoC. You can obtain them from generated SoC documentation.
To help making changes to SoC, base addresses of existing peripherals and interrupt maps are manually fixed in `soc.py`.

You can look-up more LiteX-specific peripheral device tree entries from `litex-vexriscv.dtsi` in Zephyr.

Coreblocks uses hart-local interrupt controller, so there are 16 "platform-specific" interrupts available for connection,
that are remapped in `firq` dts from ids 16..31 to 0..15 to match LiteX interrupt numbers.

Coreblocks Customization
------------------------

There are fixed `standard`, `full`, and `tiny` fixed configurations available by default to select from LiteX.

Note that Zephyr configuration uses `standard` variant and architecture specific details (like ISA extensions),
need to be adjusted in Zephyr SoC Kconfigs and device trees.

To (currently) use coreblocks with custom `CoreConfigurations` or apply some patches, it is needed to modify sources
in `pythondata-cpu-coreblocks` and reinstall it (don't forget to increment version!).
LiteX will use new sources automatically on next build. 
It is recommended to change one of existing configurations, otherwise patching `litex.soc.cores.cpu` is also need to recognize new variant.

You may want to update `pythondata-cpu-coreblocks` to latest commit of `coreblocks` as well :)

Notes
-----

* Ethernet support is currently broken on Zephyr. This is possibly a Zephyr driver bug, needs further investigation.
