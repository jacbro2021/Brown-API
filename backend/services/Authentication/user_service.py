from fastapi import Depends
from ...database import db_session

class UserService():

    def __init__(self,
                session = Depends(db_session)
    ):
        self._session = session


    

        