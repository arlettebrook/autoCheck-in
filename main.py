from __future__ import annotations

import os.path
import sys
from typing import Optional, List, Dict

import toml
from charset_normalizer import from_bytes
from loguru import logger
from pydantic import BaseModel


class Push(BaseModel):
    # 是否开启推送 默认关闭
    PUSH_OR_NOR: bool = False
    # PUSHPLUS的TOKEN
    PUSHPLUS_TOKEN: str = None


class LoginCookie(BaseModel):
    uId: str = None
    login_cookie: str = None
    login_url: str = None
    # login_url的请求体
    login_url_payload: str = """{"type": "qq", "si": {"h38": "b885b12b67288e7dcc0183f30200000b31771b", "q36": "",
                                                    "s": "000000014068b89153f4562362f80aafc61a5f261f1bbe9f47f26dad070abd34edb2085eefbcbd8999bea9fd5e612dcfa466e132725b168151744f5683ca9b054eb4904d071de80c3c931c306beda187500b50f609b9fd4b0ec83d6db51719869479e9b9630b6bcc1e81329be0dbc36103739ebff1d91c0f0205c08041a2771cf25bdd18525e661da11a4825de788b5c90f99f65a5c3adecc909485c9fe813aa88bd65c212227b0525df84e1754191cb74aac19de74043edb0f4058c2e5ee988f186283ab73eb5b93e1b1d5774404ac7f0a8d563a9d72cd9278956163ce989302b5132e64ce0b0d92c84596cbbb47863d7603be0c6d3f91b543db0",
                                                    "o_data": "g=64df242b475e272d&t=1690455867510&r=5cFXlb4OTc"}}"""
    # 获取会员信息请求体
    get_vip_info_url_payload: str = """{"geticon": 1, "viptype": "svip", "platform": 1000}"""


class LoginCookieList(BaseModel):
    accounts:List[LoginCookie]=[]


class Config(BaseModel):
    login_cookie_list: LoginCookieList=LoginCookieList()
    push: Optional[Push] = Push()

    @staticmethod
    def load_config() -> Config:
        try:
            if os.path.exists("config.cfg"):
                with open("config.cfg", "rb") as f:
                    if guessed_str := str(from_bytes(f.read()).best()):
                        return Config.model_validate(toml.loads(guessed_str))
                    else:
                        raise ValueError("无法识别配置文件，请检查是否输入有误！")
            else:
                logger.warning("请添加config.cfg配置文件")
                exit(-1)
        except Exception as e:
            logger.exception(e)
            logger.error("配置文件有误，请重新修改！")
            exit(-1)

    @staticmethod
    def save_config(config: Config):
        logger.debug(f"保存的对象{config}")
        try:
            with open("config.cfg", "wb") as f:
                parsed_str = toml.dumps(config.model_dump()).encode(sys.getdefaultencoding())
                f.write(parsed_str)
                logger.debug(parsed_str)
                logger.debug("配置文件保存成功")
        except Exception as e:
            logger.exception(e)
            logger.warning("配置保存失败。")