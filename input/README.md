# Input Data

This project uses the nuScenes dataset for multimodal 3D object detection.

The original nuScenes dataset is not included in this repository due to its size.

The required dataset structure follows the nuScenes `v1.0-test` format, including:

- `maps/`
- `samples/`
- `sweeps/`
- `v1.0-test/`

The project processes camera images and LiDAR point clouds from the dataset. Additional sensor data available in nuScenes is not directly used in the Camera-LiDAR fusion pipeline.

Please obtain the dataset from the official nuScenes source and configure the project paths before running the analysis scripts.
