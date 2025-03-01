import tinytuya, subprocess, json, asyncio, logging, configparser

logging.basicConfig(level=logging.INFO, filename="main.log", format="%(asctime)s %(levelname)s [%(funcName)s]: %(message)s")

def load_config(filename):
    config = configparser.ConfigParser()
    try:
        config.read(filename)
        logging.info("Конфігурація завантажена")
        return config
    except Exception as e:
        logging.error(e)
        return None

async def main():
    config = load_config("config.ini")
    if config is None:
        return 1
    
    DELAY = int(config["General"]["DELAY"])
    device_id = config["General"]["device_id"]
    ip_address = config["General"]["ip_address"]
    local_key = config["General"]["local_key"]

    d = tinytuya.Device(device_id, ip_address, local_key, version=3.3)
    
    print("Додаток запущено")
    logging.info("Додаток запущено")
    
    while True:
        try:            
            logging.debug("Отримую дані про заряд")
            battery = int(json.loads(subprocess.run(['termux-battery-status'], capture_output=True, text=True).stdout)['percentage'])
            logging.debug(f"battery: {battery}%")
            if battery < 50:
                while battery < 90:
                    logging.debug("Отримую дані від розетки")
                    data = d.status()
                    if 'Error' in data:
                        print("Дата має проблеми")
                        logging.error("Дата має проблеми")
                    else:
                        s = data['dps']['1']

                        if s == False:
                            print(f"Вмикаю розетку: {battery}%")
                            logging.info(f"Вмикаю розетку: {battery}%")
                            d.turn_on()
                    
                    await asyncio.sleep(DELAY)
                    logging.debug("Отримую дані про заряд")
                    battery = int(json.loads(subprocess.run(['termux-battery-status'], capture_output=True, text=True).stdout)['percentage'])
                    logging.debug(f"battery: {battery}%")

                logging.debug("Отримую дані від розетки")
                data = d.status()
                if 'Error' in data:
                    print("Дата має проблеми")
                    logging.error("Дата має проблеми")
                else:
                    s = data['dps']['1']

                    if s == True:
                        print(f"Вимикаю розетку: {battery}%")
                        logging.info(f"Вимикаю розетку: {battery}%")
                        d.turn_off()

            await asyncio.sleep(DELAY)

        except Exception as e:
            print(e)
            logging.error(e)
            await asyncio.sleep(DELAY)

        except asyncio.CancelledError as e:
            print(e)
            logging.error(e)
            await asyncio.sleep(DELAY)

if __name__ == "__main__":
    asyncio.run(main())
