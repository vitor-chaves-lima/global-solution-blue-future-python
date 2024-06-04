import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.models import CompanyStatisticsPerStateResponse, CompanyStatisticsResponse, ItemPostRequest, StatesEnum
from core.exceptions import CompanyNotFound, ItemAlreadyExists, ItemAlreadyRecycled, ItemNotFound, ItemTypeNotFound, StateNotFound
from core.db.schemas import Item
from core.db import get_db
from core.db.repositories import CompaniesRepository, ItemTypesRepository, ItemsRepository, StatesRepository


api_router = APIRouter(prefix="/api")


def map_statistics(statistics: tuple[int, int, int, str]):
   (total, raw, recycled, item_type) = statistics
   recycled_percentage = (recycled / total) * 100 if total != 0 else 0

   return {
      "type": item_type,
      "total": total,
      "raw": raw,
      "recycled": recycled,
      "recycled_percentage": recycled_percentage
   }

@api_router.get("/{company_shortname}/statistics", response_model=CompanyStatisticsResponse, status_code=status.HTTP_200_OK)
async def get_company_statistics(company_shortname: str, db: Session = Depends(get_db)):
   lowered_company_shortname = company_shortname.lower()

   company = CompaniesRepository.find_by_shortname(db, lowered_company_shortname)
   if company is None:
      raise CompanyNotFound(company_shortname)

   statistics = ItemsRepository.get_statistics(db, company.id)
   total_items = 0
   total_raw = 0
   total_recycled = 0

   for item in statistics:
      total_items += item[0]
      total_raw += item[1]
      total_recycled += item[2]

   total_recycled_percentage = (total_recycled / total_items) * 100 if total_items != 0 else 0


   return_data = {
      "shortname": company.shortname,
      "name": company.name,
      "segment": company.segment.segment,
      "statistics": {
         "total": {
            "total": total_items,
            "raw": total_raw,
            "recycled": total_recycled,
            "recycled_percentage": total_recycled_percentage
         },
         "item_types": [],
      }
   }

   return_data["statistics"]["item_types"] = list(map(map_statistics, statistics))
   return return_data


@api_router.get("/{company_shortname}/statistics/{state_shortname}", response_model=CompanyStatisticsPerStateResponse, status_code=status.HTTP_200_OK)
async def get_company_statistics_by_state(company_shortname: str, state_shortname: StatesEnum, db: Session = Depends(get_db)):
   lowered_company_shortname = company_shortname.lower()
   lowered_state_shortname = state_shortname.lower()

   company = CompaniesRepository.find_by_shortname(db, lowered_company_shortname)
   if company is None:
      raise CompanyNotFound(company_shortname)

   statistics = ItemsRepository.get_statistics(db, company.id, state=lowered_state_shortname)
   total_items = 0
   total_raw = 0
   total_recycled = 0

   for item in statistics:
      total_items += item[0]
      total_raw += item[1]
      total_recycled += item[2]

   total_recycled_percentage = (total_recycled / total_items) * 100 if total_items != 0 else 0


   return_data = {
      "shortname": company.shortname,
      "name": company.name,
      "segment": company.segment.segment,
      "statistics": {
         "state": {
            "state": lowered_state_shortname,
            "total": total_items,
            "raw": total_raw,
            "recycled": total_recycled,
            "recycled_percentage": total_recycled_percentage
         },
         "item_types": [],
      }
   }

   return_data["statistics"]["item_types"] = list(map(map_statistics, statistics))
   return return_data


@api_router.post("/{company_shortname}/items", status_code=status.HTTP_201_CREATED)
async def post_company_item(company_shortname: str, request: ItemPostRequest, db: Session = Depends(get_db)):
   lowered_company_shortname = company_shortname.lower()
   lowered_item_type = request.item_type.lower()
   lowered_state_shortname = request.state.lower()

   company = CompaniesRepository.find_by_shortname(db, lowered_company_shortname)
   item_type = ItemTypesRepository.find_by_type_name(db, lowered_item_type)
   state = StatesRepository.find_by_shortname(db, lowered_state_shortname)

   if company is None:
      raise CompanyNotFound(company_shortname)

   if item_type is None:
      raise ItemTypeNotFound(request.item_type)
   
   if state is None:
      raise StateNotFound(request.state)
   
   if ItemsRepository.exists_by_token(db, request.token):
      raise ItemAlreadyExists(request.token)

   new_item = ItemsRepository.save(
      db, 
      Item(token = request.token, company_id = company.id, type_name = item_type.type, state_shortname = state.shortname)
   )

   return {
      "token": new_item.token,
      "item_type": new_item.type.type,
      "state": {
         "name": new_item.state.name,
         "shortname": new_item.state.shortname
      },
      "created_at": new_item.created_at,
      "updated_at": new_item.updated_at,
      "company": {
         "shortname": new_item.company.shortname,
         "name": new_item.company.name,
         "segment": new_item.company.segment.segment
      }
   }


@api_router.post("/recycle/{item_token}", status_code=status.HTTP_204_NO_CONTENT)
async def post_company_item(item_token: uuid.UUID, db: Session = Depends(get_db)):
   item = ItemsRepository.find_by_token(db, item_token)

   if item is None:
      raise ItemNotFound(item_token)

   if item.recycled == True:
      raise ItemAlreadyRecycled(item_token)

   ItemsRepository.recycle(db, item)