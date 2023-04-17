from datetime import datetime
from sqlalchemy import func, String
from sqlalchemy.orm import mapped_column, Mapped
from database.connection import Base

class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
