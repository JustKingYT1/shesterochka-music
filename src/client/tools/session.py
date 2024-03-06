from src.database_models import User
from src.database_models import User, UserModel
import peewee

class Session:
    user: UserModel = UserModel(
        id=-1,
        nickname='Гость',
        password='',
        image_path=None
    )
    auth: bool = False

    def register(self, user: UserModel) -> None:
        try:
            if user:
                User.create(
                    nickname=user.nickname,
                    password=user.password,
                    image_path=user.image_path
                )
        except peewee.IntegrityError:
            self.parent.show_message(text='Такое имя уже занято, попробуйте ввести другое')
            return
        
        new_user = User.get(nickname=user.nickname)

        self.user = UserModel(
            id=new_user.id,
            nickname=new_user.nickname,
            password=new_user.password,
            image_path=new_user.image_path
        )
    
    def set_parent(self, parent) -> None:
        self.parent = parent

# TODO