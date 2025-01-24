# Quiz-Show Buzzer System

This project is a simple quiz-show buzzer system that uses a Raspberry Pi (RPi) connected to physical buzzers and communicates with a computer to run the main program. The Raspberry Pi detects when a buzzer is pressed, and the computer displays the results.

## System Overview

- **Buzzers**: Physical switches connected to the Raspberry Pi's GPIO pins.
  - Buzzer 1: GPIO pin 17
  - Buzzer 2: GPIO pin 22
  - Buzzer 3: GPIO pin 27
- **Communication**: The Raspberry Pi and the computer are connected via Ethernet.
- **IP Configuration**:
  - Raspberry Pi: `101.101.1.2`
  - Computer: `101.101.1.1`

## How the System Works

1. The Raspberry Pi runs a TCP server using the socket library, It listens for the request 'GET\_STATES' and returns the HIGH or LOW states for GPIO pins 17, 22 and 27.
2. The client on the computer sends request to the server and run the game logic for the buzzer system, presented to the user with a GUI made using pygame.

---

## Prerequisites

- A Raspberry Pi with the Raspberry Pi OS installed.
- A computer to run the GUI program.
- Ethernet cable for direct connection between the Raspberry Pi and the computer.
- Python 3 installed on both the Raspberry Pi and the computer.

---

## Hardware Setup

1. Connect each buzzer (switch) between 3.3V and the designated GPIO pins on the Raspberry Pi:
   - Buzzer 1: GPIO 17
   - Buzzer 2: GPIO 22
   - Buzzer 3: GPIO 27
2. Connect the Raspberry Pi and the computer using an Ethernet cable.
3. **Optional**: Use the included STL file to 3D-print a buzzer housing designed for the KNX-1 switch. Ensure the buzzer is connected in parallel with a 10 kΩ resistor.

---

## Software Setup

### 1. Configuring Static IP Addresses

#### On the Computer:

1. Assign the IP address to the network interface connected to the Raspberry Pi:

   ```bash
   ip addr add 101.101.1.1/24 dev <your-interface>
   ```

   Replace `<your-interface>` with the name of your network interface (e.g., `enp3s0`, `eth0`, `wlan0`). You can find the interface name using:

   ```bash
   ip link show
   ```

2. Add a route for the Raspberry Pi network:

   ```bash
   ip route add 101.101.1.0/24 dev <your-interface>
   ```

#### On the Raspberry Pi:

1. Open the DHCP configuration file:

   ```bash
   sudo nano /etc/dhcpcd.conf
   ```

2. Add the following lines at the end of the file:

   ```
   interface eth0
   static ip_address=101.101.1.2/24
   static routers=101.101.1.1
   static domain_name_servers=8.8.8.8
   ```

   Save the file and exit (Ctrl+O, Enter, Ctrl+X).

3. Restart the DHCP service:

   ```bash
   sudo systemctl restart dhcpcd
   ```

---

### 2. Running the Program

#### On the Raspberry Pi:

1. Navigate to the project directory containing `main.py`.
2. Start the server by running:
   ```bash
   python3 main.py server
   ```

#### On the Computer:

1. Navigate to the project directory containing `main.py`.
2. (Optional) Create a Python virtual environment to isolate dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install any required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the GUI by running:
   ```bash
   python3 main.py gui --physical_buzzers
   ```
   or alternatively if you are running the program without running the server.
   ```bash
   python3 main.py gui
   ```

#### After Starting the GUI:

1. You will be prompted to specify the number of players.
2. For each player, you will enter:
   - **Name**: The name of the player.
   - **Handicap**: The time delay (in seconds) before their buzzer is activated leave empty if no handicap or 0 if you don't want answers before the question is finished.
   - **Sound Effect**: The sound to play when the player buzzes in.
   - **GPIO Pin**: The GPIO pin connected to the player's buzzer.

---

## Adding Buzzer Sounds

The program supports custom buzzer sounds for players. To add your own sounds:

1. Place the sound files in the `buzzer_sounds` folder located in the project directory.
2. The program supports any file format compatible with `pygame.mixer`, such as `.mp3`, `.wav`, etc.
3. When setting up players in the GUI, you can select these custom sounds for each player's buzzer.

---

## Using the Program

1. **Host Reads Question**: The host reads the question to the participants.
2. **Start Timer**: Press the "Start Timer" button (hotkey: `t`) to begin tracking the response time.
3. **Player Buzzes**: When a player buzzes in:
   - The sound effect chosen for that player will play.
   - The player's name will be displayed on the screen as the first to buzz.
4. **Correct Answer**:
   - Press the "Reset Buzzers" button (hotkey: `r`) to allow all players to buzz in for the next question.
5. **Incorrect Answer**:
   - Press the "Wrong" button (hotkey: `y`) to disable the incorrect player's buzzer for the current question.
   - The next player to buzz in gets the chance to answer.
6. **Handicap Handling**: If a player has a handicap (e.g., 5 seconds), their buzzer will remain inactive until the timer reaches their handicap time.
