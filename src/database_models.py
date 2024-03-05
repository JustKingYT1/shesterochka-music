import peewee
import settings


database = peewee.SqliteDatabase(settings.DB_PATH)


class BaseModel(peewee.Model):
    class Meta:
        db = database


class User(BaseModel):
    name = peewee.CharField(null=False)
    nickname = peewee.CharField(unique=True, null=False)
    password = peewee.CharField(null=False)


class Music(BaseModel):
    title = peewee.CharField(null=False)
    artist = peewee.CharField(null=False)

    class Meta:
        db = database
        indexes = (('artist', 'title'), True)


class UserPlaylists(BaseModel):
    user_id = peewee.ForeignKeyField(User, backref='Playlists', null=False)
    music_id = peewee.ForeignKeyField(Music, backref='Playlists', null=False)

    class Meta:
        db = database
        indexes = (('user_id', 'music_id'), True)
    


database.create_tables([User, Music, UserPlaylists])