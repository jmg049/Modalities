import sys

sys.path.append("..")

from modalities import Modality, add_modality


def process_modality(mod):
    match mod:
        case Modality.INVALID:
            return "Invalid modality"
        case Modality.IMAGE | Modality.TEXT:
            return f"Processing image and text: {mod}"
        case Modality.AUDIO | Modality.TEXT:
            return f"Processing audio and text: {mod}"
        case Modality.IMAGE:
            return f"Processing image only: {mod}"
        case Modality.TEXT:
            return f"Processing text only: {mod}"
        case Modality.VIDEO:
            return f"Processing video: {mod}"
        case _:
            return f"Processing other combination: {mod}"


if __name__ == "__main__":
    # Test basic modality combinations
    print(str(Modality.IMAGE | Modality.TEXT))  # Should print: IMAGE_TEXT
    print(
        str(Modality.TEXT | Modality.IMAGE)
    )  # Should print: IMAGE_TEXT (order shouldn't matter)

    # Test from_str method
    print(
        Modality.from_str("IMAGE_TEXT")
    )  # Should be equal to Modality.IMAGE | Modality.TEXT
    print(
        Modality.from_str("TEXT_IMAGE")
    )  # Should be equal to Modality.IMAGE | Modality.TEXT
    print(
        Modality.from_str("AUDIO_TEXT")
    )  # Should be equal to Modality.AUDIO | Modality.TEXT
    print(Modality.from_str("IMAGE"))  # Should be equal to Modality.IMAGE
    print(Modality.from_str("INVALID"))  # Should be equal to Modality.INVALID

    # Test adding new modalities
    video = add_modality("VIDEO")
    print(str(video))  # Should print: VIDEO
    video_text = add_modality("VIDEO_TEXT", video | Modality.TEXT)
    print(str(video_text))  # Should print: VIDEO_TEXT

    # Test process_modality function
    print(process_modality(Modality.IMAGE | Modality.TEXT))
    print(process_modality(Modality.AUDIO | Modality.TEXT))
    print(process_modality(Modality.IMAGE))
    print(process_modality(Modality.INVALID))
    print(process_modality(Modality.from_str("IMAGE_TEXT")))

    # Test with new combined modalities
    image_text = add_modality("IMAGE_TEXT", Modality.IMAGE | Modality.TEXT)
    print(process_modality(image_text))
    print(process_modality(video_text))
    # Test add_modality with combinations
    image_audio = add_modality("IMAGE_AUDIO", Modality.IMAGE | Modality.AUDIO)
    print(f"New modality: {image_audio}")
    print(
        f"IMAGE_AUDIO == IMAGE | AUDIO: {image_audio == (Modality.IMAGE | Modality.AUDIO)}"
    )

    text_audio_image = add_modality(
        "TEXT_AUDIO_IMAGE", Modality.TEXT | Modality.AUDIO | Modality.IMAGE
    )
    print(f"New modality: {text_audio_image}")
    print(
        f"TEXT_AUDIO_IMAGE == TEXT | AUDIO | IMAGE: {text_audio_image == (Modality.TEXT | Modality.AUDIO | Modality.IMAGE)}"
    )

    # Test using the new combined modalities
    print(process_modality(image_audio))
    print(process_modality(text_audio_image))

    # Test combining existing combined modalities
    super_combo = add_modality("SUPER_COMBO", image_audio | text_audio_image)
    print(f"New modality: {super_combo}")
    print(
        f"SUPER_COMBO == IMAGE_AUDIO | TEXT_AUDIO_IMAGE: {super_combo == (image_audio | text_audio_image)}"
    )
    print(process_modality(super_combo))

    add_modality("VIDEO")
