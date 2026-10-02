import os

from sentence import Assignment, Sentence, SentenceSequence, Word
from tests.helpers import MemoryStream
from utils.session import Session


def test_sentence_copies_words():
    words = [Word("echo")]
    sentence = Sentence([], words)
    words.append(Word("x"))
    assert [w.word for w in sentence.words] == ["echo"]
    assert sentence.has_words()
    assert not Sentence([], []).has_words()


async def test_sentence_executes_command():
    session = Session()
    out = MemoryStream()
    await Sentence([], [Word("echo"), Word("hi")]).execute(session, MemoryStream(), out)
    assert out.buffer.getvalue() == "hi\n"


def test_sequence_container_protocol():
    session = Session()
    sequence = SentenceSequence(session)
    first, second = Sentence([], [Word("a")]), Sentence([], [Word("b")])
    sequence.add_sentence(first)
    sequence.add_sentence(second)
    assert len(sequence) == 2
    assert sequence[1] is second
    assert list(sequence) == [first, second]


async def test_empty_sequence_executes_nothing():
    session = Session()
    await SentenceSequence(session).execute()


async def test_sequence_executes_sentences(capsys):
    session = Session()
    sequence = SentenceSequence(session)
    sequence.add_sentence(Sentence([], [Word("echo"), Word("hi")]))
    await sequence.execute()
    assert capsys.readouterr().out == "hi\n"


async def test_global_assignment_changes_session():
    stream = MemoryStream()
    session = Session()
    sentence = Sentence([Assignment("X", Word("Y"))], [])
    assert session.get("X") == ""
    await sentence.execute(session, stream, stream)
    assert session.get("X") == "Y"
    assert os.environ.get("X") == "Y"


async def test_local_assignment_not_changes_session():
    os.environ["X"] = ""
    stream = MemoryStream()
    session = Session()
    sentence = Sentence([Assignment("X", Word("Y"))], [Word("echo"), Word("hi")])
    assert session.get("X") == ""
    await sentence.execute(session, stream, stream)
    assert session.get("X") == ""
    assert os.environ.get("X") == ""
    assert stream.buffer.getvalue() == "hi\n"
