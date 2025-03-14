import logging

from models import Config, Item
from models.errors import ConsoleConfigurationError, MaskConfigurationError
from notifiers import Notifier

log = logging.getLogger('tgtg')


class Console(Notifier):
    """Notifier for the console output"""

    def __init__(self, config: Config):
        self.enabled = config.console.get("enabled", False)
        self.body = config.console.get("body")
        self.cron = config.console.get("cron")

        if self.enabled:
            try:
                Item.check_mask(self.body)
            except MaskConfigurationError as exc:
                raise ConsoleConfigurationError(exc.message) from exc

    def send(self, item: Item) -> None:
        if self.enabled and self.cron.is_now:
            log.debug("Sending Console Notification")
            message = item.unmask(self.body)
            print(message)

    def __repr__(self) -> str:
        return "Console stdout"
