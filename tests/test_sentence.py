import pytest

from sentence import Sentence, SentenceSequence, Word
from tests.helpers import MemoryStream


def test_sentence_copies_words():
    words = [Word("echo")]
    sentence = Sentence(words)
    words.append(Word("x"))
    assert [w.word for w in sentence.words] == ["echo"]
    assert sentence.has_words()
    assert not Sentence([]).has_words()


def test_sentence_executes_command():
    out = MemoryStream()
    Sentence([Word("echo"), Word("hi")]).execute(MemoryStream(), out)
    assert out.buffer.getvalue() == "hi\n"


def test_sequence_container_protocol():
    sequence = SentenceSequence()
    first, second = Sentence([Word("a")]), Sentence([Word("b")])
    sequence.add_sentence(first)
    sequence.add_sentence(second)
    assert len(sequence) == 2
    assert sequence[1] is second
    assert list(sequence) == [first, second]


def test_empty_sequence_executes_nothing():
    SentenceSequence().execute()


def test_sequence_executes_sentences(capsys):
    sequence = SentenceSequence()
    sequence.add_sentence(Sentence([Word("echo"), Word("hi")]))
    sequence.execute()
    assert capsys.readouterr().out == "hi\n"
