## Getting Started

### Windows
> The driver stuff seemed dangerous, so I didn't investigate this at all. But I think the value of RTLSharp is compelling, so may come back to this at a later date.
### Windows + WSL
> All of this is done by the `setup.bat` file
1. Update wsl to version 2
   ```powershell
   wsl --update
   ```
2. Create Ubuntu Virtual Machine
   ```powershell
   wsl --install Ubuntu
   ```
3. Set Ubuntu VM to use WSL 2 (may take a few moments)
   ```powershell
   wsl --set-version Ubuntu 2
   ```

4. Enter the new virtual machine (if it is not already opened)
   ```powershell
   wsl --distribution ubuntu
   ```
   > It will prompt you to create a new user and set a password

5. Install usbipd-win for usb passthrough to the VM
   ```powershell
   winget install --interactive --exact dorssel.usbipd-win
   ```
6. Identify the Radio from the usbipd interface
   ```powershell
   (base) C:\git>usbipd list
    Connected:
    BUSID  VID:PID    DEVICE                                                        STATE
    1-14   0bda:2838  Bulk-In, Interface                                            Not shared
    2-1    0a12:0001  Generic Bluetooth Radio                                       Not shared
    2-2    046d:c54d  USB Input Device                                              Not shared
   ```
   > Mine is called `Bulk-In, Interface` and has the BUSID=`1-14`
7. Bind the device (Registers a single USB device for sharing, so it can be attached to other machines)
   ```powershell
   usbipd bind --busid 1-14
   ```
   > The value for --busid (`1-14`) was identified in the previous step
8. Attach the device to the WSL VM
   ```powershell
   usbipd attach -b 1-14 --wsl
   ```
9. Now, back in the Ubuntu terminal, you need to install the software required to recieve USB over IP data
    ```bash
    sudo apt update
    sudo apt install linux-tools-5.4.0-77-generic hwdata
    sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/5.4.0-77-generic/usbip 20
    ```
10. Install the rtlsdr software required to read the signal from the usb antenna
    ```bash
    sudo apt update
    sudo apt install rtl-sdr sox
    ```
### Linux
```bash
sudo apt update
sudo apt install linux-tools-5.4.0-77-generic hwdata rtl-sdr sox
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/5.4.0-77-generic/usbip 20
```