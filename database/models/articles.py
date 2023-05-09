from datetime import datetime
from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.connection import Base


class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_user: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)


class Articles(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    recommended_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    user = relationship("User", foreign_keys=[recommended_by])


class ArticlesTags(Base):
    __tablename__ = "articles_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_article: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    id_tag: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    article = relationship("Article", foreign_keys=[id_article])
    tags = relationship("Tags", foreign_keys=[id_tag])
