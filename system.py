import platform
import os

system = platform.system()
print(system)
if system == "Windows":
  os.system('curl -fsSl https://raw.githubusercontent.com/benji77430/SpotAFan/main/SpotAFan.py | python')
elif system == "Darwin":
    print("MacOS detected")

elif system == "Linux":
    print("LINUX detected")
    os.system('curl -fsSL https://raw.githubusercontent.com/benji77430/SpotAFan/linux/SpotAFan.py | python')
  
else:
    raise OSError(f"Unsupported operating system: {system}")
