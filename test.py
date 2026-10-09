from parser.parser import parse


def test_simple_value():
    document = parse("<doctype:web;><title:bonjour;>")
    assert document.doctype.value == "web"
    assert document.title.value == "bonjour"


def test_nested_structure():
    document = parse("<body:{<header:{<h1:lorem ipsum;};<main:{<p:bonjour;};};")
    assert document.body.header.h1.value == "lorem ipsum"
    assert document.body.main.p.value == "bonjour"


def test_heredoc_parsing():
    document = parse("<text:§hello\nworld§;>")
    assert document.text.value == "hello\nworld"
