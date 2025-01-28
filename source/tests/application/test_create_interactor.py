import pytest
from unittest.mock import AsyncMock, MagicMock

from source.api.dependency.application.gateway import ApplicationGateway
from source.api.dependency.kafka.gateway import KafkaGateway
from source.api.interactors.application.create import CreateApplicationInteractor
from source.api.interactors.application.input_data import CreateApplicationInputData
from source.common.commiter import Commiter
from source.db.models.application import Application


@pytest.mark.asyncio
async def test_create_application_interactor():
    test_name = "test_name"
    test_description = "test_description"
    mock_gateway = MagicMock(spec=ApplicationGateway)
    mock_commiter = MagicMock(spec=Commiter)
    mock_kafka_service = MagicMock(spec=KafkaGateway)

    create_data = CreateApplicationInputData(
        user_name=test_name,
        description=test_description,
    )

    mock_gateway.save = AsyncMock()

    interactor = CreateApplicationInteractor(
        application_gateway=mock_gateway,
        commiter=mock_commiter,
        kafka_service=mock_kafka_service,
    )
    await interactor(create_data=create_data)

    assert mock_gateway.save.call_count == 1
    saved_instance = mock_gateway.save.call_args[0][0]

    assert isinstance(saved_instance, Application)
    assert saved_instance.user_name == test_name
    assert saved_instance.description == test_description

    mock_commiter.commit.assert_called_once()
