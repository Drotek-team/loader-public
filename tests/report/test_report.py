import json

from loader.report.report import Contenor, Displayer


def test_displayer_standard_case() -> None:
    displayer = Displayer(name="test")
    assert displayer.name == "test"
    assert not (displayer.user_validation)
    assert displayer.display_message() == "[Displayer] test \n"
    displayer.update_annexe_message(annexe_message="annexe")
    assert displayer.display_message() == "[Displayer] test:annexe \n"
    assert displayer.display_message(1) == " [Displayer] test:annexe \n"
    assert displayer != Displayer(name="test")
    displayer.validate()
    assert displayer.display_message() == ""


def test_contenor_display_message_standard_case() -> None:
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
    assert dummy_contenor.display_message() == a + b + c + d + e + f
    assert not (dummy_contenor.user_validation)

    dummy_contenor["one"]._validation = True  # pyright: ignore[reportGeneralTypeIssues]
    assert dummy_contenor.display_message() == a + c + d + e + f
    assert not (dummy_contenor.user_validation)

    dummy_contenor["two"]._validation = True  # pyright: ignore[reportGeneralTypeIssues]
    assert dummy_contenor.display_message() == a + d + e + f
    assert not (dummy_contenor.user_validation)

    dummy_contenor["Dummier contenor"]["three"]._validation = True  # pyright: ignore
    assert dummy_contenor.display_message() == a + d + f
    assert not (dummy_contenor.user_validation)

    dummy_contenor["Dummier contenor"]["four"]._validation = True  # pyright: ignore
    assert dummy_contenor.display_message() == ""
    assert dummy_contenor.user_validation


def test_contenor_get_json_standard_case() -> None:
    dummy_contenor = Contenor("Dummy contenor")
    dummy_contenor.add_error_message(Displayer("one"))
    dummy_contenor.add_error_message(Displayer("two"))
    dummier_contenor = Contenor("Dummier contenor")
    dummier_contenor.add_error_message(Displayer("three"))
    dummier_contenor.add_error_message(Displayer("four"))
    dummy_contenor.add_error_message(dummier_contenor)
    returned_json = {
        "Dummy contenor": [
            {"one": ""},
            {"two": ""},
            {
                "Dummier contenor": [{"three": ""}, {"four": ""}],
            },
        ],
    }
    assert dummy_contenor.get_json() == returned_json
    assert json.loads(json.dumps(returned_json)) == returned_json
    assert not (dummy_contenor.user_validation)

    dummy_contenor["one"]._validation = True  # pyright: ignore[reportGeneralTypeIssues]
    returned_json["Dummy contenor"] = returned_json["Dummy contenor"][1:]
    assert dummy_contenor.get_json() == returned_json
    assert not (dummy_contenor.user_validation)

    dummy_contenor["two"]._validation = True  # pyright: ignore[reportGeneralTypeIssues]
    returned_json["Dummy contenor"] = returned_json["Dummy contenor"][1:]
    assert dummy_contenor.get_json() == returned_json
    assert not (dummy_contenor.user_validation)

    dummy_contenor["Dummier contenor"][
        "three"
    ]._validation = True  # pyright: ignore[reportGeneralTypeIssues]
    returned_json["Dummy contenor"][0][
        "Dummier contenor"
    ] = returned_json[  # pyright: ignore[reportGeneralTypeIssues]
        "Dummy contenor"
    ][
        0
    ][
        "Dummier contenor"
    ][
        1:
    ]
    assert dummy_contenor.get_json() == returned_json
    assert not (dummy_contenor.user_validation)

    dummy_contenor["Dummier contenor"]["four"]._validation = True  # pyright: ignore
    assert dummy_contenor.get_json() == {}
    assert dummy_contenor.user_validation
