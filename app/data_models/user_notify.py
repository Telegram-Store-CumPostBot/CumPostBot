from pydantic import BaseModel


class UserNotify(BaseModel):
    chat_id: int
    bot_id: int
    message: str

    def __str__(self):
        return f'chat_id={self.chat_id}, ' \
               f'bot_id={self.bot_id}, ' \
               f'message="{self.message}" '


class UserNotifications(list[UserNotify]):
    def __init__(self, *args: UserNotify):
        super(UserNotifications, self).__init__()
        [self.append(notify) for notify in args]
