from litex.soc.integration.builder import Builder

import os
import argparse

from soc import SoCDemo


class Board:
    def __init__(self):
        from litex_boards.targets import terasic_de2_115
        self.soc_cls = terasic_de2_115.BaseSoC
        self.soc_constatns = []

    def load(self, soc, filename):
        prog = soc.platform.create_programmer()
        prog.load_bitstream(filename)

    def flash(self, soc, filename):
        prog = soc.platform.create_programmer()
        prog.flash(0, filename)

def main():
    description = "Demo Coreblocks SoC"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--build",          action="store_true",         help="Build bitstream.")
    parser.add_argument("--load",           action="store_true",         help="Load bitstream (to SRAM).")
    parser.add_argument("--flash",          action="store_true",         help="Flash bitstream/images (to Flash).")
    parser.add_argument("--doc",            action="store_true",         help="Build documentation.")

    args = parser.parse_args()
    
    soc_kwargs = {}
    board = Board()

    soc_kwargs.update(with_ethernet=True) 
    soc_kwargs.update(l2_size=1024)
    soc_kwargs.update(sys_clk_freq=50e6)
    soc_kwargs.update(with_led_chaser=False)
    soc_kwargs.update(integrated_rom_size=0x10000)

    soc = SoCDemo(board.soc_cls, **soc_kwargs)

    soc.add_switches()
    soc.add_leds()

    board_name = "terasic_de2_115"
    build_dir = os.path.join("build", board_name)
    builder   = Builder(soc,
        output_dir   = os.path.join("build", board_name),
        bios_console = "lite",
        csr_json     = os.path.join(build_dir, "csr.json"),
        csr_csv      = os.path.join(build_dir, "csr.csv")
    )
    builder.build(run=args.build, build_name=board_name)

    # Load FPGA bitstream ----------------------------------------------------------------------
    if args.load:
        board.load(soc, builder.get_bitstream_filename(mode="sram"))

    # Flash bitstream/images (to SPI Flash) ----------------------------------------------------
    if args.flash:
        board.flash(soc, builder.get_bitstream_filename(mode="flash"))

    # Generate SoC documentation ---------------------------------------------------------------
    if args.doc:
        soc.generate_doc(board_name)

if __name__ == "__main__":
    main()
