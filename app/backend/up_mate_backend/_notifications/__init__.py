import requests
import up_mate_backend._config as config


def send_notification(updated_user: str, user_page: str) -> None:
    if not config.NOTIFY:
        return

    channel = config.NOTIFY_CHANNEL_TEMPLATE.format(updated_user)

    response = requests.post(
        f"https://{config.NOTIFY_HOST}/{channel}",
        data=f"{updated_user} just updated their status",
        headers={
            f"Authorization": f"Bearer {config.NOTIFY_TOKEN}",
            "Title": f"Your mate updated their status",
            "Click": f"{config.WEB_URL}/{user_page}",
        },
    )
    response.raise_for_status()
