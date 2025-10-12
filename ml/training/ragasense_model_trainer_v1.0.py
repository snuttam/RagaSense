#!/usr/bin/env python3
"""
🎵 RagaSense Model Trainer v1.0
Proper ML model training following best practices
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

# ML libraries
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# MLflow for experiment tracking
import mlflow
import mlflow.pytorch

@dataclass
class TrainingConfig:
    """Configuration for model training"""
    model_type: str = "cnn"
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2
    test_split: float = 0.1
    early_stopping_patience: int = 10
    model_save_path: str = "ml/models"

class RagaDataset(Dataset):
    """Proper PyTorch Dataset for raga classification"""
    
    def __init__(self, data: List[Dict], labels: List[str]):
        self.data = data
        self.labels = labels
        self.label_to_idx = {label: idx for idx, label in enumerate(set(labels))}
        self.idx_to_label = {idx: label for label, idx in self.label_to_idx.items()}
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        # This would return actual audio features and labels
        features = self.data[idx]["features"]
        label = self.label_to_idx[self.labels[idx]]
        return torch.tensor(features, dtype=torch.float32), torch.tensor(label, dtype=torch.long)

class RagaClassifier(nn.Module):
    """CNN-based raga classifier"""
    
    def __init__(self, num_classes: int, input_shape: Tuple[int, int]):
        super(RagaClassifier, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        
        # Calculate flattened size
        self.flattened_size = self._get_flattened_size(input_shape)
        
        self.fc1 = nn.Linear(self.flattened_size, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, num_classes)
        
        self.relu = nn.ReLU()
        
    def _get_flattened_size(self, input_shape):
        """Calculate flattened size after convolutions"""
        # Simplified calculation - in practice, you'd run a forward pass
        return 128 * (input_shape[0] // 8) * (input_shape[1] // 8)
        
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        
        x = x.view(x.size(0), -1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.fc3(x)
        
        return x

class RagaSenseModelTrainer:
    """
    Proper ML model trainer following best practices:
    1. Proper train/validation/test splits
    2. Model architecture definition
    3. Training loop with validation
    4. Model evaluation and metrics
    5. Model saving and versioning
    """
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.setup_logging()
        self.setup_directories()
        
    def setup_logging(self):
        """Setup proper logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/model_training.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_directories(self):
        """Setup required directories"""
        Path(self.config.model_save_path).mkdir(parents=True, exist_ok=True)
        
    def load_data(self) -> Tuple[List[Dict], List[str]]:
        """Load and prepare training data"""
        self.logger.info("Loading training data")
        
        # This would load actual processed data
        # For now, creating placeholder data
        data = []
        labels = []
        
        # Placeholder - in practice, load from processed data
        for i in range(1000):
            data.append({
                "features": np.random.random((13, 100)),  # MFCC features
                "metadata": {"duration": 60, "sample_rate": 22050}
            })
            labels.append(f"raga_{i % 50}")  # 50 different ragas
            
        return data, labels
        
    def create_data_loaders(self, data: List[Dict], labels: List[str]) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """Create train/validation/test data loaders"""
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            data, labels, test_size=self.config.test_split + self.config.validation_split, 
            random_state=42, stratify=labels
        )
        
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=self.config.test_split / (self.config.test_split + self.config.validation_split),
            random_state=42, stratify=y_temp
        )
        
        # Create datasets
        train_dataset = RagaDataset(X_train, y_train)
        val_dataset = RagaDataset(X_val, y_val)
        test_dataset = RagaDataset(X_test, y_test)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=self.config.batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=self.config.batch_size, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=self.config.batch_size, shuffle=False)
        
        return train_loader, val_loader, test_loader
        
    def train_model(self, model: nn.Module, train_loader: DataLoader, val_loader: DataLoader) -> Dict[str, Any]:
        """Train the model with proper validation"""
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.config.learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
        
        best_val_loss = float('inf')
        patience_counter = 0
        training_history = {"train_loss": [], "val_loss": [], "val_accuracy": []}
        
        for epoch in range(self.config.epochs):
            # Training phase
            model.train()
            train_loss = 0.0
            
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(device), target.to(device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                
            # Validation phase
            model.eval()
            val_loss = 0.0
            correct = 0
            total = 0
            
            with torch.no_grad():
                for data, target in val_loader:
                    data, target = data.to(device), target.to(device)
                    output = model(data)
                    val_loss += criterion(output, target).item()
                    
                    pred = output.argmax(dim=1)
                    correct += pred.eq(target).sum().item()
                    total += target.size(0)
                    
            val_accuracy = 100. * correct / total
            avg_train_loss = train_loss / len(train_loader)
            avg_val_loss = val_loss / len(val_loader)
            
            training_history["train_loss"].append(avg_train_loss)
            training_history["val_loss"].append(avg_val_loss)
            training_history["val_accuracy"].append(val_accuracy)
            
            scheduler.step(avg_val_loss)
            
            self.logger.info(f"Epoch {epoch+1}/{self.config.epochs}: "
                           f"Train Loss: {avg_train_loss:.4f}, "
                           f"Val Loss: {avg_val_loss:.4f}, "
                           f"Val Accuracy: {val_accuracy:.2f}%")
            
            # Early stopping
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                patience_counter = 0
                # Save best model
                torch.save(model.state_dict(), Path(self.config.model_save_path) / "best_model.pt")
            else:
                patience_counter += 1
                
            if patience_counter >= self.config.early_stopping_patience:
                self.logger.info(f"Early stopping at epoch {epoch+1}")
                break
                
        return training_history
        
    def evaluate_model(self, model: nn.Module, test_loader: DataLoader) -> Dict[str, Any]:
        """Evaluate model on test set"""
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()
        
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                pred = output.argmax(dim=1)
                
                all_predictions.extend(pred.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
                
        accuracy = accuracy_score(all_targets, all_predictions)
        report = classification_report(all_targets, all_predictions, output_dict=True)
        
        return {
            "test_accuracy": accuracy,
            "classification_report": report
        }
        
    def run_training(self) -> Dict[str, Any]:
        """Run complete training pipeline"""
        
        self.logger.info("Starting model training")
        
        # Start MLflow experiment
        mlflow.set_experiment("ragasense_model_training")
        
        with mlflow.start_run(run_name=f"training_{self.config.model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            
            # Log training parameters
            mlflow.log_params({
                "model_type": self.config.model_type,
                "learning_rate": self.config.learning_rate,
                "batch_size": self.config.batch_size,
                "epochs": self.config.epochs,
                "validation_split": self.config.validation_split
            })
            
            # Load data
            data, labels = self.load_data()
            
            # Create data loaders
            train_loader, val_loader, test_loader = self.create_data_loaders(data, labels)
            
            # Create model
            num_classes = len(set(labels))
            model = RagaClassifier(num_classes, (13, 100))  # MFCC shape
            
            # Train model
            training_history = self.train_model(model, train_loader, val_loader)
            
            # Evaluate model
            evaluation_results = self.evaluate_model(model, test_loader)
            
            # Log metrics
            mlflow.log_metrics({
                "test_accuracy": evaluation_results["test_accuracy"],
                "final_train_loss": training_history["train_loss"][-1],
                "final_val_loss": training_history["val_loss"][-1],
                "final_val_accuracy": training_history["val_accuracy"][-1]
            })
            
            # Save model
            model_path = Path(self.config.model_save_path) / f"raga_classifier_{self.config.model_type}_v1.0.pt"
            torch.save(model.state_dict(), model_path)
            mlflow.log_artifact(str(model_path), "models")
            
            # Log model
            mlflow.pytorch.log_model(model, "model")
            
            self.logger.info("Training completed successfully")
            
            return {
                "status": "success",
                "test_accuracy": evaluation_results["test_accuracy"],
                "model_path": str(model_path)
            }

def main():
    """Main function"""
    config = TrainingConfig()
    trainer = RagaSenseModelTrainer(config)
    
    try:
        results = trainer.run_training()
        print(f"✅ Training completed: {results}")
    except Exception as e:
        logging.error(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    main()
