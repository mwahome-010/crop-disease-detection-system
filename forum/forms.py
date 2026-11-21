from django import forms
from .models import ForumPost, Comment, Reply


class ForumPostForm(forms.ModelForm):
    new_flair = forms.CharField(
        required=False,
        max_length=30,
        label="Create a new flair",
        help_text="Optional. Enter a new category, up to 30 characters."
    )

    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'image', 'flair']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter your question or discussion title'
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describe your crop problem or share your experience'
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image and image.size > 10 * 1024 * 1024:
            raise forms.ValidationError(
                'The image must not exceed 10 MB.'
            )

        return image

    def clean(self):
        cleaned_data = super().clean()

        selected_flair = cleaned_data.get('flair')
        new_flair = cleaned_data.get('new_flair', '').strip()

        if selected_flair and new_flair:
            raise forms.ValidationError(
                'Select an existing flair OR create a new one, not both.'
            )

        cleaned_data['new_flair'] = new_flair

        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write your reply...'
            }),
        }