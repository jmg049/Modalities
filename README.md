# Modality Enum

This module defines the `Modality` enum class, which represents different types of modalities and provides functionality for combining modalities and adding new ones dynamically. It also includes utility functions for working with modalities.

### Why use it?
Across multimodal literature and specifically within the implementations of multimodal models and methods, there is no consistency in matching and acting based on particular modalities. Instead, what we see, is lots the below code block,

```python
if modality == "audio" ...
if modality = "t" ...
if modality == "it" ...
```
where modalities are matched on string literals. This can be easy to misuse (depending on how the code parses the modality) and generally could be conveyed in a more uniform and programmatic way. By representing a modality programmatically we can match modalities or combinations easily using native python syntax, allow for functionality to be extended since enums are just classes, catch errors early and more robustly since the Modality enum will fail on invalid modalities, and also there are simply much more verbose and descriptive. 
```python
## vs
if modality == Modality.AUDIO ...
if modality == Modality.TEXT ...
add_modality("IMAGE_TEXT", Modality.VIDEO | Modality.TEXT) ## required setup

if modality == Modality.IMAGE_TEXT ...
## OR
if modality == Modality.IMAGE | Modality.TEXT ... ## important to not read this as IMAGE or TEXT, but as IMAGE and TEXT. It performs a bitwise OR operation, not the logical OR operation.
```

## Installation

As there already exists a project on PyPi with the name `modalities`, this project is not currently published on PyPI. You can install it directly from the GitHub repository:

```bash
git clone https://github.com/jmg049/Modalities.git && pip install ./Modalities
```

**OR**
```bash
pip install git+https://github.com/jmg049/Modalities.git
```

## Overview
The `Modality` enum class is based on `IntFlag` and includes predefined modalities such as 'IMAGE', 'TEXT', 'AUDIO', and 'MULTIMODAL'. It supports combining modalities using bitwise operations and adding new user-defined modalities.

---
*Disclaimer: I created this package pretty much entirely using ClaudeAI. I described the functionality of what I wanted and when the output of Claude didn't work I just kept providing more and more specific information. I wrote very very little of the final code. I also used it for everything else in the README, this note is the only thing I did. I think this package serves as a good example of where the various LLMs can be used within the programming world. It was a very well defined sepcification, with "strict" requirements imposed on the output of the LLM, and importantly, when it spat out bullshit/generally incorrect behaviour I could tell.*

---


### Classes

- **Modality**: An `IntFlag`-based enum class representing different modalities.

### Methods

- **Modality.from_str(s: str) -> Modality**: Converts a string to the corresponding Modality enum member or combination.
- **Modality.__str__() -> str**: Returns a string representation of the Modality.
- **Modality.__or__(other: Modality) -> Modality**: Combines two Modality instances using bitwise OR.
- **Modality.__add__(other: Modality) -> Modality**: Alias for `__or__`, allowing use of the `+` operator.

### Functions

- **add_modality(name: str, combination: Optional[Modality] = None) -> Modality**: Dynamically adds a new modality to the Modality enum.

## Example Usage

```python
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

    # Test invalid combination
    try:
        invalid_combo = add_modality(
            "IMAGE_TEXT", Modality.IMAGE | Modality.TEXT
        )  # This should raise an error
    except ValueError as e:
        print(f"Caught expected error: {e}")

```

## Utility Functions
The package also includes utility functions for working with modalities:

- **create_missing_mask(n: int, m: int, pct_missing: Union[float, List[float], np.ndarray]) -> np.ndarray**: Generates a binary mask representing missing data across multiple modalities and samples.



## Utility Functions Usage

Here's an example of how to use the `create_missing_mask` function:

```python
import numpy as np
from modalities import create_missing_mask

# Create a missing mask for 2 modalities and 5 samples. 
# Approx. 30% of the data is missing for the first sample and 40% for the second sample.
mask = create_missing_mask(2, 5, [0.3, 0.4])
print(mask)
```

This will output a mask similar to:
```
[[1. 1.]
 [1. 1.]
 [1. 0.]
 [0. 1.]
 [1. 0.]]
```

In this example, we create a mask for 2 modalities and 5 samples, with missing data ratios of 0.3 and 0.4 for the two modalities respectively.


For more detailed usage and examples, refer to the documentation in the source code.

## Reference

If you use this package in your research, please cite it as follows:

```bibtex
@software{jmg_modalities,
  author = {Geraghty, Jack},
  title = {Modalities: A Python Package for Handling Multimodal Data},
  year = {2024},
  url = {https://github.com/jmg049/Modalities},
}
```

## Contributing
If you think of any useful features or changes and wish to contribute please open a pull request and we can discuss it. I always open to collaboration :)

## License
This project is licensed under the MIT License.
