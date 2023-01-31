from src.editor import export_show_user_to_iostar_json_gcs_string
from src.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def main():
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2))
    iostar_json_string = export_show_user_to_iostar_json_gcs_string(show_user)
    f = open("iostar_json_gcs_reference.json", "w")
    f.write(iostar_json_string)
    f.close()


if __name__ == "__main__":
    main()
