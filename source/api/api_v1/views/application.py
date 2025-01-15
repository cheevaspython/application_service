import json

from fastapi import APIRouter, HTTPException, Response, status
from dishka.integrations.fastapi import DishkaRoute, inject, FromDishka

from source.api.dependency.application.output_data import (
    ApplicationListPaginated,
    ApplicationResponseData,
)
from source.api.interactors.application.create import CreateApplicationInteractor
from source.api.interactors.application.get import GetApplication
from source.api.interactors.application.input_data import CreateApplicationInputData
from source.api.queries.application.get_many import GetApplications
from source.common.error import ApplicationError
from source.filters.application import ApplicationFilters
from source.filters.pagination import Pagination
from source.schemas.pydantic.application import ApplicationCreate
from source.services.application.convertor import convert_application_to_dataclass
from source.types.model_id import ModelIdType

router = APIRouter(
    tags=["Application"],
    prefix="/Application",
    route_class=DishkaRoute,
)


@router.get(
    "/{application_id}/",
    response_model=ApplicationResponseData,
)
@inject
async def get_application(
    application_id: ModelIdType,
    interactor: FromDishka[GetApplication],
):
    try:
        application = await interactor.by_id(application_id=application_id)
        return convert_application_to_dataclass(application)

    except ApplicationError as e:
        raise HTTPException(
            status_code=404,
            detail={"message": e.message},
        )


@router.get(
    "/",
    response_model=ApplicationListPaginated,
)
@inject
async def get_applications(
    query: FromDishka[GetApplications],
    user_name: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    try:
        filters = ApplicationFilters(user_name=user_name)
        pagination = Pagination(offset=offset, limit=limit)
        applications = await query(
            filters=filters,
            pagination=pagination,
        )
        return applications
    except ApplicationError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": e.message},
        )


@router.post(
    "/",
    response_model=ApplicationResponseData,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_application(
    input_data: ApplicationCreate,
    interactor: FromDishka[CreateApplicationInteractor],
):
    try:
        application = await interactor(
            create_data=CreateApplicationInputData(
                user_name=input_data.user_name,
                description=input_data.description,
            )
        )
        return convert_application_to_dataclass(application)

    except ApplicationError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": e.message},
        )
