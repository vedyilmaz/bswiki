from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label = "Username", min_length=4, max_length=50)
    password = forms.CharField(label = "Password", min_length=6, widget=forms.PasswordInput)
    confirm = forms.CharField(label = "Confirm Password", min_length=6, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords not matching!")

        values = {
            "username" : username,
            "password" : password
        }
        return values


class LoginForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget=forms.PasswordInput)
    