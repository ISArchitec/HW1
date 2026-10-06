import os

from sentence import Assignment, Sentence, SentenceSequence, Word
from tests.helpers import MemoryStream
from utils.session import Session


async def test_sentence_executes_command():
    session = Session()
    out = MemoryStream()
    await Sentence([], [Word("echo"), Word("hi")]).execute(session, MemoryStream(), out)
    assert out.buffer.getvalue() == "hi\n"


async def test_empty_sequence_executes_nothing():
    session = Session()
    await SentenceSequence(session).execute()


async def test_sequence_executes_sentences(capsys):
    session = Session()
    sequence = SentenceSequence(session)
    sequence.add_sentence(Sentence([], [Word("echo"), Word("hi")]))
    await sequence.execute()
    assert capsys.readouterr().out == "hi\n"


async def test_global_assignment_changes_session(monkeypatch):
    monkeypatch.setenv("X", "before")
    stream = MemoryStream()
    session = Session()
    sentence = Sentence([Assignment("X", Word("Y"))], [])
    assert session.get("X") == ""
    await sentence.execute(session, stream, stream)
    assert session.get("X") == "Y"
    assert os.environ.get("X") == "Y"


async def test_local_assignment_not_changes_session(monkeypatch):
    monkeypatch.setenv("X", "")
    stream = MemoryStream()
    session = Session()
    sentence = Sentence([Assignment("X", Word("Y"))], [Word("echo"), Word("hi")])
    assert session.get("X") == ""
    await sentence.execute(session, stream, stream)
    assert session.get("X") == ""
    assert os.environ.get("X") == ""
    assert stream.buffer.getvalue() == "hi\n"


def test_session_copy_is_independent():
    session = Session()
    session.set("X", "original")
    copied = session.copy()
    assert copied.get("X") == "original"
    copied.set("X", "changed")
    assert session.get("X") == "original"


async def test_local_assignment_preserves_existing_session(monkeypatch):
    monkeypatch.setenv("X", "system")
    session = Session()
    session.set("X", "session")
    stream = MemoryStream()
    await Sentence([Assignment("X", Word("local"))], [Word("echo")]).execute(
        session, stream, stream
    )
    assert session.get("X") == "session"
    assert os.environ["X"] == "system"
