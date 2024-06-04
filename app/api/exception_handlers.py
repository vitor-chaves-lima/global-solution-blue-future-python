from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions import CompanyNotFound, ItemAlreadyExists, ItemAlreadyRecycled, ItemNotFound, ItemTypeNotFound, StateNotFound


async def company_not_found_exception_handler(_: Request, exc: CompanyNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Couldn't find a company with shortname: {exc.shortname}",
            "error": CompanyNotFound.__name__
        },
    )


async def item_type_not_found_exception_handler(_: Request, exc: ItemTypeNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Couldn't find an item type with name: {exc.type_name}",
            "error": ItemTypeNotFound.__name__
        },
    )


async def item_already_exists_exception_handler(_: Request, exc: ItemAlreadyExists):
    return JSONResponse(
        status_code=409,
        content={
            "message": f"An item was already registered with token: {exc.token}",
            "error": ItemAlreadyExists.__name__
        },
    )


async def state_not_found_exception_handler(_: Request, exc: StateNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Couldn't find a state with shortname: {exc.shortname}",
            "error": StateNotFound.__name__
        },
    )


async def item_not_found_exception_handler(_: Request, exc: ItemNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Couldn't find an item with token: {exc.token}",
            "error": ItemNotFound.__name__
        },
    )


async def item_already_reacycled_exception_handler(_: Request, exc: ItemAlreadyRecycled):
    return JSONResponse(
        status_code=409,
        content={
            "message": f"Item with token: {exc.token} is already recycled",
            "error": ItemAlreadyRecycled.__name__
        },
    )

def get_exception_handlers():
    return [
        (CompanyNotFound, company_not_found_exception_handler),
        (ItemTypeNotFound, item_type_not_found_exception_handler),
        (ItemAlreadyExists, item_already_exists_exception_handler),
        (StateNotFound, state_not_found_exception_handler),
        (ItemNotFound, item_not_found_exception_handler),
        (ItemAlreadyRecycled, item_already_reacycled_exception_handler)
    ]