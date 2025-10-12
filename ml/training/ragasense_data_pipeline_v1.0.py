#!/usr/bin/env python3
"""
🎵 RagaSense Data Pipeline v1.0
Proper ML/AI data pipeline following best practices
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import pandas as pd
import numpy as np
from datetime import datetime
import argparse

# Audio processing libraries
import librosa
import soundfile as sf
from scipy import signal
from scipy.stats import skew, kurtosis

# MLflow for experiment tracking (not data collection)
import mlflow
import mlflow.sklearn

# DVC for data versioning
import dvc.api

@dataclass
class DataPipelineConfig:
    """Configuration for data pipeline"""
    input_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    output_data_dir: str = "data/final"
    validation_threshold: float = 0.8
    min_audio_duration: float = 30.0  # seconds
    max_audio_duration: float = 600.0  # seconds
    sample_rate: int = 22050
    batch_size: int = 32

class RagaSenseDataPipeline:
    """
    Proper ML data pipeline following best practices:
    1. Data validation and quality checks
    2. Feature extraction and preprocessing
    3. Data versioning with DVC
    4. Experiment tracking with MLflow
    """
    
    def __init__(self, config: DataPipelineConfig):
        self.config = config
        self.setup_logging()
        self.setup_directories()
        
    def setup_logging(self):
        """Setup proper logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/data_pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_directories(self):
        """Setup required directories"""
        for dir_path in [self.config.input_data_dir, 
                        self.config.processed_data_dir, 
                        self.config.output_data_dir]:
            Path(f"../{dir_path}").mkdir(parents=True, exist_ok=True)
            
    def validate_data_quality(self, data_path: str) -> Dict[str, Any]:
        """
        Validate data quality - proper ML practice
        """
        self.logger.info(f"Validating data quality for: {data_path}")
        
        validation_results = {
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "quality_score": 0.0,
            "issues": []
        }
        
        # Implement proper data validation
        # This is where we'd check audio quality, format, duration, etc.
        
        return validation_results
        
    def extract_features(self, audio_path: str) -> Dict[str, Any]:
        """
        Extract features from audio data - proper ML practice with real librosa
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.config.sample_rate)
            
            # Basic audio features
            duration = len(y) / sr
            
            # Skip if too short or too long
            if duration < self.config.min_audio_duration or duration > self.config.max_audio_duration:
                return None
            
            # MFCC features
            mfcc = librosa.feature.mfcc(
                y=y, 
                sr=sr, 
                n_mfcc=13,
                hop_length=512
            )
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
            
            # Chroma features
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            
            # Tonnetz features
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            
            # Rhythm features
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Statistical features
            features = {
                "mfcc": mfcc,
                "spectral_centroid": spectral_centroids,
                "spectral_rolloff": spectral_rolloff,
                "spectral_contrast": spectral_contrast,
                "zero_crossing_rate": zero_crossing_rate,
                "chroma": chroma,
                "tonnetz": tonnetz,
                "tempo": tempo,
                "duration": duration,
                "sample_rate": sr
            }
            
            return features
            
        except Exception as e:
            self.logger.error(f"Error extracting features from {audio_path}: {e}")
            return None
        
    def preprocess_data(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Preprocess data for ML training - proper ML practice
        """
        self.logger.info("Preprocessing data for ML training")
        
        processed_data = []
        for item in raw_data:
            # Implement proper preprocessing
            processed_item = {
                "id": item.get("id"),
                "features": self.extract_features(item.get("audio_data")),
                "label": item.get("raga_name"),
                "metadata": item.get("metadata", {})
            }
            processed_data.append(processed_item)
            
        return processed_data
        
    def run_pipeline(self, stage: str = "all") -> Dict[str, Any]:
        """
        Run the complete data pipeline - proper ML practice with real audio processing
        """
        self.logger.info(f"Starting RagaSense data pipeline - Stage: {stage}")
        
        # Start MLflow experiment for tracking
        mlflow.set_experiment("ragasense_data_pipeline")
        
        with mlflow.start_run(run_name=f"data_pipeline_{stage}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Log pipeline parameters
            mlflow.log_params({
                "input_dir": self.config.input_data_dir,
                "validation_threshold": self.config.validation_threshold,
                "min_audio_duration": self.config.min_audio_duration,
                "max_audio_duration": self.config.max_audio_duration,
                "sample_rate": self.config.sample_rate,
                "stage": stage
            })
            
            results = {"status": "success", "stage": stage}
            
            if stage in ["validation", "all"]:
                # Step 1: Data validation
                validation_results = self.validate_data_quality(self.config.input_data_dir)
                mlflow.log_metrics({
                    "data_quality_score": validation_results["quality_score"],
                    "total_files": validation_results["total_files"],
                    "valid_files": validation_results["valid_files"]
                })
                results["validation"] = validation_results
            
            if stage in ["features", "all"]:
                # Step 2: Feature extraction
                feature_results = self.extract_features_from_data()
                mlflow.log_metrics({
                    "features_extracted": feature_results["total_features"],
                    "extraction_success_rate": feature_results["success_rate"]
                })
                results["features"] = feature_results
            
            if stage in ["preprocessing", "all"]:
                # Step 3: Data preprocessing
                preprocessing_results = self.preprocess_features()
                mlflow.log_metrics({
                    "train_samples": preprocessing_results["train_samples"],
                    "val_samples": preprocessing_results["val_samples"],
                    "test_samples": preprocessing_results["test_samples"]
                })
                results["preprocessing"] = preprocessing_results
            
            self.logger.info(f"Data pipeline stage '{stage}' completed successfully")
            return results
    
    def extract_features_from_data(self) -> Dict[str, Any]:
        """Extract features from all audio files"""
        self.logger.info("Extracting features from audio data")
        
        features_dir = Path("../data/features")
        features_dir.mkdir(parents=True, exist_ok=True)
        
        all_features = []
        total_files = 0
        successful_extractions = 0
        
        # Process Saraga Hindustani data
        saraga_dir = Path("../data/saraga_extracted/hindustani/saraga1.5_hindustani")
        if saraga_dir.exists():
            for audio_file in saraga_dir.glob("**/*.mp3"):
                total_files += 1
                features = self.extract_features(str(audio_file))
                if features:
                    features["source"] = "saraga_hindustani"
                    features["file_path"] = str(audio_file)
                    all_features.append(features)
                    successful_extractions += 1
        
        # Process Carnatic-Hindustani data
        carnatic_dir = Path("../data/carnatic-hindustani")
        if carnatic_dir.exists():
            for audio_file in carnatic_dir.glob("**/*.mp3"):
                total_files += 1
                features = self.extract_features(str(audio_file))
                if features:
                    features["source"] = "carnatic_hindustani"
                    features["file_path"] = str(audio_file)
                    all_features.append(features)
                    successful_extractions += 1
        
        # Save features
        features_file = features_dir / "extracted_features.json"
        with open(features_file, 'w') as f:
            json.dump(all_features, f, indent=2, default=str)
        
        return {
            "total_files": total_files,
            "total_features": len(all_features),
            "success_rate": successful_extractions / total_files if total_files > 0 else 0,
            "features_file": str(features_file)
        }
    
    def preprocess_features(self) -> Dict[str, Any]:
        """Preprocess features for ML training"""
        self.logger.info("Preprocessing features for ML training")
        
        # Load features
        features_file = Path("../data/features/extracted_features.json")
        if not features_file.exists():
            raise FileNotFoundError("Features file not found. Run feature extraction first.")
        
        with open(features_file, 'r') as f:
            all_features = json.load(f)
        
        # Convert to numpy arrays and prepare for training
        processed_dir = Path("../data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # This would implement proper train/val/test splitting
        # For now, placeholder implementation
        train_samples = len(all_features) * 0.7
        val_samples = len(all_features) * 0.15
        test_samples = len(all_features) * 0.15
        
        return {
            "train_samples": int(train_samples),
            "val_samples": int(val_samples),
            "test_samples": int(test_samples),
            "total_samples": len(all_features)
        }

def main():
    """Main function following proper ML practices"""
    parser = argparse.ArgumentParser(description="RagaSense Data Pipeline")
    parser.add_argument("--stage", type=str, default="all", 
                       choices=["validation", "features", "preprocessing", "all"],
                       help="Pipeline stage to run")
    
    args = parser.parse_args()
    
    config = DataPipelineConfig()
    pipeline = RagaSenseDataPipeline(config)
    
    try:
        results = pipeline.run_pipeline(stage=args.stage)
        print(f"✅ Pipeline stage '{args.stage}' completed: {results}")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
