# Smart Meta Glasses 👓

An AI-powered wearable assistive device that acts as an "artificial vision system" for visually impaired individuals. The system provides real-time obstacle detection, distance estimation, and audio feedback for safe navigation.

## Features

- **Real-time Object Detection** - Identifies obstacles using YOLOv8
- **Distance Estimation** - Calculates proximity using monocular vision
- **Smart Audio Alerts** - Priority-based voice feedback system
- **Critical Warnings** - Immediate alerts for nearby obstacles
- **Natural Language** - Clear, intuitive voice instructions

## Technology Stack

- **Object Detection**: YOLOv8 (Ultralytics)
- **Computer Vision**: OpenCV
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Audio Processing**: Pygame
- **Core Framework**: Python 3.8+

## Project Structure

The project is organized into modular components:

- **audio/**: Audio feedback system (alert management, TTS, audio playback)
- **ml/inference/**: Machine learning modules (object detection, distance estimation)
- **ml/training/**: Model training scripts
- **utils/**: Utility functions and helpers
- **demo_object_detection.py**: Main demonstration script
- **main_integrated.py**: Integrated system controller

## Installation

1. Clone the repository
2. Install Python dependencies from requirements_ml.txt
3. Run the demonstration script

## Usage

The system automatically activates camera feed, detects objects in real-time, calculates distances, and provides voice alerts. Example alerts include "Person detected, 3 meters" and "Warning! Chair very close!"

## Alert Priority System

- **Critical** (🚨): Objects within 1.0 meter - Immediate warnings
- **High** (⚠️): Objects within 1.0-2.0 meters - Proximity alerts
- **Medium** (ℹ️): Objects beyond 2.0 meters - Informational alerts

## Supported Objects

The system detects 80+ object categories including people, vehicles, furniture, electronic devices, and common obstacles.

## System Architecture

Camera Input → Object Detection → Distance Estimation → Alert Management → Audio Output

## Demonstration

A real-time demonstration is available that shows the system detecting objects and providing audio feedback through the computer's camera and speakers.

## Contributing

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

## License

This project is licensed under the MIT License.

## Acknowledgments

- YOLOv8 by Ultralytics for object detection
- Google Text-to-Speech for voice synthesis
- OpenCV for computer vision capabilities
- IIT Patna Incubation Center for support and resources
