#!/usr/bin/env python3
"""
Verify MLflow data is accessible and show experiment details
"""

import mlflow
import mlflow.tracking

def verify_mlflow_data():
    """Verify MLflow data is accessible"""
    
    # Set tracking URI to the main mlruns directory
    mlflow.set_tracking_uri("file:///Users/adhi/axonome/RagaSense/mlruns")
    
    print("🔍 MLflow Data Verification")
    print("=" * 50)
    print(f"Tracking URI: {mlflow.get_tracking_uri()}")
    
    # Get all experiments
    experiments = mlflow.search_experiments()
    print(f"\n📊 Found {len(experiments)} experiments:")
    
    for exp in experiments:
        print(f"\n🎯 Experiment: {exp.name}")
        print(f"   ID: {exp.experiment_id}")
        print(f"   Artifact Location: {exp.artifact_location}")
        
        # Get runs for this experiment
        runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
        print(f"   Runs: {len(runs)}")
        
        if len(runs) > 0:
            print("   Recent runs:")
            for i, (_, run) in enumerate(runs.head(3).iterrows()):
                print(f"     {i+1}. {run['tags.mlflow.runName']} ({run['run_id'][:8]}...)")
                print(f"        Status: {run['status']}")
                print(f"        Start Time: {run['start_time']}")
    
    # Check specific experiment
    try:
        ragasense_exp = mlflow.get_experiment_by_name("RagaSense_Data_Processing")
        if ragasense_exp:
            print(f"\n✅ RagaSense_Data_Processing experiment found!")
            print(f"   ID: {ragasense_exp.experiment_id}")
            
            # Get runs for RagaSense experiment
            runs = mlflow.search_runs(experiment_ids=[ragasense_exp.experiment_id])
            print(f"   Total runs: {len(runs)}")
            
            if len(runs) > 0:
                print("\n📈 Run Details:")
                for i, (_, run) in enumerate(runs.iterrows()):
                    print(f"\n   Run {i+1}: {run['tags.mlflow.runName']}")
                    print(f"   Run ID: {run['run_id']}")
                    print(f"   Status: {run['status']}")
                    print(f"   Duration: {run['end_time'] - run['start_time']:.2f} seconds")
                    
                    # Show some metrics
                    metrics = [col for col in runs.columns if col.startswith('metrics.')]
                    if metrics:
                        print(f"   Metrics: {len(metrics)} logged")
                        for metric in metrics[:3]:  # Show first 3 metrics
                            value = run[metric]
                            if not pd.isna(value):
                                print(f"     - {metric.replace('metrics.', '')}: {value}")
        else:
            print("\n❌ RagaSense_Data_Processing experiment not found")
            
    except Exception as e:
        print(f"\n❌ Error accessing experiment: {e}")
    
    print(f"\n🌐 MLflow UI should be available at: http://localhost:5001")
    print("   Look for the 'RagaSense_Data_Processing' experiment")

if __name__ == "__main__":
    verify_mlflow_data()
