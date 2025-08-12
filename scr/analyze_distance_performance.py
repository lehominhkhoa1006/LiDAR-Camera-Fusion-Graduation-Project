import json
import numpy as np
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import Box
from pyquaternion import Quaternion

def load_predictions(json_file):
    """Load predictions from JSON file"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data['results']

def calculate_distance(prediction, nusc, sample_token):
    """Calculate distance from ego vehicle to predicted object"""
    # Get sample and camera data
    sample = nusc.get('sample', sample_token)
    camera_data = nusc.get('sample_data', sample['data']['CAM_FRONT'])
    calib = nusc.get('calibrated_sensor', camera_data['calibrated_sensor_token'])
    ego_pose = nusc.get('ego_pose', camera_data['ego_pose_token'])
    
    # Create box object
    box = Box(center=prediction['translation'],
             size=prediction['size'],
             orientation=Quaternion(prediction['rotation']))
    
    # Transform box to camera coordinate system
    box.translate(-np.array(ego_pose['translation']))
    box.rotate(Quaternion(ego_pose['rotation']).inverse)
    box.translate(-np.array(calib['translation']))
    box.rotate(Quaternion(calib['rotation']).inverse)
    
    # Calculate distance from camera to object center
    return np.linalg.norm(box.center)

def get_distance_group(distance):
    """Group distance into categories"""
    if distance <= 10:
        return '0-10m'
    elif distance <= 20:
        return '10-20m'
    elif distance <= 30:
        return '20-30m'
    elif distance <= 40:
        return '30-40m'
    elif distance <= 50:
        return '40-50m'
    else:
        return '>50m'

def analyze_predictions(predictions, nusc):
    """Analyze predictions and create descriptive statistics"""
    # Create lists to store data
    all_distances = []
    all_scores = []
    all_names = []
    all_groups = []
    
    # Process each sample
    for sample_token, sample_preds in tqdm(predictions.items(), desc="Processing samples"):
        for pred in sample_preds:
            distance = calculate_distance(pred, nusc, sample_token)
            distance_group = get_distance_group(distance)
            
            # Store prediction info
            all_distances.append(distance)
            all_scores.append(pred['detection_score'])
            all_names.append(pred['detection_name'])
            all_groups.append(distance_group)
    
    # Create DataFrame
    df = pd.DataFrame({
        'distance': all_distances,
        'score': all_scores,
        'name': all_names,
        'distance_group': all_groups
    })
    
    # Print debug information
    print("\nDebug Information:")
    print("Total number of predictions:", len(df))
    print("\nDistance groups distribution:")
    print(df['distance_group'].value_counts().sort_index())
    print("\nDistance statistics:")
    print(df['distance'].describe())
    
    return df

def calculate_distance_statistics(df):
    """Calculate statistics for each distance group"""
    # Define the order of distance groups
    distance_order = ['0-10m', '10-20m', '20-30m', '30-40m', '40-50m', '>50m']
    
    # Initialize statistics dictionary
    stats = {
        'Number of Predictions': [],
        'Average Score': [],
        'Median Score': [],
        'Score Std Dev': [],
        'Score > 0.3 (%)': [],
        'Score > 0.7 (%)': []
    }
    
    # Calculate statistics for each distance group
    for group in distance_order:
        group_data = df[df['distance_group'] == group]
        
        if len(group_data) > 0:
            stats['Number of Predictions'].append(len(group_data))
            stats['Average Score'].append(f"{group_data['score'].mean():.3f}")
            stats['Median Score'].append(f"{group_data['score'].median():.3f}")
            stats['Score Std Dev'].append(f"{group_data['score'].std():.3f}")
            stats['Score > 0.3 (%)'].append(f"{(group_data['score'] > 0.3).mean() * 100:.1f}")
            stats['Score > 0.7 (%)'].append(f"{(group_data['score'] > 0.7).mean() * 100:.1f}")
        else:
            # If no data for this group, append zeros or appropriate default values
            stats['Number of Predictions'].append(0)
            stats['Average Score'].append("0.000")
            stats['Median Score'].append("0.000")
            stats['Score Std Dev'].append("0.000")
            stats['Score > 0.3 (%)'].append("0.0")
            stats['Score > 0.7 (%)'].append("0.0")
    
    # Create DataFrame with distance groups as index
    stats_df = pd.DataFrame(stats, index=distance_order)
    
    return stats_df

def plot_class_distribution(df):
    """Plot distribution of predictions by class as percentages"""
    # Calculate percentages
    class_counts = df['name'].value_counts()
    class_percentages = (class_counts / len(df) * 100).round(2)
    
    # Set style parameters
    plt.style.use('seaborn')
    plt.rcParams.update({
        'font.size': 40,
        'axes.titlesize': 46,
        'axes.labelsize': 42,
        'xtick.labelsize': 40,
        'ytick.labelsize': 40,
        'legend.fontsize': 40
    })
    
    # Create figure with larger size
    plt.figure(figsize=(30, 20))
    bars = plt.bar(class_percentages.index, class_percentages.values, width=0.6)
    
    # Add percentage labels on top of bars with larger font
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom',
                fontsize=40, fontweight='bold')
    
    plt.title('Distribution of Predictions by Class (%)', fontsize=46, pad=50)
    plt.xlabel('Class', fontsize=42)
    plt.ylabel('Percentage of Total Predictions', fontsize=42)
    plt.xticks(rotation=45, ha='right', fontsize=40)
    plt.yticks(fontsize=40)
    
    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.savefig('class_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return class_percentages

def plot_distance_statistics(stats_df):
    """Plot statistics for each distance group"""
    # Convert string values to float for plotting
    plot_df = stats_df.copy()
    for col in plot_df.columns:
        plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')
    
    # Set style parameters
    plt.style.use('seaborn')
    plt.rcParams.update({
        'font.size': 16,
        'axes.titlesize': 20,
        'axes.labelsize': 18,
        'xtick.labelsize': 16,
        'ytick.labelsize': 16,
        'legend.fontsize': 16
    })
    
    # Create combined plot
    fig, axes = plt.subplots(2, 2, figsize=(25, 20))
    fig.suptitle('Prediction Statistics by Distance Group', fontsize=24, y=0.95)
    
    # Plot 1: Number of Predictions
    sns.barplot(data=plot_df.reset_index(), x='index', y='Number of Predictions', ax=axes[0,0])
    axes[0,0].set_title('Number of Predictions', pad=30, fontsize=20)
    axes[0,0].set_xlabel('Distance Group', fontsize=18)
    axes[0,0].set_ylabel('Number of Predictions', fontsize=18)
    axes[0,0].tick_params(axis='x', rotation=45, labelsize=16)
    axes[0,0].tick_params(axis='y', labelsize=16)
    
    # Plot 2: Average and Median Scores
    plot_df[['Average Score', 'Median Score']].plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title('Average and Median Scores', pad=30, fontsize=20)
    axes[0,1].set_xlabel('Distance Group', fontsize=18)
    axes[0,1].set_ylabel('Score', fontsize=18)
    axes[0,1].tick_params(axis='x', rotation=45, labelsize=16)
    axes[0,1].tick_params(axis='y', labelsize=16)
    
    # Plot 3: Score Standard Deviation
    sns.barplot(data=plot_df.reset_index(), x='index', y='Score Std Dev', ax=axes[1,0])
    axes[1,0].set_title('Score Standard Deviation', pad=30, fontsize=20)
    axes[1,0].set_xlabel('Distance Group', fontsize=18)
    axes[1,0].set_ylabel('Standard Deviation', fontsize=18)
    axes[1,0].tick_params(axis='x', rotation=45, labelsize=16)
    axes[1,0].tick_params(axis='y', labelsize=16)
    
    # Plot 4: Score Thresholds
    plot_df[['Score > 0.3 (%)', 'Score > 0.7 (%)']].plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('Percentage of Scores Above Thresholds', pad=30, fontsize=20)
    axes[1,1].set_xlabel('Distance Group', fontsize=18)
    axes[1,1].set_ylabel('Percentage (%)', fontsize=18)
    axes[1,1].tick_params(axis='x', rotation=45, labelsize=16)
    axes[1,1].tick_params(axis='y', labelsize=16)
    
    plt.tight_layout()
    plt.savefig('distance_statistics_combined.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create individual plots with larger size and clearer text
    # 1. Number of Predictions
    plt.figure(figsize=(15, 10))
    sns.barplot(data=plot_df.reset_index(), x='index', y='Number of Predictions')
    plt.title('Number of Predictions by Distance Group', pad=30, fontsize=24)
    plt.xlabel('Distance Group', fontsize=20)
    plt.ylabel('Number of Predictions', fontsize=20)
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig('distance_statistics_count.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Average and Median Scores
    plt.figure(figsize=(15, 10))
    plot_df[['Average Score', 'Median Score']].plot(kind='bar')
    plt.title('Average and Median Scores by Distance Group', pad=30, fontsize=24)
    plt.xlabel('Distance Group', fontsize=20)
    plt.ylabel('Score', fontsize=20)
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(['Average Score', 'Median Score'], fontsize=16)
    plt.tight_layout()
    plt.savefig('distance_statistics_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Score Standard Deviation
    plt.figure(figsize=(15, 10))
    sns.barplot(data=plot_df.reset_index(), x='index', y='Score Std Dev')
    plt.title('Score Standard Deviation by Distance Group', pad=30, fontsize=24)
    plt.xlabel('Distance Group', fontsize=20)
    plt.ylabel('Standard Deviation', fontsize=20)
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig('distance_statistics_std.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Score Thresholds
    plt.figure(figsize=(15, 10))
    plot_df[['Score > 0.3 (%)', 'Score > 0.7 (%)']].plot(kind='bar')
    plt.title('Percentage of Scores Above Thresholds by Distance Group', pad=30, fontsize=24)
    plt.xlabel('Distance Group', fontsize=20)
    plt.ylabel('Percentage (%)', fontsize=20)
    plt.xticks(rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(['Score > 0.3 (%)', 'Score > 0.7 (%)'], fontsize=16)
    plt.tight_layout()
    plt.savefig('distance_statistics_thresholds.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Initialize NuScenes
    nusc = NuScenes(version='v1.0-test', dataroot='.', verbose=True)
    
    # Load predictions
    predictions = load_predictions('results_nusc.json')
    
    # Analyze predictions
    df = analyze_predictions(predictions, nusc)
    
    # Calculate and display distance statistics
    stats_df = calculate_distance_statistics(df)
    print("\nPrediction Statistics by Distance Group:")
    print("=" * 100)
    print(stats_df.to_string())
    
    # Plot distance statistics
    plot_distance_statistics(stats_df)
    
    # Calculate and display class distribution
    class_percentages = plot_class_distribution(df)
    print("\nClass Distribution (%):")
    print("=" * 80)
    print(class_percentages.to_string())
    
    # Save statistics to CSV
    stats_df.to_csv('distance_statistics.csv')
    class_percentages.to_csv('class_distribution.csv')

if __name__ == '__main__':
    main() 