from typing import Union
from time import time

import asyncpg
from asyncpg import Pool, Connection

import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        peer_id BIGINT PRIMARY KEY,
        id SERIAL,
        username VARCHAR(255) NOT NULL,
        last_activity INT DEFAULT 0, 
        status VARCHAR(255) DEFAULT 'training',
        fire_balance BIGINT DEFAULT 0,
        chung_balance BIGINT DEFAULT 0,
        bonus_day SMALLINT DEFAULT 0,
        bonus_time INT DEFAULT 0,
        attachment VARCHAR(255) DEFAULT '3_1_2',
        room_lvl SMALLINT DEFAULT 1,
        hall SMALLINT DEFAULT 0,
        kitchen SMALLINT DEFAULT 0,
        bathroom SMALLINT DEFAULT 0,
        bedroom SMALLINT DEFAULT 0,
        current_clothes SMALLINT DEFAULT 1,
        clothes SMALLINT[] DEFAULT '{1}',
        health REAL DEFAULT 100,
        max_health SMALLINT DEFAULT 100,
        happiness REAL DEFAULT 100,
        reserve_happiness INT DEFAULT 0,
        max_happiness SMALLINT DEFAULT 100,
        satiety REAL DEFAULT 100,
        reserve_satiety INT DEFAULT 0,
        max_satiety SMALLINT DEFAULT 100,
        hygiene REAL DEFAULT 100,
        reserve_hygiene INT DEFAULT 0,
        max_hygiene SMALLINT DEFAULT 100,
        energy REAL DEFAULT 100,
        reserve_energy INT DEFAULT 0,
        max_energy SMALLINT DEFAULT 100
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, peer_id, username):
        sql = "INSERT INTO Users (peer_id, username) VALUES($1, $2) returning *"
        return await self.execute(sql, peer_id, username, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def get_user_hall(self, peer_id):
        sql = f"SELECT attachment, current_clothes, room_lvl, hall, happiness, max_happiness, reserve_happiness " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_kitchen(self, peer_id):
        sql = f"SELECT attachment, current_clothes, room_lvl, kitchen, satiety, max_satiety, reserve_satiety " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_bedroom(self, peer_id):
        sql = f"SELECT attachment, current_clothes, room_lvl, bedroom, energy, max_energy, reserve_energy " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_bathroom(self, peer_id):
        sql = f"SELECT attachment, current_clothes, room_lvl, bathroom, hygiene, max_hygiene, reserve_hygiene " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_status(self, peer_id):
        sql = "SELECT status FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_last_activity(self, peer_id):
        sql = "SELECT last_activity FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_indicators(self, peer_id):
        sql = "SELECT health, happiness, satiety, hygiene, energy FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_room_lvl_furniture(self, peer_id, room):
        sql = f"SELECT room_lvl, {room} FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_room_lvl_furniture_balance(self, peer_id, furniture):
        sql = f"SELECT room_lvl, {furniture}, fire_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_clothes(self, peer_id):
        sql = "SELECT clothes FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_balance(self, peer_id):
        sql = "SELECT fire_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_reserve_happiness(self, peer_id):
        sql = "SELECT reserve_happiness, happiness, max_happiness FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_reserve_satiety(self, peer_id):
        sql = "SELECT reserve_satiety, satiety, max_satiety FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_reserve_hygiene(self, peer_id):
        sql = "SELECT reserve_hygiene, hygiene, max_hygiene FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_reserve_energy(self, peer_id):
        sql = "SELECT reserve_energy, energy, max_energy FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_bonus_time(self, peer_id):
        sql = "SELECT bonus_time FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def append_clothes(self, peer_id, clothes_num):
        sql = "UPDATE Users SET clothes=array_append(clothes, $1) WHERE peer_id = $2"
        return await self.execute(sql, clothes_num, peer_id, execute=True)

    async def start_over(self, peer_id):
        sql = f"UPDATE Users SET last_activity={time()}, status='active', " \
              "fire_balance=1000, chung_balance=0, bonus_day=0, bonus_time=0, attachment='3_1_2', " \
              "room_lvl=1, hall=0, kitchen=0, bathroom=0, bedroom=0, current_clothes=1, clothes='{1}', " \
              "health=100, happiness=100, satiety=100, hygiene=100, energy=100 WHERE peer_id = $1"
        return await self.execute(sql, peer_id, execute=True)

    async def buy_satiety(self, peer_id, ind, reserve):
        sql = "UPDATE Users SET satiety=$1, reserve_satiety=$2 WHERE peer_id=$3"
        return await self.execute(sql, ind, reserve, peer_id, execute=True)

    async def buy_hygiene(self, peer_id, ind, reserve):
        sql = "UPDATE Users SET hygiene=$1, reserve_hygiene=$2 WHERE peer_id=$3"
        return await self.execute(sql, ind, reserve, peer_id, execute=True)

    async def buy_happiness(self, peer_id, ind, reserve):
        sql = "UPDATE Users SET happiness=$1, reserve_happiness=$2 WHERE peer_id=$3"
        return await self.execute(sql, ind, reserve, peer_id, execute=True)

    async def buy_energy(self, peer_id, ind, reserve):
        sql = "UPDATE Users SET energy=$1, reserve_energy=$2 WHERE peer_id=$3"
        return await self.execute(sql, ind, reserve, peer_id, execute=True)

    async def buy_product(self, peer_id, fire, reserve):
        sql = "UPDATE Users SET fire_balance=$1, reserve_satiety=reserve_satiety+$2 WHERE peer_id=$3"
        return await self.execute(sql, fire, reserve, peer_id, execute=True)

    async def update_username(self, username, peer_id):
        sql = "UPDATE Users SET username=$1 WHERE peer_id=$2"
        return await self.execute(sql, username, peer_id, execute=True)

    async def update_last_activity(self, peer_id, time):
        sql = "UPDATE Users SET last_activity=$1 WHERE peer_id=$2"
        return await self.execute(sql, time, peer_id, execute=True)

    async def update_balance_furniture(self, peer_id, balance, furniture, lvl):
        sql = f"UPDATE Users SET fire_balance=$1, {furniture}=$2 WHERE peer_id=$3"
        return await self.execute(sql, balance, lvl, peer_id, execute=True)

    # Индикаторы

    async def update_user_indicators_without_health(self, peer_id, attachment, happiness, satiety, hygiene, energy):
        sql = "UPDATE Users SET attachment=$1, happiness=$2, satiety=$3, hygiene=$4, " \
              f"energy=$5, last_activity={time()} WHERE peer_id=$6"
        return await self.execute(sql, attachment, happiness, satiety, hygiene, energy, peer_id, execute=True)

    async def update_user_indicators_with_health(self, peer_id, attachment, happiness, satiety, hygiene, energy, health):
        sql = "UPDATE Users SET attachment=$1, happiness=$2, satiety=$3, hygiene=$4, " \
              f"energy=$5, health=$6, last_activity={time()} WHERE peer_id=$7"
        return await self.execute(sql, attachment, happiness, satiety, hygiene, energy, health, peer_id, execute=True)

    async def update_status(self, peer_id, status):
        sql = "UPDATE Users SET status=$1, last_activity=$2 WHERE peer_id=$3"
        return await self.execute(sql, status, time(), peer_id, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)