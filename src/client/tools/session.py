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
                )
        except peewee.IntegrityError as ex:
            self.parent.show_message(text='Такое имя уже занято, попробуйте ввести другое', 
                                     error=True, 
                                     parent=self.parent)
            
            print(str(ex))
            return
        
        new_user = User.get(nickname=user.nickname)

        self.user = UserModel(
            id=new_user.id,
            nickname=new_user.nickname,
            password=new_user.password,
            image_path=new_user.image_path
        )

        self.auth = True

    def login(self, nickname: str, password: str) -> None:
        user = User.get_or_none(nickname=nickname, password=password)
        if user:
            self.user = user
            self.auth = True
        else:
            self.parent.show_message(text='Неверный логин или пароль', 
                                    error=True, 
                                    parent=self.parent)

    def leave(self) -> None:
        self.auth = False
        self.user = UserModel(
            id=-1,
            nickname='Гость',
            password='',
            image_path=None
        )
    
    def set_parent(self, parent) -> None:
        self.parent = parent

# TODO