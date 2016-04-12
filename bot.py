from __future__ import unicode_literals

import os
import re

from telegram import Bot
from util import extract_token


class TelegramBot(object):

    def __init__(self, token=None):
        self.offset = None
        self.commands = {}
        if token:
            self.bot = Bot(token)

    def set_token(self, token):
        self.bot = Bot(token)

    def loop(self):
        while 1:
            updates = self.bot.getUpdates(offset=self.offset, timeout=10)
            for update in updates:
                self.run_command(update)

            if updates:
                self.offset = updates[-1].update_id + 1

    def run_command(self, update):
        not_matched = True
        for pattern, func in self.commands.items():
            text = update.message.text
            matched = pattern.match(text)

            if not matched:
                continue

            not_matched = False

            kwargs = matched.groupdict()
            reply = func(**kwargs)
            if reply:
                self.bot.sendMessage(update.message.chat_id, reply)

        if not_matched:
            self.bot.sendMessage(update.message.chat_id, 'Not matched')

    def command(self, pattern):
        """
        This function is a decorator to bind command.
        """
        def real_decorator(func):
            compiled_pattern = re.compile(pattern)
            self.commands[compiled_pattern] = func
            return func

        return real_decorator