#!/usr/bin/env python3
"""
Create MLflow experiment that will be visible in the UI
"""

import mlflow
import mlflow.sklearn
import numpy as np
import json
import os
from datetime import datetime

def create_visible_experiment():
    """Create an experiment that will be visible in the MLflow UI"""
    
    # Use the default tracking URI (what the UI is using)
    mlflow.set_tracking_uri("file:///Users/adhi/axonome/RagaSense/mlruns")
    
    # Create a new experiment
    experiment_name = "RagaSense_Demo"
    try:
        experiment = mlflow.create_experiment(experiment_name)
        print(f"✅ Created experiment: {experiment_name} (ID: {experiment})")
    except mlflow.exceptions.MlflowException as e:
        if "already exists" in str(e):
            experiment = mlflow.get_experiment_by_name(experiment_name)
            print(f"✅ Using existing experiment: {experiment_name} (ID: {experiment.experiment_id})")
        else:
            raise e
    
    # Set the experiment
    mlflow.set_experiment(experiment_name)
    
    # Create multiple runs
    with mlflow.start_run(run_name="RagaSense_Dataset_Analysis") as run:
        print(f"📊 Creating run: {run.info.run_name}")
        
        # Log parameters
        mlflow.log_param("dataset_name", "RagaSense_Unified")
        mlflow.log_param("data_sources", "Saraga, Ramanarunachalam, YouTube")
        mlflow.log_param("processing_date", datetime.now().isoformat())
        mlflow.log_param("sample_rate", 22050)
        mlflow.log_param("min_duration", 5.0)
        mlflow.log_param("max_duration", 1200.0)
        
        # Log metrics
        mlflow.log_metric("total_ragas", 50)
        mlflow.log_metric("carnatic_ragas", 25)
        mlflow.log_metric("hindustani_ragas", 25)
        mlflow.log_metric("avg_tempo", 120.5)
        mlflow.log_metric("avg_duration", 180.2)
        mlflow.log_metric("processing_time_seconds", 45.2)
        mlflow.log_metric("audio_quality_score", 0.87)
        mlflow.log_metric("feature_extraction_accuracy", 0.92)
        
        # Log tags
        mlflow.set_tag("project", "RagaSense")
        mlflow.set_tag("model_type", "Audio_Classification")
        mlflow.set_tag("data_type", "Indian_Classical_Music")
        mlflow.set_tag("status", "Demo_Run")
        
        print(f"   ✅ Logged parameters, metrics, and tags")
    
    with mlflow.start_run(run_name="Model_Training_CNN") as run:
        print(f"🤖 Creating run: {run.info.run_name}")
        
        # Log training parameters
        mlflow.log_param("model_architecture", "CNN")
        mlflow.log_param("learning_rate", 0.001)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("epochs", 50)
        mlflow.log_param("optimizer", "Adam")
        mlflow.log_param("loss_function", "CrossEntropyLoss")
        
        # Simulate training metrics
        epochs = 50
        for epoch in range(epochs):
            train_loss = 1.2 - epoch * 0.02 + np.random.normal(0, 0.05)
            val_loss = 1.3 - epoch * 0.018 + np.random.normal(0, 0.08)
            train_acc = 0.3 + epoch * 0.012 + np.random.normal(0, 0.02)
            val_acc = 0.25 + epoch * 0.011 + np.random.normal(0, 0.03)
            
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)
        
        # Log final metrics
        mlflow.log_metric("final_train_accuracy", 0.89)
        mlflow.log_metric("final_val_accuracy", 0.85)
        mlflow.log_metric("best_val_accuracy", 0.87)
        mlflow.log_metric("training_time_minutes", 125.5)
        
        mlflow.set_tag("model_type", "CNN")
        mlflow.set_tag("training_status", "completed")
        mlflow.set_tag("best_epoch", 42)
        
        print(f"   ✅ Logged training metrics for {epochs} epochs")
    
    with mlflow.start_run(run_name="Data_Processing_Pipeline") as run:
        print(f"⚙️ Creating run: {run.info.run_name}")
        
        # Log data processing parameters
        mlflow.log_param("pipeline_stage", "feature_extraction")
        mlflow.log_param("audio_files_processed", 1250)
        mlflow.log_param("successful_extractions", 1180)
        mlflow.log_param("failed_extractions", 70)
        mlflow.log_param("processing_method", "librosa")
        
        # Log processing metrics
        mlflow.log_metric("processing_success_rate", 0.944)
        mlflow.log_metric("avg_processing_time_per_file", 2.3)
        mlflow.log_metric("total_processing_time_minutes", 48.2)
        mlflow.log_metric("memory_usage_gb", 3.2)
        mlflow.log_metric("cpu_usage_percent", 85.5)
        
        # Log data quality metrics
        mlflow.log_metric("audio_quality_score", 0.87)
        mlflow.log_metric("feature_extraction_accuracy", 0.92)
        mlflow.log_metric("data_completeness", 0.95)
        mlflow.log_metric("noise_reduction_effectiveness", 0.78)
        
        mlflow.set_tag("pipeline_stage", "data_processing")
        mlflow.set_tag("status", "completed")
        mlflow.set_tag("processing_method", "librosa")
        
        print(f"   ✅ Logged data processing metrics")
    
    print(f"\n🎉 Successfully created experiment with 3 runs!")
    print(f"🌐 View at: http://localhost:5001")
    print(f"🔍 Look for experiment: '{experiment_name}'")

if __name__ == "__main__":
    create_visible_experiment()
