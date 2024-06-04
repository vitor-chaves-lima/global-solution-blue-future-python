from sqlalchemy import case, func
from sqlalchemy.orm import Session
from .schemas import Company, Item, ItemType, State


class CompaniesRepository:
    @staticmethod
    def find_by_shortname(db: Session, shortname: str) -> Company:
        return db.query(Company).filter(Company.shortname == shortname).first()

    @staticmethod
    def exists_by_shortname(db: Session, shortname: int) -> bool:
        return db.query(Company).filter(Company.shortname == shortname).first() is not None
    

class StatesRepository:
    @staticmethod
    def find_by_shortname(db: Session, shortname: str) -> State:
        return db.query(State).filter(State.shortname == shortname).first()
    

class ItemTypesRepository:
    @staticmethod
    def find_by_type_name(db: Session, type_name: str) -> Company:
        return db.query(ItemType).filter(ItemType.type == type_name).first()
    

class ItemsRepository:
    @staticmethod
    def find_by_token(db: Session, token: str) -> Item:
        return db.query(Item).filter(Item.token == token).first()


    @staticmethod
    def exists_by_token(db: Session, token: int) -> bool:
        return db.query(Item).filter(Item.token == token).first() is not None


    @staticmethod
    def save(db: Session, item: Item) -> Item:
        db.add(item)
        db.commit()
        return item


    @staticmethod
    def recycle(db: Session, item: Item) -> Item:
        item.recycled = True
        item.updated_at = func.now()
        db.add(item)
        db.commit()
        return item

    @staticmethod
    def get_statistics(db: Session, company_shortname, **kwargs) -> list[tuple[int, int, int, str]]:
        query = db.query(
            func.count().label('total'),
            func.count().filter(Item.recycled == False).label('raw'),
            func.count().filter(Item.recycled == True).label('recycled'),
            Item.type_name.label("item_type")
        ).filter(Item.company_id == company_shortname).group_by(Item.type_name)

        if 'state' in kwargs:
            query = query.filter(Item.state_shortname == kwargs.get('state'))

        return query.all()