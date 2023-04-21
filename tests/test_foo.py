from ssh_dispatch.foo import foo


def test_foo():
    assert foo() == "foo"
