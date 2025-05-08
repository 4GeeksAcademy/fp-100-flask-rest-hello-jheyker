from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80),unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    seguidores: Mapped[list["Followers"]] = relationship(back_populates = "seguidor")
    seguidos: Mapped[list["Followers"]] = relationship(back_populates = "seguido")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    post: Mapped[list["Posts"]] = relationship(back_populates = "user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Followers(db.Model):
    __tablename__ = "followers"
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"),primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"),primary_key=True)
    seguidor: Mapped["User"]= relationship(back_populates = "seguidores")
    seguido: Mapped["User"]= relationship(back_populates = "seguidos")


class Comment (db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(150), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Posts"] = relationship(back_populates="comments")

class Posts (db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"]= relationship(back_populates = "post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    Media: Mapped["Media"] = relationship (back_populates = "post")

class Media (db.Model): 
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship (back_populates = "media")

