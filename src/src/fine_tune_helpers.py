from src.fine_tune_helpers import preprocess_data, train_model, save_model
import logging

def fine_tune_model(dataset_path, config):
    try:
        # Preprocess data
        data = preprocess_data(dataset_path)
        
        # Initialize model and configure hyperparameters
        model = train_model(data, config)
        
        # Save the fine-tuned model
        save_model(model)
        
        logging.info("Model fine-tuning complete!")
    except Exception as e:
        logging.error(f"Error during model fine-tuning: {e}")

if __name__ == "__main__":
    import argparse

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fine-tune a model with specified dataset and configuration.")
    parser.add_argument("dataset_path", type=str, help="Path to the dataset file.")
    parser.add_argument("--config", type=str, default="configs/model_config.json", help="Path to the configuration file.")

    args = parser.parse_args()

    # Fine-tune the model with provided arguments
    fine_tune_model(args.dataset_path, args.config)