from typing import Union
from time import time

import asyncpg
from asyncpg import Pool, Connection

import config
from settings.cannot_change import needs_button


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

    async def close(self):
        await self.pool.close()

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
        work_experience INT DEFAULT 0,
        fire_balance BIGINT DEFAULT 0,
        chung_balance BIGINT DEFAULT 0,
        bonus_day SMALLINT DEFAULT 0,
        bonus_time INT DEFAULT 0,
        body SMALLINT DEFAULT 3,
        dirt SMALLINT DEFAULT 1,
        face SMALLINT DEFAULT 2,
        room_lvl SMALLINT DEFAULT 1,
        hall SMALLINT DEFAULT 0,
        kitchen SMALLINT DEFAULT 0,
        bathroom SMALLINT DEFAULT 0,
        bedroom SMALLINT DEFAULT 0,
        current_clothes SMALLINT DEFAULT 1,
        clothes SMALLINT[] DEFAULT '{1}',
        health REAL DEFAULT 1000,
        max_health SMALLINT DEFAULT 100,
        happiness REAL DEFAULT 100,
        time_draw INT DEFAULT 0,
        time_read INT DEFAULT 0,
        max_happiness SMALLINT DEFAULT 100,
        satiety REAL DEFAULT 100,
        time_ration INT DEFAULT 0,
        reserve_satiety INT DEFAULT 0,
        max_satiety SMALLINT DEFAULT 100,
        hygiene REAL DEFAULT 100,
        time_shower INT DEFAULT 0,
        time_toilet INT DEFAULT 0,
        max_hygiene SMALLINT DEFAULT 100,
        energy REAL DEFAULT 100,
        time_sleep INT DEFAULT 0,
        time_rest INT DEFAULT 0,
        max_energy SMALLINT DEFAULT 100
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_conversations(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Conversations (
        peer_id BIGINT PRIMARY KEY,
        id SERIAL,
        experience BIGINT NOT NULL DEFAULT 0
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

    async def get_fire_balance(self, peer_id):
        sql = "SELECT fire_balance FROM Users WHERE peer_id = $1 "
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_fire_work_energy_happiness(self, peer_id):
        sql = "SELECT fire_balance, work_experience, energy, happiness FROM Users WHERE peer_id = $1 "
        return await self.execute(sql, peer_id, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_user(self, peer_id, username):
        sql = "INSERT INTO Users (peer_id, username) VALUES($1, $2) returning *"
        return await self.execute(sql, peer_id, username, fetchrow=True)

    async def del_user(self, peer_id):
        sql = "DELETE FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, execute=True)

    async def get_user_hall(self, peer_id):
        sql = f"SELECT body, dirt, face, current_clothes, room_lvl, hall, " \
              f"happiness, max_happiness, time_draw, time_read, health, max_health " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_kitchen(self, peer_id):
        sql = f"SELECT body, dirt, face, current_clothes, room_lvl, kitchen, " \
              f"satiety, max_satiety, reserve_satiety, time_ration " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_bedroom(self, peer_id):
        sql = f"SELECT body, dirt, face, current_clothes, room_lvl, bedroom, " \
              f"energy, max_energy, time_sleep, time_rest, health, max_health " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_bathroom(self, peer_id):
        sql = f"SELECT body, dirt, face, current_clothes, room_lvl, bathroom, " \
              f"hygiene, max_hygiene, time_shower, time_toilet, health, max_health " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_passport(self, peer_id):
        sql = "SELECT username, fire_balance, chung_balance, bonus_day, room_lvl, work_experience " \
              "FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_status(self, peer_id):
        sql = "SELECT status FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_last_activity(self, peer_id):
        sql = "SELECT last_activity FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_energy(self, peer_id):
        sql = "SELECT energy FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_happiness(self, peer_id):
        sql = "SELECT happiness FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_user_indicators(self, peer_id):
        sql = "SELECT health, happiness, satiety, hygiene, energy FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_for_products_shop(self, peer_id):
        sql = "SELECT fire_balance, reserve_satiety, satiety, max_satiety FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_room_lvl_balance_rooms(self, peer_id):
        sql = f"SELECT room_lvl, fire_balance, hall, kitchen, bedroom, bathroom FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_room_lvl_furniture(self, peer_id, room):
        sql = f"SELECT room_lvl, {room}, fire_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_room_lvl_furniture_balance(self, peer_id, furniture):
        sql = f"SELECT room_lvl, {furniture}, fire_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_current_clothes(self, peer_id):
        sql = "SELECT current_clothes FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_clothes(self, peer_id):
        sql = "SELECT current_clothes, clothes, fire_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_full_balance(self, peer_id):
        sql = "SELECT fire_balance, chung_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_fire_balance(self, peer_id):
        sql = "SELECT fire_balance FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def update_user_fire_balance(self, peer_id, new_balance):
        sql = f"UPDATE Users SET fire_balance = $1 WHERE peer_id = $2"
        return await self.execute(sql, new_balance, peer_id, execute=True)

    async def update_user_time_button(self, peer_id, button, indicator):
        sql = f"UPDATE Users SET time_{button} = $1, {needs_button[button]['indicator']} = $2 WHERE peer_id = $3"
        return await self.execute(sql, time(), indicator, peer_id, execute=True)

    async def update_user_time_button_with_attachment(self, peer_id, button, indicator, name, value):
        sql = f"UPDATE Users SET time_{button} = $1, {needs_button[button]['indicator']} = $2, " \
              f"{name} = $3 WHERE peer_id = $4"
        return await self.execute(sql, time(), indicator, value, peer_id, execute=True)

    async def buy_indicator(self, peer_id, indicator_name, indicator_value, balance):
        sql = f"UPDATE Users SET {indicator_name} = $1, fire_balance = $2 WHERE peer_id = $3"
        return await self.execute(sql, indicator_value, balance, peer_id, execute=True)

    async def buy_indicator_with_attachment(self, peer_id, indicator_name, indicator_value,
                                            attachment_name, attachment_value, balance):
        sql = f"UPDATE Users SET {indicator_name} = $1, {attachment_name} = $2, fire_balance = $3 WHERE peer_id = $4"
        return await self.execute(sql, indicator_value, attachment_value, balance, peer_id, execute=True)

    async def work_cleaner_update(self, peer_id, energy, balance, work_experience):
        sql = f"UPDATE Users SET energy = $1, fire_balance = $2, work_experience = $3 WHERE peer_id = $4"
        return await self.execute(sql, energy, balance, work_experience, peer_id, execute=True)

    async def work_cleaner_update_with_attachment(self, peer_id, energy, balance, face, work_experience):
        sql = f"UPDATE Users SET energy = $1, face = $2, fire_balance = $3, work_experience = $4 WHERE peer_id = $5"
        return await self.execute(sql, energy, face, balance, work_experience, peer_id, execute=True)

    async def work_cleaner_update_without_attachment(self, peer_id, energy, balance, work_experience):
        sql = f"UPDATE Users SET energy = $1, fire_balance = $2, work_experience = $3 WHERE peer_id = $4"
        return await self.execute(sql, energy, balance, work_experience, peer_id, execute=True)

    async def get_user_reserve_satiety(self, peer_id):
        sql = "SELECT reserve_satiety, satiety, max_satiety, time_ration FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_time_button(self, peer_id, button):
        sql = f"SELECT time_{button}, {needs_button[button]['indicator']}, max_{needs_button[button]['indicator']} " \
              f"FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_cases_menu(self, peer_id):
        sql = f"SELECT fire_balance, chung_balance, bonus_time FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_rooms(self, peer_id):
        sql = f"SELECT hall, kitchen, bedroom, bathroom FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_user_bonus_time(self, peer_id):
        sql = "SELECT bonus_time FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def get_balance_and_reserve(self, peer_id):
        sql = "SELECT fire_balance, reserve_satiety, satiety, max_satiety FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_balance_and_energy(self, peer_id):
        sql = "SELECT fire_balance, energy, max_energy, happiness FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_balance_and_hygiene(self, peer_id):
        sql = "SELECT fire_balance, hygiene, max_hygiene FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_balance_and_happiness(self, peer_id):
        sql = "SELECT fire_balance, happiness, max_happiness, energy FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def get_balance_and_health(self, peer_id):
        sql = "SELECT fire_balance, health, max_health FROM Users WHERE peer_id = $1"
        return await self.execute(sql, peer_id, fetchrow=True)

    async def append_clothes(self, peer_id, clothes_num, fire_balance):
        sql = "UPDATE Users SET current_clothes=$1, clothes=array_append(clothes, $1), " \
              "fire_balance=$2 WHERE peer_id = $3"
        return await self.execute(sql, clothes_num, fire_balance, peer_id, execute=True)

    async def update_current_clothes(self, peer_id, clothes_num):
        sql = "UPDATE Users SET current_clothes=$1 WHERE peer_id = $2"
        return await self.execute(sql, clothes_num, peer_id, execute=True)

    async def start_over(self, peer_id):
        sql = f"UPDATE Users SET last_activity={time()}, status='active', " \
              "fire_balance=1000, chung_balance=0, bonus_day=0, bonus_time=0, body=3, dirt=1, face=2, " \
              "room_lvl=1, hall=0, kitchen=0, bathroom=0, bedroom=0, " \
              "health=100, happiness=100, satiety=100, hygiene=100, energy=100 WHERE peer_id = $1"
        return await self.execute(sql, peer_id, execute=True)

    async def buy_satiety(self, peer_id, ind, reserve):
        sql = "UPDATE Users SET satiety=$1, reserve_satiety=$2 WHERE peer_id=$3"
        return await self.execute(sql, ind, reserve, peer_id, execute=True)

    async def buy_satiety_with_attachment(self, peer_id, ind, reserve, body):
        sql = "UPDATE Users SET body=$1, satiety=$2, reserve_satiety=$3 WHERE peer_id=$4"
        return await self.execute(sql, body, ind, reserve, peer_id, execute=True)

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
        sql = "UPDATE Users SET fire_balance=$1, reserve_satiety=$2 WHERE peer_id=$3"
        return await self.execute(sql, fire, reserve, peer_id, execute=True)

    async def buy_coffee(self, peer_id, fire, energy):
        sql = "UPDATE Users SET fire_balance=$1, energy=$2 WHERE peer_id=$3"
        return await self.execute(sql, fire, energy, peer_id, execute=True)

    async def buy_sauna(self, peer_id, fire, hygiene):
        sql = "UPDATE Users SET fire_balance=$1, hygiene=$2 WHERE peer_id=$3"
        return await self.execute(sql, fire, hygiene, peer_id, execute=True)

    async def buy_game(self, peer_id, fire, happiness):
        sql = "UPDATE Users SET fire_balance=$1, happiness=$2 WHERE peer_id=$3"
        return await self.execute(sql, fire, happiness, peer_id, execute=True)

    async def buy_pharmacy(self, peer_id, fire, health):
        sql = "UPDATE Users SET fire_balance=$1, health=$2 WHERE peer_id=$3"
        return await self.execute(sql, fire, health, peer_id, execute=True)

    async def update_username(self, username, peer_id):
        sql = "UPDATE Users SET username=$1 WHERE peer_id=$2"
        return await self.execute(sql, username, peer_id, execute=True)

    async def update_user_room_lvl(self, new_room_lvl, balance, peer_id):
        sql = f"UPDATE Users SET room_lvl={new_room_lvl}, " \
              f"fire_balance={balance}, hall=0, kitchen=0, bedroom=0, bathroom=0, " \
              f"happiness=max_happiness WHERE peer_id=$1"
        return await self.execute(sql, peer_id, execute=True)

    async def update_last_activity(self, peer_id, time):
        sql = "UPDATE Users SET last_activity=$1 WHERE peer_id=$2"
        return await self.execute(sql, time, peer_id, execute=True)

    async def add_fire_balance(self, peer_id, count):
        sql = f"UPDATE Users SET fire_balance=fire_balance+$1 WHERE peer_id=$2"
        return await self.execute(sql, count, peer_id, execute=True)

    async def update_balance_furniture(self, peer_id, balance, furniture, lvl):
        sql = f"UPDATE Users SET fire_balance=$1, {furniture}=$2 WHERE peer_id=$3"
        return await self.execute(sql, balance, lvl, peer_id, execute=True)

    async def update_user_indicators_without_health(self, peer_id, body, dirt, face, happiness,
                                                    satiety, hygiene, energy):
        sql = "UPDATE Users SET body=$1, dirt=$2, face=$3, happiness=$4, satiety=$5, hygiene=$6, " \
              f"energy=$7, last_activity={time()} WHERE peer_id=$8"
        return await self.execute(sql, body, dirt, face, happiness, satiety, hygiene, energy, peer_id, execute=True)

    async def update_user_indicators_with_health(self, peer_id, body, dirt, face, happiness,
                                                 satiety, hygiene, energy, health):
        sql = "UPDATE Users SET body=$1, dirt=$2, face=$3, happiness=$4, satiety=$5, hygiene=$6, " \
              f"energy=$7, health=$8, last_activity={time()} WHERE peer_id=$9"
        return await self.execute(sql, body, dirt, face, happiness,
                                  satiety, hygiene, energy, health, peer_id, execute=True)

    async def update_status(self, peer_id, status):
        sql = "UPDATE Users SET status=$1, last_activity=$2 WHERE peer_id=$3"
        return await self.execute(sql, status, time(), peer_id, execute=True)

    async def update_fire_work_energy(self, peer_id, fire, work, energy):
        sql = "UPDATE Users SET fire_balance=$1, work_experience=$2, energy=$3 WHERE peer_id=$4"
        return await self.execute(sql, fire, work, energy, peer_id, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def check_user_peer_id(self, peer_id):
        sql = "SELECT peer_id FROM Users WHERE peer_id=$1"
        return await self.execute(sql, peer_id, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)