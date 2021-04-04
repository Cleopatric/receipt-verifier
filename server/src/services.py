""" Module for manage work with API, models and client. """
import json

from .configs import *
from .client import HttpClient
from .models import Base, engine, User, UserReceipt
from .data_models import PydanticUser, PydanticReceipt, PydanticUserWithReceipts, ReceiptBody
from logger import logger

from typing import NoReturn
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(bind=engine)
Session = sessionmaker()


class ReceiptVerifier:
    """ Auth and receipt verification instance."""

    base_url = r'https://buy.itunes.apple.com/verifyReceipt'
    sandbox_url = r'https://sandbox.itunes.apple.com/verifyReceipt'

    def __init__(self):
        self.session = Session(bind=engine)
        self.client = HttpClient()

    async def __add_user(self, username: str, email: str, pwd: str) -> dict:
        """ Add user in database.

        :param username: user username/login.
        :param email:    user email.
        :param pwd:      user password.
        :return:         response status.
        """
        try:
            user = User(name=username, email=email, password=pwd)
            self.session.add(user)
            self.session.commit()
            return ADD_USER_MSG
        except Exception as error:
            logger.error(str(error))

    async def add_user(self, params: dict) -> dict:
        """ Check and add user for adding in database.

        :param params: request params.
        :return:       sign up response status.
        """
        try:
            params['id'] = 0
            user = PydanticUser.parse_obj(params)
            users = self.session.query(User).filter(User.name == user.name)
            if users.count() > 0:
                return SIGN_UP_ERROR
            return await self.__add_user(user.name, user.email, user.password)
        except ValidationError as error:
            logger.error(error.json())

    async def add_receipt(self, user_id: int, params: dict) -> NoReturn:
        """ Add receipt in database.

        :param user_id: user ID.
        :param params:  request params.
        """
        try:
            params['id'] = 0
            parse = PydanticReceipt.parse_obj(params)
            is_retryable = parse.dict().get('', False)
            user = UserReceipt(user_id=user_id, environment=parse.environment,
                               latest_receipt=parse.latest_receipt, is_retryable=is_retryable,
                               latest_receipt_info=parse.latest_receipt_info, receipt=parse.receipt,
                               pending_renewal_info=parse.pending_renewal_info, status=parse.status)
            self.session.add(user)
            self.session.commit()
        except Exception as error:
            logger.error(str(error))

    async def get_receipt(self, params: dict, sandbox: bool = False) -> dict:
        """ Send a receipt to the AppStore for verification.

        :param params:  request params.
        :param sandbox: sandbox param to choose url endpoint.
        :return:        response from the AppStore.
        """
        if sandbox:
            response = await self.client.get_api_data(self.sandbox_url, [params])
        else:
            response = await self.client.get_api_data(self.base_url, [params])
        return response[0]

    async def get_user_info(self, username: str, password: str) -> dict:
        """ Get all user receipts and user info by login/password.
        
        :param username: user username/login.
        :param password: user password.
        :return:         dict with user info.
        """
        user = self.session.query(User).filter(User.name == username,
                                               User.password == password).first()
        if user:
            user_info = PydanticUserWithReceipts.from_orm(user)
            return user_info.dict(exclude={'password'})
        else:
            return AUTH_ERROR

    async def __verify_receipt(self, params: dict) -> dict:
        """ Check request params and get response from AppStore.
        
        :param params: request params.
        :return:       dict with user instance.
        """
        try:
            obj = ReceiptBody.parse_obj(params)
            req_body = obj.dict()
            sandbox = req_body.get('sandbox', False)
            response = await self.get_receipt(obj.json(by_alias=True), sandbox)
            return response
        except ValidationError as error:
            return {'code': 400, 'status': 'error', 'message': json.loads(error.json())}

    async def verify_receipt(self, username: str, password: str, params: dict) -> dict:
        """ Send a receipt to the App Store for verification and add result in database.

        :param username: user username/login.
        :param password: user password.
        :param params:   request params.
        :return:         App Store response data.
        """
        user = self.session.query(User).filter(User.name == username,
                                               User.password == password).first()
        if user:
            receipt = await self.__verify_receipt(params)
            status = receipt.get('status')
            if status == 'error':
                return receipt
            elif status == 0:
                await self.add_receipt(user.id, receipt)
                return receipt
            else:
                return {'status': status, 'message': RECEIPT_STATUS.get(str(status), '')}
        else:
            return AUTH_ERROR
