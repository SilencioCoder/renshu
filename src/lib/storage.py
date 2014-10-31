# -*- coding: utf-8 -*-


import MySQLdb
from lib.info import *


class Storage(object):
    def __init__(self):
        self.host = '172.20.80.99'
        self.user = 'root'
        self.pswd = ''
        self.data = 'jisho'

    def get_id(self, entry_id):
        lst_entries = []

        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.pswd,
                               db=self.data,
                               use_unicode=True,
                               charset='UTF8')
        cur = conn.cursor()

        try:
            entries = [[long(entry_id)]]

            if entries:
                str_sql = ', '.join(['%s' for i in range(len(entries))])
                str_prm = tuple([i[0] for i in entries])

                kanji = self.get_kanji(cur, str_sql, str_prm)
                reads = self.get_reads(cur, str_sql, str_prm)
                sense = self.get_sense(cur, str_sql, str_prm)

                parts = []
                gloss = []
                if sense:
                    str_sql = ', '.join(['%s' for i in range(len(sense))])
                    str_prm = tuple([i[0] for i in sense])

                    parts = self.get_parts(cur, str_sql, str_prm)
                    gloss = self.get_gloss(cur, str_sql, str_prm)

                for e in entries:
                    obj_entry = self.create_entry(e, kanji, reads, sense, parts, gloss)

                    lst_entries.append(obj_entry)

        except Exception as e:
            pass
        finally:
            conn.close()

        return lst_entries

    def retrieve(self, box, limit=None):
        lst_entries = []
        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.pswd,
                               db=self.data,
                               use_unicode=True,
                               charset='UTF8')
        cur = conn.cursor()

        try:
            entries = self.get_entries(cur, box, limit)

            if entries:
                str_sql = ', '.join(['%s' for i in range(len(entries))])
                str_prm = tuple([i[0] for i in entries])

                kanji = self.get_kanji(cur, str_sql, str_prm)
                reads = self.get_reads(cur, str_sql, str_prm)
                sense = self.get_sense(cur, str_sql, str_prm)

                parts = []
                gloss = []
                if sense:
                    str_sql = ', '.join(['%s' for i in range(len(sense))])
                    str_prm = tuple([i[0] for i in sense])

                    parts = self.get_parts(cur, str_sql, str_prm)
                    gloss = self.get_gloss(cur, str_sql, str_prm)

                for e in entries:
                    obj_entry = self.create_entry(e, kanji, reads, sense, parts, gloss)

                    lst_entries.append(obj_entry)

        except Exception as e:
            pass
        finally:
            conn.close()

    def get_entries(self, cur, box, limit):
        if limit:
            cur.execute("""
                SELECT c.entry_id
                FROM card AS c
                WHERE c.mastery = %s
                LIMIT %s
            """, (box, limit))
            return cur.fetchall()
        else:
            cur.execute("""
                SELECT c.entry_id
                FROM card AS c
                WHERE c.mastery = %s
            """, (box,))
            return cur.fetchall()

    def search_sense_entries(self, cur, subject, limit):
        tokens = subject.split(' ')
        if len(tokens) == 1:
            compare = subject
            search = ''
        elif len(tokens) > 1:
            compare = ' '.join(['+' + i for i in tokens])
            search = ' IN BOOLEAN MODE'
        else:
            return []

        if limit:
            cur.execute("""
                SELECT DISTINCT(s.entry_id) AS 'entry_id'
                FROM sense AS s
                INNER JOIN gloss AS g ON s.id = g.sense_id
                WHERE MATCH(g.content) AGAINST(%s)
                LIMIT %s
            """ % ('%s' + search, limit), (compare,))
        else:
            cur.execute("""
                SELECT DISTINCT(s.entry_id) AS 'entry_id'
                FROM sense AS s
                INNER JOIN gloss AS g ON s.id = g.sense_id
                WHERE MATCH(g.content) AGAINST(%s)
            """ % ('%s' + search,), (compare,))

        return cur.fetchall()

    def get_kanji(self, cur, str_sql, str_prm):
        cur.execute("""
            SELECT k.id, k.entry_id, k.content
            FROM k_ele AS k
            WHERE k.entry_id IN (%s)
        """ % str_sql, str_prm)
        return cur.fetchall()

    def get_reads(self, cur, str_sql, str_prm):
        cur.execute("""
            SELECT r.id, r.entry_id, r.content
            FROM  r_ele AS r
            WHERE r.entry_id IN (%s)
        """ % str_sql, str_prm)
        return cur.fetchall()

    def get_sense(self, cur, str_sql, str_prm):
        cur.execute("""
            SELECT s.id, s.entry_id
            FROM sense AS s
            WHERE s.entry_id IN (%s)
        """ % str_sql, str_prm)
        return cur.fetchall()

    def get_parts(self, cur, str_sql, str_prm):
        cur.execute("""
            SELECT p.id, p.sense_id, p.parts
            FROM pos AS p
            WHERE p.sense_id IN (%s)
        """ % str_sql, str_prm)
        return cur.fetchall()

    def get_gloss(self, cur, str_sql, str_prm):
        cur.execute("""
            SELECT g.id, g.sense_id, g.content
            FROM gloss AS g
            WHERE g.sense_id IN (%s)
        """ % str_sql, str_prm)
        return cur.fetchall()

    def create_entry(self, e, kanji, reads, sense, parts, gloss):
        obj_entry = Entry()
        obj_entry.id = e[0]
        for k in [row for row in kanji if row[1] == obj_entry.id]:
            obj_kanji = Writing()
            obj_kanji.id = k[0]
            obj_kanji.content = k[2]
            obj_entry.writings.append(obj_kanji)
        for r in [row for row in reads if row[1] == obj_entry.id]:
            obj_reads = Reading()
            obj_reads.id = r[0]
            obj_reads.content = r[2]
            obj_entry.readings.append(obj_reads)
        for s in [row for row in sense if row[1] == obj_entry.id]:
            obj_sense = Meaning()
            obj_sense.id = s[0]

            for p in [prow for prow in parts if prow[1] == obj_sense.id]:
                obj_parts = Parts()
                obj_parts.id = p[0]
                obj_parts.content = p[2]
                obj_sense.parts.append(obj_parts)

            for g in [grow for grow in gloss if grow[1] == obj_sense.id]:
                obj_gloss = Gloss()
                obj_gloss.id = g[0]
                obj_gloss.content = g[2]
                obj_sense.gloss.append(obj_gloss)

            obj_entry.meanings.append(obj_sense)
        return obj_entry

    def search_meaning(self, subject, limit):
        lst_entries = []

        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.pswd,
                               db=self.data,
                               use_unicode=True,
                               charset='UTF8')
        cur = conn.cursor()

        try:
            entries = self.search_sense_entries(cur, subject, limit)

            if entries:
                str_sql = ', '.join(['%s' for i in range(len(entries))])
                str_prm = tuple([i[0] for i in entries])

                kanji = self.get_kanji(cur, str_sql, str_prm)
                reads = self.get_reads(cur, str_sql, str_prm)
                sense = self.get_sense(cur, str_sql, str_prm)

                parts = []
                gloss = []
                if sense:
                    str_sql = ', '.join(['%s' for i in range(len(sense))])
                    str_prm = tuple([i[0] for i in sense])

                    parts = self.get_parts(cur, str_sql, str_prm)
                    gloss = self.get_gloss(cur, str_sql, str_prm)

                for e in entries:
                    obj_entry = self.create_entry(e, kanji, reads, sense, parts, gloss)

                    lst_entries.append(obj_entry)

        except Exception as e:
            pass
        finally:
            conn.close()

        return lst_entries

    def search_reading(self, subject):
        pass

    def search_write_entries(self, cur, subject, limit):
        if limit:
            cur.execute("""
                SELECT entry_id
                FROM k_ele
                WHERE content = %s
                LIMIT %s
            """, (subject, limit))
        else:
            cur.execute("""
                SELECT entry_id
                FROM k_ele
                WHERE content = %s
            """, (subject,))
        return cur.fetchall()

    def search_writing(self, subject, limit):
        lst_entries = []

        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.pswd,
                               db=self.data,
                               use_unicode=True,
                               charset='UTF8')
        cur = conn.cursor()

        try:
            entries = self.search_write_entries(cur, subject, limit)

            if entries:
                str_sql = ', '.join(['%s' for i in range(len(entries))])
                str_prm = tuple([i[0] for i in entries])

                kanji = self.get_kanji(cur, str_sql, str_prm)
                reads = self.get_reads(cur, str_sql, str_prm)
                sense = self.get_sense(cur, str_sql, str_prm)

                parts = []
                gloss = []
                if sense:
                    str_sql = ', '.join(['%s' for i in range(len(sense))])
                    str_prm = tuple([i[0] for i in sense])

                    parts = self.get_parts(cur, str_sql, str_prm)
                    gloss = self.get_gloss(cur, str_sql, str_prm)

                for e in entries:
                    obj_entry = self.create_entry(e, kanji, reads, sense, parts, gloss)

                    lst_entries.append(obj_entry)

        except Exception as e:
            pass
        finally:
            conn.close()

        return lst_entries
    def count_meaning(self, subject):
        lst_entries = []

        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.pswd,
                               db=self.data,
                               use_unicode=True,
                               charset='UTF8')
        cur = conn.cursor()

        try:
            entries = self.search_sense_entries(cur, subject, None)
            return len(entries)
        except Exception as e:
            pass
        finally:
            conn.close()

        return 0

    def save(self, entry, prompt, answer):
        conn = MySQLdb.connect(host=self.host,
                               user=self.user,
                               passwd=self.pswd,
                               db=self.data,
                               use_unicode=True,
                               charset='UTF8')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO card (entry_id, prompt, answer) VALUES (%s, %s, %s)", (entry, prompt, answer))
            conn.commit()
        except:
            raise
        finally:
            conn.close()