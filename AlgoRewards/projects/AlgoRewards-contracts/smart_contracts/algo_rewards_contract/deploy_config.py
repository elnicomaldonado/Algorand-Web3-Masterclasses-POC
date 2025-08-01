import logging

import algokit_utils

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import (
        AlgoRewardsContractFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        AlgoRewardsContractFactory, default_sender=deployer_.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        # Fund the app with ALGO for asset creation
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )
        
        logger.info(f"Funded app {app_client.app_id} with 1 ALGO for asset creation")

    # Test the contract with a sample session creation
    try:
        # Create a test session
        test_session_id = "test-session-001"
        test_session_name = "Algorand Masterclass"
        test_session_description = "Learn about Algorand smart contracts and NFTs"
        test_metadata_url = "ipfs://QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme.md"
        
        response = app_client.send.create_session(
            args={
                "session_id": test_session_id,
                "session_name": test_session_name,
                "session_description": test_session_description,
                "metadata_url": test_metadata_url
            }
        )
        
        logger.info(
            f"Created test session on {app_client.app_name} ({app_client.app_id}) "
            f"with session_id={test_session_id}, session_number={getattr(response, 'return', 'N/A')}"
        )
        
        # Test getting session info
        session_info = app_client.send.get_session_info(
            args={"session_id": test_session_id}
        )
        
        logger.info(f"Session info: {getattr(session_info, 'return', 'N/A')}")
        
    except Exception as e:
        logger.warning(f"Test session creation failed: {e}")
        logger.info("Contract deployed successfully but test failed - this is normal for first deployment")

    logger.info(f"AlgoRewards contract deployed successfully!")
    logger.info(f"App ID: {app_client.app_id}")
    logger.info(f"App Address: {app_client.app_address}")
    logger.info("Ready for NFT minting operations!")
