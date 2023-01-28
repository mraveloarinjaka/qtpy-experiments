import asyncio
import board
import adafruit_shtc3

# i2c = board.I2C()
i2c = board.STEMMA_I2C()
sht = adafruit_shtc3.SHTC3(i2c)

async def check_measurements_loop(interval):
    while True:
        temperature, relative_humidity = sht.measurements
        print("Temperature: %0.1f C" % temperature)
        print("Humidity: %0.1f %%fH" % relative_humidity)
        await asyncio.sleep(interval)

