# Traffic-Signal-Violence
This repository contains a project for detecting traffic signal violations using the YOLOv8m model. The project is implemented using Python and utilizes the following libraries: OpenCV, ultralytics, os, and numpy. The model is capable of identifying and flagging instances of vehicles running red lights in the provided video footage. <br/>
<br/>

## Introduction
Traffic signal violations, such as running a red light, are a significant cause of road accidents. This project aims to detect such violations using a pre-trained YOLOv8m model. The model processes video footage to identify vehicles that do not adhere to traffic signals, providing a practical tool for improving road safety. <br/>
<br/>

## Requirements
To run this project, you will need the following Python packages:
* opencv-python
* ultralytics
* numpy <br/>
These dependencies are listed in the requirements.txt file. <br/>
<br/>

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Shah114/traffic-signal-violence.git
   cd traffic-signal-violence
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
<br/>

## Usage
To use this project, follow the steps below: <br/>
1. Place your input video file in the project directory.
2. Run the detection script:
   ```bash
   python main.py
   ```
Replace main.py with the actual script name if different.
3. The output will be a video with detected violations highlighted. <br/>
<br/>

##

