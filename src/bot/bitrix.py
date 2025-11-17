import requests
from datetime import datetime, timedelta, timezone
from os import getenv
from bot.loggers import logger

WEBHOOK = getenv("BITRIX_WEBHOOK")
MANAGER_ID = 1  # Заменить на ID менеджера в Bitrix24


def get_overdue_leads():
    url = WEBHOOK + "crm.lead.list.json"
    tz_plus3 = timezone(timedelta(hours=3))
    two_hours_ago_utc = datetime.now(tz_plus3) - timedelta(hours=2)
    formatted = two_hours_ago_utc.strftime("%Y-%m-%dT%H:%M:%S")

    params = {
        "filter[STATUS_ID]": "NEW",
        "filter[>DATE_CREATE]": formatted,
        "filter[IS_DELETED]": "N",
        "select[]": ["ID", "TITLE", "STATUS_ID", "DATE_CREATE"],

    }

    r = requests.get(url, params=params)
    result = r.json()
    if "error" in result:
        logger.error(f"Bitrix24 API error: {result}")
        return []

    logger.info(result)
    return result.get("result", [])


def add_comment(lead_id: int, text: str):
    url = WEBHOOK + "crm.lead.update"
    payload = {
        "id": lead_id,
        "fields": {
            "COMMENTS": text
        }
    }
    r = requests.post(url, json=payload)
    return r.json()


def create_task_for_lead(lead_id: int, lead_title: str):
    """Создаём задачу 'Перезвонить по лиду' с дедлайном через 2 часа"""
    from datetime import datetime, timedelta, timezone

    # Дедлайн через 2 часа в UTC
    deadline = datetime.now(timezone.utc) + timedelta(hours=2)
    deadline_iso = deadline.strftime("%Y-%m-%dT%H:%M:%S%z")

    url = WEBHOOK + "task.item.add"
    payload = {
        "fields": {
            "TITLE": f"Перезвонить по лиду {lead_title}",
            "RESPONSIBLE_ID": MANAGER_ID,
            "DEADLINE": deadline_iso,
            "DESCRIPTION": f"Лид ID: {lead_id}",
        }
    }

    r = requests.post(url, json=payload)
    logger.info(r.json())
    return r.json()