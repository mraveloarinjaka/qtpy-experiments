import board

# i2c = board.I2C()  # uses board.SCL and board.SDA

# To create I2C bus on specific pins
# import busio
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

i2c = (
    board.STEMMA_I2C()
)  # For using the built-in STEMMA QT connector on a microcontroller

while not i2c.try_lock():
    pass

try:
    print(
        "I2C addresses found:",
        [hex(device_address) for device_address in i2c.scan()],
    )
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()
