from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

db = SQLAlchemy()

# User Model


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(250), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow)

    # Relationships
    posts = relationship("Post", back_populates="user")
    friends = relationship("Friends", back_populates="user")
    messages_sent = relationship("Messages", foreign_keys="[Messages.send_id]")
    messages_received = relationship(
        "Messages", foreign_keys="[Messages.receive_id]")

# Post Model


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(250), nullable=True)
    image_url = db.Column(db.String(250), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))

    # Relationship
    user = relationship("User", back_populates="posts")

# Friends Model


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])

# Messages Model


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(250), nullable=False)
    send_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    receive_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    # Relationships
    send = relationship("User", foreign_keys=[send_id])
    receive = relationship("User", foreign_keys=[receive_id])

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "content": self.content,
            "send_id": self.send_id,
            "receive_id": self.receive_id,
            "is_read": self.is_read
        }
