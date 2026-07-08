from django import forms


class SecretTextField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault(
            'widget',
            forms.PasswordInput(
                attrs={'autocomplete': 'new-password'},
                render_value=True,
            ),
        )
        super().__init__(*args, **kwargs)


class ThemeColorField(forms.RegexField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('regex', r'^#[0-9a-fA-F]{6}$')
        kwargs.setdefault('required', True)
        kwargs.setdefault('max_length', 7)
        kwargs.setdefault('min_length', 7)
        kwargs.setdefault(
            'widget',
            forms.TextInput(attrs={
                'type': 'color',
                'style': 'width: 6rem; height: 2.25rem; padding: 0.15rem;',
            }),
        )
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        return value.lower()
