from sqlalchemy import Column, ForeignKey, Integer, Table
from app.config.database import Base
from sqlalchemy.orm import relationship


# user_group = Table(
#     "user_group",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("group_id", ForeignKey("groups.id"), primary_key=True)
# )


class UserGroupModel(Base):
    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), index=True)

    user = relationship("UserModel", back_populates="user_groups")
    group = relationship("GroupModel", back_populates="group_users")
