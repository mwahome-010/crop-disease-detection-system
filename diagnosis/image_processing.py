from io import BytesIO
from PIL import Image, ImageOps
from django.core.exceptions import ValidationError


def preprocess_image(uploaded_image):
    try:
        image = Image.open(uploaded_image)

        # Correct image orientation using EXIF information.
        image = ImageOps.exif_transpose(image)

        # Check minimum image dimensions.
        min_width = 100
        min_height = 100

        if image.width < min_width or image.height < min_height:
            raise ValidationError(
                "Image resolution is too low. "
                "Upload an image at least 100 x 100 pixels."
            )

        # Resize large images while preserving proportions.
        image.thumbnail((1024, 1024))

        # Convert to RGB to standardise image processing.
        image = image.convert('RGB')

        # Re-encode into a new image without original EXIF metadata.
        output = BytesIO()
        image.save(output, format='JPEG', quality=85)

        output.seek(0)

        return output

    except (OSError, Image.DecompressionBombError):
        raise ValidationError(
            "The uploaded image could not be processed."
        )