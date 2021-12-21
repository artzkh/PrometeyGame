from time import time
from math import ceil

from config import db
from settings.cannot_change import rec_limit


async def calculate_indicators(peer_id, last_activity):
    passed_time = ((time() - last_activity) / 60) / 5

    indicators = await db.get_user_indicators(peer_id)
    happiness, satiety, hygiene, energy = [indicator-passed_time for indicator in indicators[1:]]
    health = indicators[0]

    if happiness <= 0:
        if satiety <= 0:
            if hygiene <= 0:
                if energy <= 0:
                    indicators = [happiness, satiety, hygiene, energy]
                    indicators.sort(reverse=True)
                    health += indicators[1] * 0.7
                    happiness = satiety = hygiene = energy = 0
                else:
                    indicators = [happiness, satiety, hygiene]
                    indicators.sort(reverse=True)
                    health += indicators[1] * 0.7
                    happiness = satiety = hygiene = 0
            elif energy <= 0:
                indicators = [happiness, satiety, energy]
                indicators.sort(reverse=True)
                health += indicators[1] * 0.7
                happiness = satiety = energy = 0
            else:
                health += min(happiness, satiety) * 0.7
                happiness = satiety = 0
        elif hygiene <= 0:
            if energy <= 0:
                indicators = [happiness, hygiene, energy]
                indicators.sort(reverse=True)
                health += indicators[1] * 0.7
                happiness = hygiene = energy = 0
            else:
                health += min(happiness, hygiene) * 0.7
                happiness = hygiene = 0
        elif energy <= 0:
            health = health + min(happiness, satiety) * 0.7
            happiness = energy = 0
        else:
            happiness = 0
            body, dirt, face, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
            await db.update_user_indicators_without_health(peer_id, body, dirt, face, happiness, satiety, hygiene, energy)
            if health <= rec_limit['health']:
                recommendations.append('health')
            return recommendations
    elif satiety <= 0:
        if hygiene <= 0:
            health = health
            if energy <= 0:
                indicators = [satiety, hygiene, energy]
                indicators.sort(reverse=True)
                health += indicators[1] * 0.7
                satiety = hygiene = energy = 0
            else:
                health = health + min(satiety, hygiene) * 0.7
                satiety = hygiene = 0
        elif energy <= 0:
            health = health + min(satiety, energy) * 0.7
            satiety = energy = 0
        else:
            satiety = 0
            body, dirt, face, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
            await db.update_user_indicators_without_health(peer_id, body, dirt, face, happiness, satiety, hygiene, energy)
            if health <= rec_limit['health']:
                recommendations.append('health')
            return recommendations

    elif hygiene <= 0:
        if energy <= 0:
            health = health + min(hygiene, energy) * 0.7
            hygiene = energy = 0
        else:
            hygiene = 0
            body, dirt, face, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
            await db.update_user_indicators_without_health(peer_id, body, dirt, face, happiness, satiety, hygiene, energy)
            if health <= rec_limit['health']:
                recommendations.append('health')
            return recommendations

    else:
        if energy <= 0:
            energy = 0
        body, dirt, face, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
        await db.update_user_indicators_without_health(peer_id, body, dirt, face, happiness, satiety, hygiene, energy)
        if health <= rec_limit['health']:
            recommendations.append('health')
        return recommendations

    body, dirt, face, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
    if ceil(health) <= 0:
        return False
    elif health <= 99:
        recommendations.append('health')
    await db.update_user_indicators_with_health(peer_id, body, dirt, face, happiness, satiety, hygiene, energy, health)
    return recommendations


def generate_attachment(happiness, satiety, hygiene, energy):

    recommendations = []

    if hygiene > rec_limit['hygiene']:
        dirt = 1
    else:
        recommendations.append('hygiene')
        dirt = 2

    if satiety >= 200:
        body = 5
    elif satiety >= 120:
        body = 4
    elif satiety >= 70:
        body = 3
    elif satiety > rec_limit['satiety']:
        body = 2
    else:
        recommendations.append('satiety')
        body = 1

    if energy <= rec_limit['energy']:
        recommendations.append('energy')

    if happiness >= 100 and energy >= 80:
        face = 1
    elif happiness >= 60 and energy >= 30:
        face = 2
    elif happiness > rec_limit['happiness']:
        face = 3
    else:
        recommendations.append('happiness')
        face = 4

    return body, dirt, face, recommendations
