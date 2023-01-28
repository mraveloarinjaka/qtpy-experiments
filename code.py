import asyncio
import time

# # check wifi connectivity
# import test_wifi

# # check i2c bus
# import check_i2c

import check_temp
import check_leds

CHECK_MEASUREMENTS_INTERVAL = 15


async def main():
    await asyncio.gather(
        check_temp.check_measurements_loop(CHECK_MEASUREMENTS_INTERVAL),
        check_leds.run_leds_loop(),
    )


asyncio.run(main())

