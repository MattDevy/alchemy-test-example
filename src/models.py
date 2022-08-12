from .config import DATABASE as CONFIG
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class KV(Base):
    __tablename__ = "kvs"
    key = Column(String(255), primary_key=True)
    value = Column(String(255))

    def get_uid(self):
        return self.key


class OrganizationOverride(Base):
    __tablename__ = "organization_overrides"
    organization_uid = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(String(255))

    def get_uid(self) -> Column:
        return self.organization_uid


class ListingOverride(Base):
    __tablename__ = "listing_overrides"
    listing_uid = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(String(255))

    def get_uid(self) -> Column:
        return self.listing_uid


class AssetOverride(Base):
    __tablename__ = "asset_overrides"
    asset_uid = Column(String(255), primary_key=True)
    key = Column(String(255), primary_key=True)
    value = Column(String(255))

    def get_uid(self) -> Column:
        return self.asset_uid
