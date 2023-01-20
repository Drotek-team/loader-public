from .report import Contenor, Displayer


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


def test_contenor_standard_case():
    dummy_contenor = Contenor("Dummy contenor")
    dummy_contenor.add_error_message(Displayer("one"))
    dummy_contenor.add_error_message(Displayer("two"))
    dummier_contenor = Contenor("Dummier contenor")
    dummier_contenor.add_error_message(Displayer("three"))
    dummier_contenor.add_error_message(Displayer("four"))
    dummy_contenor.add_error_message(dummier_contenor)
    a = "[Contenor] Dummy contenor \n"
    b = " [Displayer] one \n"
    c = " [Displayer] two \n"
    d = " [Contenor] Dummier contenor \n"
    e = "  [Displayer] three \n"
    f = "  [Displayer] four \n"
    assert dummy_contenor.display_message(0, " ") == a + b + c + d + e + f
    assert not (dummy_contenor.user_validation)
    dummy_contenor["one"]._validation = True  # type:ignore[for the sack of the test]
    assert dummy_contenor.display_message(0, " ") == a + c + d + e + f
    assert not (dummy_contenor.user_validation)
    dummy_contenor["two"]._validation = True  # type:ignore[for the sack of the test]
    assert dummy_contenor.display_message(0, " ") == a + d + e + f
    assert not (dummy_contenor.user_validation)
    dummy_contenor["Dummier contenor"]["three"]._validation = True  # type: ignore[test env]
    assert dummy_contenor.display_message(0, " ") == a + d + f
    assert not (dummy_contenor.user_validation)
    dummy_contenor["Dummier contenor"]["four"]._validation = True  # type: ignore[test env]
    assert dummy_contenor.display_message(0, " ") == ""
    assert dummy_contenor.user_validation
