from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    content = db.Column(db.Text,nullable=False)
    category = db.Column(db.String(50),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    tags = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime,default= datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags.split(",") if self.tags else [],
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }