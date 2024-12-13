from huggingface_hub import HfApi
from datetime import datetime
from typing import Set, List
from loguru import logger

logger = logger.bind(tool="org_mover")

def load_exceptions(file_path: str) -> Set[str]:
    try:
        with open(file_path, 'r') as f:
            return {line.strip() for line in f if line.strip() and not line.startswith('#')}
    except FileNotFoundError:
        logger.warning("⚠️  Exceptions file {} not found. No exceptions will be applied.", file_path)
        return set()

def move_repos_between_orgs(source_org: str, target_org: str, token: str, exceptions_file: str = None, debug: bool = False):
    # Initialize the Hugging Face API
    api = HfApi(token=token)
    
    # Get timestamp for unique identifier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Load exceptions if file provided
    exceptions = load_exceptions(exceptions_file) if exceptions_file else set()
    
    # List all datasets and models from source organization and convert to lists
    logger.debug("📝 Fetching repositories from {}", source_org)
    datasets = list(api.list_datasets(author=source_org))
    models = list(api.list_models(author=source_org))
    
    # Filter out exceptions
    datasets_to_move = [d for d in datasets if d.id.split('/')[-1] not in exceptions]
    models_to_move = [m for m in models if m.id.split('/')[-1] not in exceptions]
    
    if exceptions:
        logger.info("🔍 Found {} exceptions to exclude", len(exceptions))
        if debug:
            logger.debug("🚫 Excluded repositories: {}", ", ".join(exceptions))
    
    def set_repo_private(repo_id: str, repo_type: str) -> bool:
        try:
            api.update_repo_visibility(
                repo_id=repo_id,
                private=True,
                repo_type=repo_type
            )
            logger.debug("🔒 Set {} to private", repo_id)
            return True
        except Exception as e:
            logger.error("❌ Failed to set {} to private: {}", repo_id, str(e))
            return False
    
    def move_repo_with_retry(item, repo_type: str) -> bool:
        # Extract repository name
        repo_name = item.id.split('/')[-1]
        
        # Construct source repo_id
        from_repo = f"{source_org}/{repo_name}"
        
        # Try with original name first
        to_repo = f"{target_org}/{repo_name}"
        
        try:
            # Set source repo to private before moving
            set_repo_private(from_repo, repo_type)
            
            # Move the repository
            api.move_repo(
                from_id=from_repo,
                to_id=to_repo,
                repo_type=repo_type
            )
            
            # Set destination repo to private after moving
            set_repo_private(to_repo, repo_type)
            
            logger.success("✅ Successfully moved {} to {}", from_repo, to_repo)
            return True
            
        except Exception as e:
            if "already exists" in str(e):
                # Try with timestamped name
                to_repo = f"{target_org}/{repo_name}_{timestamp}"
                try:
                    # Set source repo to private before moving
                    set_repo_private(from_repo, repo_type)
                    
                    # Move the repository
                    api.move_repo(
                        from_id=from_repo,
                        to_id=to_repo,
                        repo_type=repo_type
                    )
                    
                    # Set destination repo to private after moving
                    set_repo_private(to_repo, repo_type)
                    
                    logger.success("✅ Successfully moved {} to {} (renamed due to conflict)", from_repo, to_repo)
                    return True
                except Exception as e2:
                    logger.error("❌ Failed to move {} even with rename: {}", from_repo, str(e2))
                    return False
            else:
                logger.error("❌ Failed to move {}: {}", from_repo, str(e))
                return False
    
    # Move datasets
    if datasets_to_move:
        logger.info("\n📦 Moving {} Datasets...", len(datasets_to_move))
        dataset_results = [move_repo_with_retry(dataset, "dataset") for dataset in datasets_to_move]
    else:
        logger.info("ℹ️  No datasets to move")
        dataset_results = []
    
    # Move models
    if models_to_move:
        logger.info("\n🤖 Moving {} Models...", len(models_to_move))
        model_results = [move_repo_with_retry(model, "model") for model in models_to_move]
    else:
        logger.info("ℹ️  No models to move")
        model_results = []
    
    # Print summary
    moved_datasets = sum(dataset_results)
    moved_models = sum(model_results)
    
    logger.info("\n📊 Summary:")
    if datasets_to_move:
        success_rate = (moved_datasets / len(datasets_to_move)) * 100
        logger.info("📦 Datasets: {}/{} moved successfully ({:.1f}%)", 
                   moved_datasets, len(datasets_to_move), success_rate)
    if models_to_move:
        success_rate = (moved_models / len(models_to_move)) * 100
        logger.info("🤖 Models: {}/{} moved successfully ({:.1f}%)", 
                   moved_models, len(models_to_move), success_rate)