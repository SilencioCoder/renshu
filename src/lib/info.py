# -*- coding: utf-8 -*-

class Card(object):
    def __init__(self):
        self.id = None
        self.entry = None
        self.mastery = None

class Entry(object):
    def __init__(self):
        self.id = None
        self.sequence = None
        self.writings = []
        self.readings = []
        self.meanings = []

class Content(object):
    def __init__(self):
        self.id = None
        self.content = ''

class Writing(Content):
    pass

class Reading(Content):
    pass

class Meaning(object):
    def __init__(self):
        self.id = None
        self.parts = []
        self.gloss = []

class Parts(Content):
    pass

class Gloss(Content):
    pass