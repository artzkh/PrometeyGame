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
            attachment, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
            await db.update_user_indicators_without_health(peer_id, attachment, happiness, satiety, hygiene, energy)
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
            attachment, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
            await db.update_user_indicators_without_health(peer_id, attachment, happiness, satiety, hygiene, energy)
            if health <= rec_limit['health']:
                recommendations.append('health')
            return recommendations

    elif hygiene <= 0:
        if energy <= 0:
            health = health + min(hygiene, energy) * 0.7
            hygiene = energy = 0
        else:
            hygiene = 0
            attachment, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
            await db.update_user_indicators_without_health(peer_id, attachment, happiness, satiety, hygiene, energy)
            if health <= rec_limit['health']:
                recommendations.append('health')
            return recommendations

    else:
        if energy <= 0:
            energy = 0
        attachment, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
        await db.update_user_indicators_without_health(peer_id, attachment, happiness, satiety, hygiene, energy)
        if health <= rec_limit['health']:
            recommendations.append('health')
        return recommendations

    attachment, recommendations = generate_attachment(ceil(happiness), ceil(satiety), ceil(hygiene), ceil(energy))
    if ceil(health) <= 0:
        return False
    elif health <= 99:
        recommendations.append('health')
    await db.update_user_indicators_with_health(peer_id, attachment, happiness, satiety, hygiene, energy, health)
    return recommendations


def generate_attachment(happiness, satiety, hygiene, energy):

    recommendations = []

    if satiety >= 200:
        attachment = "5"
    elif satiety >= 120:
        attachment = "4"
    elif satiety >= 70:
        attachment = "3"
    elif satiety >= rec_limit['satiety']:
        attachment = "2"
    else:
        recommendations.append('satiety')
        attachment = "1"

    if hygiene >= rec_limit['hygiene']:
        attachment += "_1"
    else:
        recommendations.append('hygiene')
        attachment += "_2"

    if happiness >= 100 and energy >= 80:
        attachment += "_1"
    elif happiness >= 60 and energy >= 30:
        attachment += "_2"
    elif happiness >= rec_limit['happiness']:
        attachment += "_3"
    else:
        recommendations.append('happiness')
        attachment += "_4"

    if energy <= rec_limit['energy']:
        recommendations.append('energy')

    return attachment, recommendations
