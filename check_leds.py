import asyncio
import board
from rainbowio import colorwheel

import adafruit_is31fl3741
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
from adafruit_is31fl3741.is31fl3741_PixelBuf import IS31FL3741_PixelBuf
import adafruit_framebuf
from adafruit_framebuf import FrameBuffer
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_pixelbuf import PixelBuf
from adafruit_led_animation.color import (
    RED,
    PURPLE,
    WHITE,
    AMBER,
    JADE,
    TEAL,
    PINK,
    MAGENTA,
    ORANGE,
)

# WIDTH = 13
# HEIGHT = 9
# LEDS_MAP = tuple(
#     (
#         address
#         for x in range(WIDTH)
#         for y in range(HEIGHT)
#         for address in Adafruit_RGBMatrixQT.pixel_addrs(x, y)
#     )
# )


WIDTH = 13
HEIGHT = 9
LEDS_MAP = tuple(
    (
        address
        for x in range(WIDTH)
        for y in range(HEIGHT)
        for address in Adafruit_RGBMatrixQT.pixel_addrs(x, y)
    )
)


class RGBMatrixQTToPixelBufAdapter(Adafruit_RGBMatrixQT):
    """Additional properties so that Adafruit_RGBMatrixQT can be used with IS31FL3741_PixelBuf."""

    def __init__(
        self,
        i2c,
        allocate,
    ):
        super().__init__(i2c, allocate=allocate)

    def write(self, mapping, buffer):
        temp_buffer = FrameBuffer(
            buffer,
            WIDTH,
            HEIGHT,
            adafruit_framebuf.RGB888,
        )
        self.image(temp_buffer)
        self.show()


i2c = board.STEMMA_I2C()
is31 = RGBMatrixQTToPixelBufAdapter(i2c, allocate=adafruit_is31fl3741.PREFER_BUFFER)
# is31.set_led_scaling(0xFF)
is31.set_led_scaling(1)
is31.global_current = 0xFF
is31.enable = True
pixels = IS31FL3741_PixelBuf(is31, LEDS_MAP, init=False, auto_write=False)

comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
# blink = Blink(pixels, speed=0.5, color=JADE)
colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, ORANGE])
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = Pulse(pixels, speed=0.1, period=3, color=AMBER)
sparkle = Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = Solid(pixels, color=JADE)
rainbow = Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=JADE)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
custom_color_chase = CustomColorChase(
    pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)
animations = AnimationSequence(
    comet,
    # blink,
    rainbow_sparkle,
    chase,
    pulse,
    sparkle,
    rainbow,
    solid,
    rainbow_comet,
    sparkle_pulse,
    rainbow_chase,
    custom_color_chase,
    advance_interval=5,
    auto_clear=True,
)


async def run_leds_loop():
    while True:
        animations.animate()
        await asyncio.sleep(0)
