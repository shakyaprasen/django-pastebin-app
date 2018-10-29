from django import forms

class PostForm(forms.Form):
    post = forms.CharField(widget=forms.Textarea)

    def send_data(self):

        pass


