# Project Title

Short Overview

## Overview
## Objectives

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

## Results

## Visualization

## Limitations

## Future Development

## Project Structure

## Requirements

## Usage

## Thesis
