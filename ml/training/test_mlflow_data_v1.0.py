#!/usr/bin/env python3
"""
Test script to populate MLflow UI with sample data
"""

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from datetime import datetime
import json
import os

def create_sample_raga_data():
    """Create sample raga data for testing"""
    ragas = [
        "Kalyani", "Bhairavi", "Kambhoji", "Shankarabharanam", "Todi",
        "Kharaharapriya", "Natabhairavi", "Kiravani", "Vachaspati", "Charukesi"
    ]
    
    # Sample audio features
    features = []
    for i, raga in enumerate(ragas):
        feature_dict = {
            "raga": raga,
            "mfcc_mean": np.random.normal(0, 1, 13).tolist(),
            "spectral_centroid": np.random.uniform(1000, 4000),
            "tempo": np.random.uniform(60, 180),
            "duration": np.random.uniform(30, 300),
            "tradition": "Carnatic" if i % 2 == 0 else "Hindustani"
        }
        features.append(feature_dict)
    
    return features

def log_ragasense_experiment():
    """Log a comprehensive RagaSense experiment to MLflow"""
    
    # Set experiment
    experiment_name = "RagaSense_Data_Processing"
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run(run_name="RagaSense_Dataset_Analysis") as run:
        run_id = run.info.run_id
        
        # Log parameters
        mlflow.log_param("dataset_name", "RagaSense_Unified")
        mlflow.log_param("data_sources", "Saraga, Ramanarunachalam, YouTube")
        mlflow.log_param("processing_date", datetime.now().isoformat())
        mlflow.log_param("sample_rate", 22050)
        mlflow.log_param("min_duration", 5.0)
        mlflow.log_param("max_duration", 1200.0)
        
        # Create and log sample data
        raga_data = create_sample_raga_data()
        
        # Log metrics
        mlflow.log_metric("total_ragas", len(raga_data))
        mlflow.log_metric("carnatic_ragas", len([r for r in raga_data if r["tradition"] == "Carnatic"]))
        mlflow.log_metric("hindustani_ragas", len([r for r in raga_data if r["tradition"] == "Hindustani"]))
        mlflow.log_metric("avg_tempo", np.mean([r["tempo"] for r in raga_data]))
        mlflow.log_metric("avg_duration", np.mean([r["duration"] for r in raga_data]))
        mlflow.log_metric("processing_time_seconds", 45.2)
        
        # Log artifacts
        # Save raga data as JSON
        raga_data_file = "raga_sample_data.json"
        with open(raga_data_file, 'w') as f:
            json.dump(raga_data, f, indent=2)
        mlflow.log_artifact(raga_data_file)
        
        # Create and log a sample model
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        # Create sample training data
        X = np.random.rand(100, 13)  # 13 MFCC features
        y = np.random.randint(0, len(raga_data), 100)  # Raga labels
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train a simple model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Log model
        mlflow.sklearn.log_model(model, "raga_classifier")
        
        # Log model metrics
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        mlflow.log_metric("train_accuracy", train_score)
        mlflow.log_metric("test_accuracy", test_score)
        
        # Log tags
        mlflow.set_tag("project", "RagaSense")
        mlflow.set_tag("model_type", "RandomForest")
        mlflow.set_tag("data_type", "Audio_Features")
        mlflow.set_tag("status", "Test_Run")
        
        # Clean up
        os.remove(raga_data_file)
        
        print(f"✅ Logged experiment to MLflow!")
        print(f"Run ID: {run_id}")
        print(f"Experiment: {experiment_name}")
        print(f"View at: http://localhost:5001")

def log_data_processing_run():
    """Log a data processing run"""
    
    with mlflow.start_run(run_name="Data_Processing_Pipeline") as run:
        # Log data processing parameters
        mlflow.log_param("pipeline_stage", "feature_extraction")
        mlflow.log_param("audio_files_processed", 1250)
        mlflow.log_param("successful_extractions", 1180)
        mlflow.log_param("failed_extractions", 70)
        
        # Log processing metrics
        mlflow.log_metric("processing_success_rate", 0.944)
        mlflow.log_metric("avg_processing_time_per_file", 2.3)
        mlflow.log_metric("total_processing_time_minutes", 48.2)
        mlflow.log_metric("memory_usage_gb", 3.2)
        
        # Log data quality metrics
        mlflow.log_metric("audio_quality_score", 0.87)
        mlflow.log_metric("feature_extraction_accuracy", 0.92)
        mlflow.log_metric("data_completeness", 0.95)
        
        mlflow.set_tag("pipeline_stage", "data_processing")
        mlflow.set_tag("status", "completed")
        
        print(f"✅ Logged data processing run: {run.info.run_id}")

def log_model_training_run():
    """Log a model training run"""
    
    with mlflow.start_run(run_name="Model_Training_CNN") as run:
        # Log training parameters
        mlflow.log_param("model_architecture", "CNN")
        mlflow.log_param("learning_rate", 0.001)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("epochs", 50)
        mlflow.log_param("optimizer", "Adam")
        
        # Simulate training metrics
        epochs = 50
        train_losses = [1.2 - i*0.02 + np.random.normal(0, 0.05) for i in range(epochs)]
        val_losses = [1.3 - i*0.018 + np.random.normal(0, 0.08) for i in range(epochs)]
        train_accs = [0.3 + i*0.012 + np.random.normal(0, 0.02) for i in range(epochs)]
        val_accs = [0.25 + i*0.011 + np.random.normal(0, 0.03) for i in range(epochs)]
        
        # Log metrics for each epoch
        for epoch in range(epochs):
            mlflow.log_metric("train_loss", train_losses[epoch], step=epoch)
            mlflow.log_metric("val_loss", val_losses[epoch], step=epoch)
            mlflow.log_metric("train_accuracy", train_accs[epoch], step=epoch)
            mlflow.log_metric("val_accuracy", val_accs[epoch], step=epoch)
        
        # Log final metrics
        mlflow.log_metric("final_train_accuracy", train_accs[-1])
        mlflow.log_metric("final_val_accuracy", val_accs[-1])
        mlflow.log_metric("best_val_accuracy", max(val_accs))
        mlflow.log_metric("training_time_minutes", 125.5)
        
        mlflow.set_tag("model_type", "CNN")
        mlflow.set_tag("training_status", "completed")
        mlflow.set_tag("best_epoch", val_accs.index(max(val_accs)))
        
        print(f"✅ Logged model training run: {run.info.run_id}")

if __name__ == "__main__":
    print("🚀 Creating sample MLflow data for RagaSense...")
    
    # Log multiple runs to populate the UI
    log_ragasense_experiment()
    log_data_processing_run()
    log_model_training_run()
    
    print("\n🎉 MLflow UI should now show data!")
    print("📊 Visit: http://localhost:5001")
    print("🔍 Look for experiment: 'RagaSense_Data_Processing'")
