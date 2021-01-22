from django import forms


class loginUserForm(forms.Form):

    email = forms.CharField(label="email", widget=forms.TextInput(attrs={
        'placeholder' : 'email',
        'class' : "form-control"
    }))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        'class' : "form-control"
    }))


class signupUserForm(forms.Form):

    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={
        'placeholder' : 'Email',
        'class' : "form-control"
    }))    

    userName = forms.CharField(label="User Name", widget=forms.TextInput(attrs={
        'placeholder' : 'User Name',
        'class' : "form-control"
    }))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',
        'class' : "form-control"
    }))

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password',
        'class' : "form-control"
    }))

    # for cleaneing data after pass didnt same
    def clean(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data