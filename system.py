import platform
import os

system = platform.system()
print(system)
if system == "Windows":
  os.system('curl -fsSL -o SpotAFan.py https://raw.githubusercontent.com/benji77430/SpotAFan/refs/heads/main/SpotAFan.py && python SpotAFan.py ')
elif system == "Darwin":
    print("MacOS detected")

elif system == "Linux":
    print("LINUX detected")
    os.system('curl -fsSL -o SpotAFan.py https://raw.githubusercontent.com/benji77430/SpotAFan/linux/SpotAFan.py && python SpotAFan.py')
  
else:
    raise OSError(f"Unsupported operating system: {system}")
