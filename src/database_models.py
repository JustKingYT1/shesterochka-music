import peewee
import settings
import pydantic
import typing

database = peewee.SqliteDatabase(settings.DB_PATH)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class UserModel(pydantic.BaseModel):
    id: typing.Optional[int] = 0
    nickname: str
    password: str
    image_path: typing.Optional[str] = ''


class User(BaseModel):
    nickname = peewee.CharField(null=False, unique=True)
    password = peewee.CharField(null=False)
    image_path = peewee.CharField(null=True)


class Music(BaseModel):
    title = peewee.CharField(null=False)
    artist = peewee.CharField(null=False)
    path = peewee.CharField(null=False, unique=True)

    class Meta:
        database = database
        indexes = ((('title', 'artist'), True),)


class UserPlaylists(BaseModel):
    user_id = peewee.ForeignKeyField(User, backref='Playlists', null=False)
    music_id = peewee.ForeignKeyField(Music, backref='Playlists', null=False)

    class Meta:  
        database = database
        indexes = ((('user_id', 'music_id'), True),)
    

database.create_tables([User, Music, UserPlaylists])