"""

query_maker class file

Eric Riddoch
Nov 25, 2018

"""

import sqlite3 as sql

class query_maker:
    """

    The purpose of a query_maker object is to obtain 
    necessary language data given a speficic type of query.

    Examples:
        Given:          Provide:
        - word          - example sentence
        - verb          - conjugations
        - adjective     - short forms
        - noun          - declensions

    """

    def __init__(self, db_file, tables):
        """

        Store the parameters.

        Parameters:
            db_file  (str): file path of sqlite database file
            tables  (dict): dictionary {table_name : columns_dict} 

        """

        self.db_file = db_file
        self.tables = tables

    def get_id(self, word, is_russian=True):
        """
        
        Returns the ID of the word.

        Parameters:
            word        (str): russian word
            is_russian (bool): search of ID among russian/english words

        Returns:
            int: ID of given word

        """

        # will return ID
        ID = None

        # connect with database
        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()
                
                # if russian, use words table
                if is_russian:
                    ID = cur.execute(f"""
                    SELECT words.word_id
                    FROM words
                    WHERE words.word == '{word}'
                    """).fetchall()[0][0]
                
                # if english, use translations table
                else:
                    ID = cur.execute(f"""
                    SELECT translations.word_id
                    FROM translations
                    WHERE translations.translation == '{word}'
                    """).fetchall()[0][0]

        finally:
            conn.close()

        return ID

    def get_noun_declensions(self, search, search_by="id", is_russian=True):
        """

        Return a tuple of the declensions for the noun.

        Parameters:
            input      (str/int): id number or word
            input_type     (str): "id" or "word"
            is_russian    (bool): search among English/Russian sentences
        
        Returns:
            Tuples containing noun declensions of the given noun.

        Raises ValueError:
            - if search_by is of invalid type

        """

        # check for valid parameters
        if search_by not in ["id", "word"]:
            raise ValueError(f"Invalid type of search_by: {search_by}")

        # ID number of noun
        ID = None

        # connect with database
        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()
                
                if search_by == "word":
                    ID = self.get_id(search, is_russian)
                else:
                    ID = search


        finally:
            conn.close()

    def get_sentences(self, search, search_by="id", is_russian=True):
        """

        Given a word or word_id number, 
        retrieve all associated sentences (Russian, English). 

        Parameters:
            input      (str/int): id number or word
            input_type     (str): "id" or "word"
            is_russian    (bool): search among English/Russian sentences
        
        Returns:
            List of tuples containing sentences, (Russian, English).

        """

        # check for valid parameters
        if search_by not in ["id", "word"]:
            raise ValueError(f"Invalid type of search_by: {search_by}")

        # will be returned
        results = None
        ID = None

        # connect with database
        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()
                
                # if word, then get id
                if search_by == "word":
                    ID = self.get_id(search, is_russian)                    
                elif search_by == "id":
                    ID = search

                # print(f"input: {search} ⇒ id: {ID}")

                # search by word_id
                results = cur.execute(f"""SELECT S.russian, S.english
                    FROM sentences AS S INNER JOIN sentences_words AS SW 
                    ON S.sentence_id=SW.sentence_id
                    INNER JOIN words AS W
                    ON SW.bare_id=W.word_id
                    WHERE W.word_id == {ID}
                    """).fetchall()

        finally:
            conn.close()

        return results

    def get_word(self, ID):
        """
        Returns word corresponding to ID number:

        Parameters:
            ID (int): ID number

        Returns
            (str): word corresponding to ID number
        """

        # connect with database
        try:
            with sql.connect(self.db_file) as conn:
                cur = conn.cursor()

                word = cur.execute(f"""
                SELECT W.word
                FROM words as W
                WHERE W.word_id == {ID}""").fetchall()[0][0]

        finally:
            conn.close()

        return word
        
            