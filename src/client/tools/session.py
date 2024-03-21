from src.database_models import User, UserModel
import peewee
from src.client.tools.config_manager import ConfigManager

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
                )
        except peewee.IntegrityError:
            self.parent.show_message(text='This name is already occupied, try to enter another one', 
                                     error=True, 
                                     parent=self.parent)
            return
        
        new_user = User.get(nickname=user.nickname)

        self.user = UserModel(
            id=new_user.id,
            nickname=new_user.nickname,
            password=new_user.password,
            image_path=new_user.image_path
        )
        
        self.update_user_in_config()

        self.auth = True

    def login(self, nickname: str, password: str) -> None:
        user = User.get_or_none(nickname=nickname, password=password)
        if user:
            self.user = user
            self.auth = True
            self.update_user_in_config()

    def update_user_in_config(self) -> None:
        ConfigManager.set_config({'user': {'id': self.user.id, 
                                    'login': self.user.nickname, 
                                    'password': self.user.password, 
                                    'image_path': self.user.image_path}})

    def leave(self) -> None:
        self.auth = False
        self.user = UserModel(
            id=-1,
            nickname='Гость',
            password='',
            image_path=None
        )

        self.update_user_in_config()
    
    def set_parent(self, parent) -> None:
        self.parent = parent

# TODO