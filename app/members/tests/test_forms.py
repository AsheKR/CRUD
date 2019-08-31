from model_mommy import mommy

from ..forms import UserCreationForm


class TestUserCreationForm:
    def test_clean_username(self):
        # A user with proto_user params does not exist yet.
        proto_user = mommy.prepare("members.Member")
        proto_user.set_password('password')

        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user.password,
                "password2": proto_user.password,
            }
        )

        assert form.is_valid(), form.errors
        assert form.clean_username() == proto_user.username, form.errors

        # Creating a user.
        form.save()

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user.password,
                "password2": proto_user.password,
            }
        )

        assert not form.is_valid(), form.errors
        assert len(form.errors) == 1, form.errors
        assert "username" in form.errors, form.errors
