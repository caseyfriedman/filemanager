from typing import Any, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.dialects.postgresql import JSONB
class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    type_annotation_map = {
        dict[str, Any]: JSON
    }

    
class FileEntry(Base):
    __tablename__ = "timestamp_test"
    id: Mapped[UUID] = mapped_column(init=True, primary_key=True)
    filename: Mapped[str]
    fileloc: Mapped[str]
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB)
    timestamp_added: Mapped[datetime]
