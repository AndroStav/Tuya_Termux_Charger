import tinytuya
import subprocess
import json
import asyncio

DELAY = 1200

async def main():

    d = tinytuya.Device('DEVICE_ID_HERE', 'IP_ADDRESS_HERE', 'LOCAL_KEY_HERE', version=3.3)
    
    while True:
        try:            
            battery = int(json.loads(subprocess.run(['termux-battery-status'], capture_output=True, text=True).stdout)['percentage'])
            if battery < 50:
                while battery < 90:
                    data = d.status()
                    if 'Error' in data:
                        print("Дата має проблеми")
                    else:
                        s = data['dps']['1']

                        if s == False:
                            print(f"Вмикаю розетку: {battery}%")
                            d.turn_on()
                    
                    await asyncio.sleep(DELAY)
                    battery = int(json.loads(subprocess.run(['termux-battery-status'], capture_output=True, text=True).stdout)['percentage'])

                data = d.status()
                if 'Error' in data:
                    print("Дата має проблеми")
                else:
                    s = data['dps']['1']

                    if s == True:
                        print(f"Вимикаю розетку: {battery}%")
                        d.turn_off()

            await asyncio.sleep(DELAY)

        except Exception as e:
            print(e)
            await asyncio.sleep(DELAY)

        except asyncio.CancelledError as e:
            print(e)
            await asyncio.sleep(DELAY)

if __name__ == "__main__":
    asyncio.run(main())
