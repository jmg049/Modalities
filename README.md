# Modality Enum

This module defines the `Modality` enum class, which represents different types of modalities and provides functionality for adding new modalities dynamically.

## Installation
So there already exists a project on PyPi with the name ``modalities``. They provide very little information and it appears to install a lot of dependencies. For now I will avoid publishing on PyPI.

```bash
git clone https://github.com/jmg049/Modalities.git && pip install ./Modalities
```

## Overview

The `Modality` enum class includes predefined modalities such as 'image', 'text', 'audio', and 'multimodal'. It also supports adding new user-defined modalities using the `add_modality` function.

### Classes

- **Modality**: An enum class representing different modalities.

### Functions

- **Modality.from_str(s: str) -> Modality**: Converts a string to the corresponding Modality enum member.
- **add_modality(name: str, value: Any)**: Dynamically adds a new modality to the Modality enum.

## Example Usage

```python
# Convert string to Modality enum member
print(Modality.from_str("image"))  # Outputs: Modality.IMAGE

# Add a new user-defined modality
add_modality("VIDEO", "video")
print(Modality.from_str("video"))  # Outputs: Modality.VIDEO

# Check if the new modality is part of Modality enum
print(Modality.VIDEO)  # Outputs: Modality.VIDEO
print(Modality.VIDEO in Modality)  # Outputs: True
