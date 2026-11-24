from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Select a crop image",
        widget=forms.FileInput(attrs={'accept': 'image/jpeg,image/png'}),
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')

    # 10MB due to smartphones' high res images
        max_size = 10 * 1024 * 1024

        if image.size > max_size:
            raise forms.ValidationError(
                "Image size must not exceed 10 MB."
            )

        return image