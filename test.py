from parser import parse


def test_simple_value():
    document = parse("<doctype: web;><title: bonjour;>")
    assert document.doctype.content == "web"
    assert document.title.content == "bonjour"


def test_nested_structure():
    document = parse("<body:{<header:{<h1: lorem ipsum;};<main:{<p: bonjour;};};")
    assert document.body.header.h1 == "lorem ipsum"
    assert document.body.main.p == "bonjour"


def test_heredoc_parsing():
    document = parse("<text: §hello\nworld§;>")
    assert document.text.content == "hello\nworld"


test_simple_value()
test_nested_structure()
test_heredoc_parsing()
print("ok")
