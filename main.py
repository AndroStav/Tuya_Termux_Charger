import tinytuya
import subprocess
import json
import asyncio

async def main():

    d = tinytuya.Device('DEVICE_ID_HERE', 'IP_ADDRESS_HERE', 'LOCAL_KEY_HERE', version=3.3)
    
    while True:
        try:            
            battery = int(json.loads(subprocess.run(['termux-battery-status'], capture_output=True, text=True).stdout)['percentage'])
            if battery < 50:
                while True:
                    battery = int(json.loads(subprocess.run(['termux-battery-status'], capture_output=True, text=True).stdout)['percentage'])
                    if battery >= 90:
                        break
                    else:
                        data = d.status()
                        if 'Error' in data:
                            print("Дата має проблеми")
                        else:
                            s = data['dps']['1']

                            if s == False:
                                print("Вмикаю розетку")
                                d.turn_on()
                    
                    await asyncio.sleep(1800)

                data = d.status()
                if 'Error' in data:
                    print("Дата має проблеми")
                else:
                    s = data['dps']['1']

                    if s == True:
                        print("Вимикаю розетку")
                        d.turn_off()

            await asyncio.sleep(1800)

        except Exception as e:
            print(e)
            await asyncio.sleep(1800)

        except asyncio.CancelledError as e:
            print(e)
            await asyncio.sleep(1800)

if __name__ == "__main__":
    asyncio.run(main())
