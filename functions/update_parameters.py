from math import ceil

from config import db
from settings.cannot_change import rec_limit


async def update_energy(peer_id, old_energy, new_energy, happiness, balance):
    old_energy, new_energy = ceil(old_energy), ceil(new_energy)

    if happiness >= 100:
        if (old_energy < 80) and (new_energy >= 80):
            await db.buy_indicator_with_attachment(peer_id, 'energy', new_energy, 'face', 1, balance)
        elif (old_energy < 30) and (new_energy >= 30):
            await db.buy_indicator_with_attachment(peer_id, 'energy', new_energy, 'face', 2, balance)
        else:
            await db.buy_indicator(peer_id, 'energy', new_energy, balance)
    elif happiness >= 60:
        if (old_energy < 30) and (new_energy >= 30):
            await db.buy_indicator_with_attachment(peer_id, 'energy', new_energy, 'face', 2, balance)
        else:
            await db.buy_indicator(peer_id, 'energy', new_energy, balance)
    else:
        await db.buy_indicator(peer_id, 'energy', new_energy, balance)

    if (old_energy < rec_limit['happiness']) and (new_energy >= rec_limit['happiness']):
        return True


async def update_happiness(peer_id, old_happiness, new_happiness, energy, balance):
    old_happiness, new_happiness = ceil(old_happiness), ceil(new_happiness)

    if energy < 30:
        if (old_happiness < rec_limit['happiness']) and (new_happiness >= rec_limit['happiness']):
            await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 3, balance)
            return True
        else:
            await db.buy_indicator(peer_id, 'happiness', new_happiness, balance)
    elif energy < 80:
        if (old_happiness < rec_limit['happiness']) and (new_happiness >= rec_limit['happiness']):
            if new_happiness >= 60:
                await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 2, balance)
            else:
                await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 3, balance)
            return True
        elif (old_happiness < 60) and (new_happiness >= 60):
            await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 2, balance)
        else:
            await db.buy_indicator(peer_id, 'happiness', new_happiness, balance)
    else:
        if (old_happiness < rec_limit['happiness']) and (new_happiness >= rec_limit['happiness']):
            if new_happiness >= 100:
                await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 1, balance)
            elif new_happiness >= 60:
                await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 2, balance)
            else:
                await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 3, balance)
            return True
        elif (old_happiness < 100) and (new_happiness >= 100):
            await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 1, balance)
        elif (old_happiness < 60) and (new_happiness >= 60):
            await db.buy_indicator_with_attachment(peer_id, 'happiness', new_happiness, 'face', 2, balance)
        else:
            await db.buy_indicator(peer_id, 'happiness', new_happiness, balance)


async def update_hygiene(peer_id, old_hygiene, new_hygiene, balance):
    old_hygiene, new_hygiene = ceil(old_hygiene), ceil(new_hygiene)

    if (old_hygiene < rec_limit['satiety']) and (new_hygiene >= rec_limit['satiety']):
        await db.buy_indicator_with_attachment(peer_id, 'hygiene', new_hygiene, 'dirt', 1, balance)
        return True
    else:
        await db.buy_indicator(peer_id, 'hygiene', new_hygiene, balance)

