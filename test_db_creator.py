"""

db_creator test file

"""

import pytest
import db_creator as db
import query_maker

@pytest.fixture
def make_russian_db():
    return db.db_creator("russian.db")

def test_add_table(make_russian_db):
    creator = make_russian_db

    """
    
    Main files:
        mp3_no_space for words/frequency/

        Task checklist
        1) convert essential .numbers files to csv, tsv
        2) write schema dictionaries in this file
        3) read csv files in with csv module and add to database
        4) read tsv files in with open() command and str.split('\t')
        5) test
            - select a verb, conjugate it
            - select a noun, decline it
            - select an adjective, decline it
            - select a word, get its sentences
        
        Beyond:
        1) create spreadshoot from russian prefixes book, search for roots table
            - (word_id, prefix_id, suffix_id, root_id)
        2) 
    
    """

    verbs = {
        'word_id' : "INTEGER",
        "verb_id" : "INTEGER",
        "aspect" : "TEXT",
        "verb"   : "TEXT"
    }

    words = {
        'word_id' : 'INTEGER',
        'word'   : 'TEXT',
        'frequency' : 'TEXT',
        '___' : 'INTEGER',
        'type' : "TEXT",
        'mp3' : 'TEXT'
    }
     
    sentences_words = {
        "id" : "INTEGER",
        "sentence_id" : "INTEGER",
        "bare_id" : "INTEGER",
        "start" : "INTEGER",
        "length" : "INTEGER"
    }

    sentences = {
        "sentence_id" : "INTEGER",
        "russian" : "TEXT",
        "english" : "TEXT",
        "___" : "INTEGER"
    }

    translations = {
        "id" : "INTEGER",
        "word_id" : "INTEGER",
        "superpos" : "INTEGER",
        "position" : "INTEGER",
        "translation" : "TEXT"
    }

    declensions = {
        "id" : "INTEGER",
        "word_id" : "INTEGER",
        "nom" : "TEXT",
        "gen" : "TEXT",
        "dat" : "TEXT",
        "acc" : "TEXT",
        "inst" : "TEXT",
        "prep" : "TEXT"
    }

    conjugations = {
        
    }

    adjectives = {

    }

    # words
    creator.add_table("data/mp3_NO_SPACE.csv", "words", words)
    creator.to_null("N/A", "words")
    # creator.print_table("words", num_rows=15)

    # sentences
    creator.add_table("sentences.tsv", "sentences", sentences, "tsv")
    # creator.print_table("sentences", num_rows=15)

    # sentences_words
    creator.add_table("data/sentences_words.csv", "sentences_words", sentences_words)

    # verbs
    creator.add_table("data/verbs.csv", "verbs", verbs)
    creator.to_null("N/A", "verbs")
    # creator.print_table("verbs", num_rows=20)

    # translations
    creator.add_table("data/translations.csv", "translations", translations)

    # declensions
    creator.add_table("data/declensions.csv", "declensions", declensions)

    # query for sentence by id
    query = query_maker.query_maker("russian.db", creator.tables)
    results = query.get_sentences("hello", "word", is_russian=True)

    # swag breaks this
    # results = query.get_sentences("join", "word", is_russian=False)
    
    for result in results:
        print(result)
``
    # num = 1409
    # results = query.get_sentences(num, "id")
    # for result in results:
    #     print(result)
    
    # word = query.get_word(num)
    # print(f"""ID: {num}\tWord: {word} """)


    

    assert False