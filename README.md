# Overflow Open House 2024: RC Car Project

> WebSocket-Controlled RTSP Video Streaming and Motor Control

This project provides a framework to control a robotic vehicle with video streaming capabilities using WebSocket communication. It includes features such as RTSP video streaming, motor control, and authentication for secure access.

## Features

- RTSP Video Streaming: Streams video using GStreamer and OpenCV.
- Motor Control: Controls motors through GPIO pins, enabling remote navigation.
- WebSocket Communication: Facilitates real-time control and data exchange.
- Secure Access: Password-protected access to ensure authorized usage.

## Setup and Installation

### Prerequisites

1. **Python**: Ensure Python 3.x is installed.
2. **System Dependencies**: Install the required libraries and dependencies using the following command:

```bash
sudo apt install python3-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0 libcairo2-dev libgirepository1.0-dev libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libglib2.0-dev libgstrtspserver-1.0-dev gstreamer1.0-rtsp
```

## Usage

1. Configure Environment Variables:

   - Create a .env file in the root directory.
   - Use config.sample.env as a template.

2. Run the Project:
   - Start the motor control script:

```bash
python3 car.py
```

3. Start the main WebSocket and RTSP server:

```bash
python3 main.py
```

4. (Optional) Access Remotely:
   - Use tools like Tailscale for remote access.
   - Cloudflared support is planned but not yet implemented.

## Development

#### Directory Structure

`car.py` : Handles motor control.
`main.py` : Manages WebSocket communication and video streaming.
`stream.py`: Implements RTSP streaming using GStreamer and OpenCV.

#### Testing

Our car is powered by a Raspberry Pi 5. To test the project, you can run the scripts on the Raspberry Pi or any other compatible device.
All the scripts were ran outside a virtual environment.
Remote Access: Configure Tailscale for secure, remote connectivity.

## Notes

- Make sure GPIO permissions are set appropriately for motor control.
- Use caution when testing motor controls to avoid damage to hardware or surroundings.

Have Fun! 🚗💨

## Contributors

- Daksh Thapar (Controling the Car)
- Richard Tan (Building the Car)
- Tan Xuan Han (Building the [Driving App](https://github.com/XuanHanTan-School/overflow-car-app))
