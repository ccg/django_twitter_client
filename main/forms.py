from django import forms

class TwitterForm(forms.Form):
    tweet = forms.CharField(required=True,
                            min_length=1,
                            max_length=140,
                            help_text="140 characters max.",
                            widget=forms.TextInput(attrs={'size': '70'}),
                            # FIXME Hook in some Javascript so the user
                            # can see how many characters are left in the
                            # textarea.
                            #widget=forms.Textarea(attrs={'rows': '2',
                            #                             'cols': '70',
                            #                             'wrap': 'soft'}),
                            )
