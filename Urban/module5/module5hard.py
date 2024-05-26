"""
Classes for interacting with 'UrTube' platform, each of which contains methods for
authorization and user registration, etc.
"""
import time
import bcrypt  # hashing library


class User:
    """User constructor"""
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = password
        self.age = age

    def __repr__(self):  # override representational decorator for easy use
        return self.nickname


class Video:
    """Video class"""
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration  # total video time
        self.time_now = 0  # current time
        self.adult_mode = adult_mode

    def __repr__(self):  # override representational decorator for easy use
        return self.title


class UrTube:
    """
    Main class of UrTube platform.
    Contains methods for authorization, age verification, video handling.
    Uses 'bcrypt' library for password hashing with default salt constant of 12
    to increase security level. Increasing constant effects on hashing time exponentially,
    depends on your machine hardware level. Constant can be changed on user behalf in __init__ before call.
    """
    def __init__(self):
        self.users: list[User] = []
        self.videos: set[Video] = set()  # set for unique videos
        self.current_user: User | None = None
        self._WORK_FACTOR = 12  # Constant for 'gensalt' function in bcrypt hashing algorithm

    def log_in(self, login: str, password: str):
        """
        Logs in user if exists.
        Uses bcrypt's password check function for hashed password matching
        :param login: Nickname used on registration
        :param password: Password used on registration
        """
        is_invalid = True
        for user in self.users:
            # check for user and password match
            # string passwords needs to be encoded first
            if user.nickname == login and bcrypt.checkpw(bytes(password.encode("utf-8")), user.password):
                self.current_user = user
                is_invalid = False
                break
        if is_invalid:
            print("Invalid credentials")

    def register(self, nickname: str, password: str, age: int):
        """
        Creates new account with unique nickname and password.
        Uses bcrypt's password hashing function with default salt constant
        :param nickname:
        :param password:
        :param age:
        """
        # check for existing account:
        if nickname not in str(self.users):
            # string password needs to be encoded first
            hashed = bcrypt.hashpw(bytes(password.encode("utf-8")), bcrypt.gensalt(rounds=self._WORK_FACTOR))
            user = User(nickname, hashed, age)
            self.users.append(user)
            self.current_user = user
        # if not:
        else:
            print(f"User {nickname} already exists")

    def log_out(self):
        """Logs out current user"""
        self.current_user = None

    def add(self, *videos: Video):
        """
        Adds new unique videos with set.update()
        :param videos: iterable[Video]
        """
        self.videos.update(videos)

    def get_videos(self, title: str):
        """
        Returns video list with matching argument
        :param title: search keyword
        :return: iterable[Video]
        """
        result = []
        for video in self.videos:
            if title.lower() in str(video).lower():  # check with lower register to avoid mismatching
                result.append(video)
        return result

    def watch_video(self, title: str):
        """
        Video resume handler.
        Checks for user login and user age verification to proceed watch videos
        :param title:
        """
        # check for user login:
        if self.current_user:
            # find the video
            for video in self.videos:
                if video.title == title:
                    # check for age verification
                    if video.adult_mode and self.current_user.age < 18:
                        print("You are under 18 years old, please leave the page!")
                        break
                    else:
                        while video.time_now < video.duration:  # proceed to watch until end
                            time.sleep(1)
                            video.time_now += 1
                            print(video.time_now, end=" ")
                        print("End of video")
        # if not:
        else:
            print("Login to watch the video")


# test
ur = UrTube()
v1 = Video('Best programming language in 2024', 200)
v2 = Video('Why do girls need a programmer guy?', 10, adult_mode=True)

# adding videos test
ur.add(v1, v2)

# search test
print(ur.get_videos('best'))
print(ur.get_videos('PROG'))

# user login verification and age restrictions test
ur.watch_video('Why do girls need a programmer guy?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Why do girls need a programmer guy?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Why do girls need a programmer guy?')

# login to another account test
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Try to open non-existing video
ur.watch_video('Best programming language in 2024!')
