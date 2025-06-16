from sensors.ads1256 import ADS1256
import time

def run_ads1256_test():
    adc = ADS1256(vref=2.5, channel=0)
    print("Starting ADS1256 voltage test...")
    
    for _ in range(5):
        voltage = adc.read_voltage()
        print(f"DSSC Voltage: {voltage:.4f} V")
        time.sleep(1)
        
if __name__ == "__main__":
    run_ads1256_test()