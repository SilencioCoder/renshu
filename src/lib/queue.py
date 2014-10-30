# -*- coding: utf-8 -*-

from random import shuffle


class Queue(object):
    def __init__(self):
        self.min = 1
        self.max = 6
        self.card = None
        self.queue = None
        self.storage = None

    def initialize(self, level):
        self.queue = self.storage.retrieve(level)
        shuffle(self.queue)

    def next(self):
        if self.queue:
            self.card = self.queue.pop()
            return self.card
        return None

    def correct(self):
        if self.card.mastery < self.max:
            self.card.mastery += 1
            self.storage.save(self.card)

    def incorrect(self):
        if self.card.mastery > self.min:
            self.card.mastery -= 1
            self.storage.save(self.card)
