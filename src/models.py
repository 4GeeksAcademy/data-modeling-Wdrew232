from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

db = SQLAlchemy()
# creates user
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationship with Post*
    posts = relationship("Post", back_populates="user")

#creates post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    
    # Relationship with User*
    user = relationship("User", back_populates="posts")
        
        #friends list !Hola, Mi Amigo
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    
     # Relationships to link users*
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])
    
    # Sending Messages :)
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(250), nullable=False)
    send_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    receive_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    
    # Relationships*
    send = relationship("User", foreign_keys=[send_id])
    receive = relationship("User", foreign_keys=[receive_id])
    # ???
    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "content": self.content,
            "send_id": self.send_id,
            "receive_id": self.receive_id
        }
