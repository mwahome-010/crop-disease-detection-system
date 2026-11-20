from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Select a crop image",
        help_text="Upload a JPG, JPEG, PNG or other supported image."
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')

        max_size = 5 * 1024 * 1024  # 5 MB

        if image.size > max_size:
            raise forms.ValidationError(
                "Image size must not exceed 5 MB."
            )

        return image