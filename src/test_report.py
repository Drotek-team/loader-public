from .report import *


def test_displayer_standard_case():
    displayer = Displayer(name="test")
    assert displayer.name == "test"
    assert not (displayer.user_validation)
    assert displayer.display_message(0, " ") == "[Displayer] test \n"
    displayer.update_annexe_message(annexe_message="annexe")
    assert displayer.display_message(0, " ") == "[Displayer] test:annexe \n"
    assert displayer.display_message(1, " ") == " [Displayer] test:annexe \n"
    assert displayer.display_message(1, "*") == "*[Displayer] test:annexe \n"
    assert displayer != Displayer(name="test")
    displayer.validate()
    assert displayer.display_message(0, " ") == ""


def test_displayer_list_standard_case():
    first_displayer = Displayer(name="first")
    second_displayer = Displayer(name="second")
    displayer_list = ErrorMessageList(
        name="test list", error_messages=[first_displayer, second_displayer]
    )
    assert not (displayer_list.user_validation)
    a = "[Error Message List] test list \n"
    b = " [Displayer] first \n"
    c = " [Displayer] second \n"
    assert displayer_list.display_message(0, " ") == a + b + c
    displayer_list[0]._validation = True  # type: ignore[this is just a test]
    assert not (displayer_list.user_validation)
    assert displayer_list.display_message(0, " ") == a + c
    displayer_list[1]._validation = True  # type: ignore[this is just a test]
    assert displayer_list.user_validation
    assert displayer_list.display_message(0, " ") == ""


class DummyContenor(Contenor):
    def __init__(self):
        self.name = "contenor name"
        self.first_displayer = Displayer(name="one")
        self.second_displayer = Displayer(name="two")
        self.displayer_list = ErrorMessageList(
            "list", [Displayer(name="three"), Displayer(name="four")]
        )


def test_contenor_standard_case():
    contenor = DummyContenor()
    a = "[Contenor] contenor name \n"
    b = " [Displayer] one \n"
    c = " [Displayer] two \n"
    d = " [Error Message List] list \n"
    e = "  [Displayer] three \n"
    f = "  [Displayer] four \n"
    assert contenor.display_message(0, " ") == a + b + c + d + e + f
    assert not (contenor.user_validation)
    contenor.first_displayer.validate()
    assert contenor.display_message(0, " ") == a + c + d + e + f
    assert not (contenor.user_validation)
    contenor.second_displayer.validate()
    assert contenor.display_message(0, " ") == a + d + e + f
    assert not (contenor.user_validation)
    contenor.displayer_list[0]._validation = True  # type: ignore[this is just a test]
    assert contenor.display_message(0, " ") == a + d + f
    assert not (contenor.user_validation)
    contenor.displayer_list[1]._validation = True  # type: ignore[this is just a test]
    assert contenor.display_message(0, " ") == ""
    assert contenor.user_validation
