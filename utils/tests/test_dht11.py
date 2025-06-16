from sensors.dht11 import DHT11Sensor
import time

def run_dht11_test():
    sensor = DHT11Sensor()
    print("Starting DHT11 test...")
    
    try:        
        for _ in range(5):
            temperature, humidity = sensor.read()
            if humidity is not None and temperature is not None:
                print(f"Temperature: {temperature} °C | Humidity: {humidity} %")
            else:
                print("Sensor returned invalid data. Retrying...")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Test interrupted by user.")

if __name__ == "__main__":
    run_dht11_test()