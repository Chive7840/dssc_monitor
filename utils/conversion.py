def adc_to_voltage(raw, vref=2.5):
    return (raw / 0x7FFFFF) * vref