from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import DishkaRoute, inject, FromDishka

from source.api.interactors.kafka.get import GetKafkaMessagesInteractor
from source.common.error import ApplicationError
from source.schemas.pydantic.kafka import KafkaOutPutBase

router = APIRouter(
    tags=["Kafka"],
    prefix="/kafka",
    route_class=DishkaRoute,
)


@router.get(
    "/",
    response_model=list[KafkaOutPutBase],
)
@inject
async def get_application(
    interactor: FromDishka[GetKafkaMessagesInteractor],
):
    try:
        return await interactor.get_messages()

    except ApplicationError as e:
        raise HTTPException(
            status_code=404,
            detail={"message": e.message},
        )
