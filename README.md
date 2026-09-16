# Development of a Multimodal 3D Object Recognition and Visualization System for Traffic Environments Using Camera-LiDAR Fusion

## Overview
This project develops a multimodal 3D object recognition and visualization system for traffic environments using camera and LiDAR data. The system integrates the MEFormer model within the MMDetection3D framework to perform 3D object detection on the nuScenes dataset and provides visualization tools for analyzing detection results from both 2D camera images and 3D LiDAR point clouds.

## Objectives
- Develop a pipeline for multimodal 3D object detection using camera and LiDAR data.
- Integrate and evaluate the MEFormer model within the MMDetection3D framework.
- Process and evaluate detection results using the nuScenes dataset and standard 3D detection metrics.
- Develop a visualization application for inspecting camera images, LiDAR point clouds, and 3D bounding boxes.

## System Pipeline
<img src="docs/pipeline.png" alt="System Pipeline" width="400">

## Methodology

This project implements a multimodal 3D object detection and visualization pipeline based on the MEFormer model within the MMDetection3D framework.

### Sensor Fusion

The system combines camera images and LiDAR point clouds to exploit their complementary information. Camera data provides rich semantic and visual information, while LiDAR provides direct spatial and depth information for 3D scene understanding.

### Model Integration

MEFormer is integrated into the MMDetection3D framework to process multimodal camera and LiDAR data for 3D object detection. The workflow includes data preparation, format standardization, model inference, result processing, and evaluation.

### Data Processing and Inference

The input data is preprocessed and synchronized using the calibration and metadata provided by the nuScenes dataset. Camera images, LiDAR point clouds, and related annotations are converted into the formats required by the detection pipeline before inference.

### Result Visualization

A Python-based visualization application was developed to inspect the detection results from both camera and LiDAR views. The application supports 2D image visualization, 3D point-cloud visualization, bounding-box display, result analysis, and export of processed outputs.

## Dataset

The project uses the **nuScenes dataset** as the benchmark for multimodal 3D object detection. For the experimental evaluation, the **nuScenes mini** dataset was used as a compact subset suitable for research under limited computational resources.

| Item | Details |
|---|---|
| Dataset | nuScenes mini |
| Scenes | 10 |
| Camera | 6 views |
| LiDAR | 1 sensor |
| Radar | 5 sensors |
| Task | Multimodal 3D object detection |
| Model | MEFormer |
| Framework | MMDetection3D |

For the experimental evaluation, four scenes were selected:

- Scene 0103
- Scene 0916
- Scene 0796
- Scene 0553

The project focuses on **camera and LiDAR data** for multimodal 3D object detection, while the additional sensor information available in nuScenes provides broader dataset context.

## Implementation

The system is implemented in Python and built around the MMDetection3D framework. The workflow covers dataset preparation, sensor-data preprocessing, MEFormer inference, result standardization, evaluation, and visualization.

The visualization application is developed with PyQt5 and Open3D, providing synchronized views of camera images and 3D LiDAR point clouds. OpenCV and NumPy are used for image processing and numerical operations.

## Results

## Visualization

## Limitations

## Future Development

## Project Structure

## Requirements

The project was developed and tested with the following environment:

| Component | Version / Configuration |
|---|---|
| Python | 3.8 |
| PyQt5 | 5.15.0 |
| Open3D | 0.17.0 |
| OpenCV | 4.7.0 |
| NumPy | 1.23.0 |
| Framework | MMDetection3D |

## Usage

### 1. Prepare the environment

Install the required Python packages and configure the MMDetection3D environment according to the project setup.

### 2. Prepare the dataset

Place the required nuScenes data and project inputs in the appropriate directories.

### 3. Run the detection pipeline

Run the corresponding Python script from the `src` directory to preprocess the data, perform MEFormer inference, and generate the prediction outputs.

### 4. Run the visualization application

Launch the visualization module to inspect camera images, LiDAR point clouds, 3D bounding boxes, and evaluation results.

## Thesis
