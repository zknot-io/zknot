"""
SSD1306 OLED driver for MicroPython.
Supports 128x64 and 128x32 displays over I2C.

This is a minimal driver focused on the text display needs of ZKnot Witness.
For the 0.96" and 0.91" OLED modules in your parts order.
"""

import time
import framebuf


# SSD1306 command constants
SET_CONTRAST        = 0x81
SET_ENTIRE_ON       = 0xA4
SET_NORM_INV        = 0xA6
SET_DISP            = 0xAE
SET_MEM_ADDR        = 0x20
SET_COL_ADDR        = 0x21
SET_PAGE_ADDR       = 0x22
SET_DISP_START_LINE = 0x40
SET_SEG_REMAP       = 0xA0
SET_MUX_RATIO       = 0xA8
SET_COM_OUT_DIR     = 0xC0
SET_DISP_OFFSET     = 0xD3
SET_COM_PIN_CFG     = 0xDA
SET_DISP_CLK_DIV    = 0xD5
SET_PRECHARGE       = 0xD9
SET_VCOM_DESEL      = 0xDB
SET_CHARGE_PUMP     = 0x8D


class SSD1306:
    def __init__(self, width, height, external_vcc=False):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer(
            self.buffer, self.width, self.height, framebuf.MONO_VLSB
        )
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,           # display off
            SET_MEM_ADDR, 0x00,        # horizontal addressing
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,      # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,    # scan from COM[N-1] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if (self.width == 128 and self.height == 32) else 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xFF,
            SET_ENTIRE_ON,             # output follows RAM
            SET_NORM_INV,              # not inverted
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,           # display on
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def hline(self, x, y, w, col):
        self.framebuf.hline(x, y, w, col)

    def vline(self, x, y, h, col):
        self.framebuf.vline(x, y, h, col)

    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)

    def rect(self, x, y, w, h, col):
        self.framebuf.rect(x, y, w, h, col)

    def fill_rect(self, x, y, w, h, col):
        self.framebuf.fill_rect(x, y, w, h, col)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def show(self):
        x0 = 0
        x1 = self.width - 1
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        # Prepend the 0x40 data byte
        full = bytearray(1 + len(buf))
        full[0] = 0x40
        full[1:] = buf
        self.i2c.writeto(self.addr, full)
