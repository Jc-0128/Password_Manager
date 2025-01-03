import json
from project import (
    PasswordManager,
    generate_password,
    save_data,
    load_data,
    generate_key,
    get_key,
    encrypt,
    decrypt,
    clear_screen,
)


def test_add():
    pm = PasswordManager()
    result = pm.add("TEST1")
    assert result == "TEST1 is added"
    assert "TEST1" in pm.passwords

    result = pm.add("TEST1")
    assert result == "TEST1 already exists."


def test_get():
    pm = PasswordManager()
    pm.add("TEST1")
    result = pm.get("TEST1")
    assert result == pm.passwords["TEST1"]

    result = pm.get("TEST2")
    assert result == "TEST2 not found."


def test_remove(monkeypatch):
    pm = PasswordManager()
    pm.add("TEST1")
    monkeypatch.setattr("builtins.input", lambda _: "no")
    result = pm.remove("TEST1")
    assert result == "Operation is canceled"

    monkeypatch.setattr("builtins.input", lambda _: "yes")
    result = pm.remove("TEST1")
    assert result not in pm.passwords

    non = pm.remove("NON")
    assert non == "NON not found"


def test_generate_password():
    result = generate_password()
    assert type(result) == str
    assert len(result) == 16


def test_save_load_data():
    data = {"USER": "PASSWORD"}
    save_data(json.dumps(data).encode())
    load = load_data()
    result = json.loads(load.decode())
    assert result == data


def test_generate_get_key():
    generate_key()
    key = get_key()
    assert len(key) > 0
    assert type(key) == bytes


def test_encrypt_decrypt():
    data = {"USER": "PASSWORD"}
    encrypted = encrypt(data)
    assert encrypted != data

    decrypted = decrypt(encrypted)
    assert decrypted == data


def test_clear_screen(monkeypatch):
    monkeypatch.setattr("os.system", lambda x: "clear")
    clear_screen()
