#!/usr/bin/python3

# Simple test script for ADXL345 accelerometer
import sys
import time

print("Testing ADXL345 accelerometer...")
print("=" * 40)

try:
    print("1. Importing board library...")
    import board
    print("   ✓ board imported successfully")
    
    print("2. Importing adafruit_adxl34x library...")
    import adafruit_adxl34x
    print("   ✓ adafruit_adxl34x imported successfully")
    
    print("3. Setting up I2C...")
    i2c = board.I2C()
    print("   ✓ I2C setup successful")
    
    print("4. Scanning I2C bus...")
    # Check what devices are on the I2C bus
    print("   Scanning for I2C devices...")
    devices_found = []
    for addr in range(0x08, 0x78):  # Standard I2C address range
        try:
            i2c.try_lock()
            i2c.writeto(addr, b'')
            devices_found.append(hex(addr))
        except:
            pass
        finally:
            i2c.unlock()
    
    print(f"   Found I2C devices at: {devices_found}")
    
    print("5. Connecting to ADXL345...")
    # Try default address first
    try:
        tilt = adafruit_adxl34x.ADXL345(i2c)
        print("   ✓ ADXL345 connected successfully at default address")
    except:
        # Try specific address 0x53
        try:
            tilt = adafruit_adxl34x.ADXL345(i2c, address=0x53)
            print("   ✓ ADXL345 connected successfully at address 0x53")
        except:
            # Try alternative address 0x1D
            tilt = adafruit_adxl34x.ADXL345(i2c, address=0x1D)
            print("   ✓ ADXL345 connected successfully at address 0x1D")
    
    print("6. Reading accelerometer data...")
    for i in range(5):
        accel = tilt.acceleration
        print(f"   Reading {i+1}: X={accel[0]:.2f}, Y={accel[1]:.2f}, Z={accel[2]:.2f} m/s²")
        time.sleep(0.5)
    
    print("\n✓ ADXL345 test completed successfully!")
    print("The accelerometer is working properly.")
    
except ImportError as e:
    print(f"   ✗ Import error: {e}")
    print("   Missing Python libraries. Install with:")
    print("   pip install adafruit-blinka")
    print("   pip install adafruit-circuitpython-adxl34x")
    print("   ")
    print("   Note: You may also need to enable I2C:")
    print("   sudo raspi-config -> Interface Options -> I2C -> Enable")
    sys.exit(1)

except ValueError as e:
    print(f"   ✗ I2C/Hardware error: {e}")
    print("   Possible causes:")
    print("   - ADXL345 not connected")
    print("   - Wrong I2C address")
    print("   - I2C not enabled")
    print("   - Wiring issue")
    sys.exit(1)

except Exception as e:
    print(f"   ✗ Unexpected error: {e}")
    print(f"   Error type: {type(e).__name__}")
    sys.exit(1)