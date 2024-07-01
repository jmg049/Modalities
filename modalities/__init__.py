"""
This module defines the `Modality` enum class, representing different types of modalities.
It allows for predefined modalities such as 'image', 'text', 'audio', and 'multimodal'.
Additionally, it supports adding new user-defined modalities dynamically using the `add_modality` function.

Classes:
    Modality: An enum class representing different modalities.

Functions:
    Modality.from_str(s: str): Converts a string to the corresponding Modality enum member.
    add_modality(name: str, value: Any): Dynamically adds a new modality to the Modality enum.

Example usage:
    # Convert string to Modality enum member
    print(Modality.from_str("image"))  # Outputs: Modality.IMAGE

    # Add a new user-defined modality
    add_modality("VIDEO", "video")
    print(Modality.from_str("video"))  # Outputs: Modality.VIDEO

    # Check if the new modality is part of Modality enum
    print(Modality.VIDEO)  # Outputs: Modality.VIDEO
    print(Modality.VIDEO in Modality)  # Outputs: True
"""

__all__ = ["Modality", "add_modality"]

from enum import Enum
from typing import Any
from aenum import extend_enum
import pytest


class Modality(Enum):
    """
    An enum class representing different modalities.

    Attributes:
        IMAGE (str): Represents the 'image' modality.
        TEXT (str): Represents the 'text' modality.
        AUDIO (str): Represents the 'audio' modality.
        MULTIMODAL (str): Represents the 'multimodal' modality.
        INVALID (None): Represents an invalid modality.
    """

    IMAGE = "image"
    TEXT = "text"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"
    INVALID = None

    @staticmethod
    def from_str(s: str):
        """
        Converts a string to the corresponding Modality enum member.

        Args:
            s (str): The string representation of the modality.

        Returns:
            Modality: The corresponding Modality enum member if found,
                      otherwise Modality.INVALID.
        """
        _s = s.lower()
        for modality in Modality:
            if modality.value == _s:
                return modality
        return Modality.INVALID


def add_modality(name: str, value: Any):
    """
    Dynamically adds a new modality to the Modality enum.

    Args:
        name (str): The name of the new modality to add.
        value (Any): The value of the new modality to add.

    Raises:
        ValueError: If the modality name or value already exists.

    Example:
        add_modality("VIDEO", "video")
        print(Modality.from_str("video"))  # Outputs: Modality.VIDEO
    """
    lower_name = name.lower()
    lower_value = value.lower() if isinstance(value, str) else value
    if lower_name in Modality.__members__ or any(
        mod.value == lower_value for mod in Modality
    ):
        raise ValueError(f"'{name}' or value '{value}' already exists as a modality.")
    extend_enum(Modality, name, value)


def test_predefined_modalities():
    assert (
        Modality.from_str("image") == Modality.IMAGE
    ), "Failed to match 'image' to Modality.IMAGE"
    assert (
        Modality.from_str("text") == Modality.TEXT
    ), "Failed to match 'text' to Modality.TEXT"
    assert (
        Modality.from_str("audio") == Modality.AUDIO
    ), "Failed to match 'audio' to Modality.AUDIO"
    assert (
        Modality.from_str("multimodal") == Modality.MULTIMODAL
    ), "Failed to match 'multimodal' to Modality.MULTIMODAL"
    assert (
        Modality.from_str("unknown") == Modality.INVALID
    ), "Failed to match 'unknown' to Modality.INVALID"


def test_add_user_modality():
    add_modality("VIDEO", "video")
    assert (
        Modality.from_str("video") == Modality.VIDEO
    ), "Failed to match 'video' to dynamically added Modality.VIDEO"
    assert Modality.VIDEO in Modality, "'video' not found in Modality enum after adding"


def test_add_duplicate_modality():
    with pytest.raises(ValueError, match="already exists as a modality"):
        add_modality("IMAGE", "image")
    with pytest.raises(ValueError, match="already exists as a modality"):
        add_modality("VIDEO", "video")


def test_invalid_modality():
    assert (
        Modality.from_str("invalid") == Modality.INVALID
    ), "Failed to match 'invalid' to Modality.INVALID"


def test_case_insensitivity():
    assert (
        Modality.from_str("IMAGE") == Modality.IMAGE
    ), "Failed to match 'IMAGE' to Modality.IMAGE (case-insensitive)"
    assert (
        Modality.from_str("Text") == Modality.TEXT
    ), "Failed to match 'Text' to Modality.TEXT (case-insensitive)"


def test_new_modality():
    add_modality("NEWMODALITY", "newmodality")
    assert (
        Modality.from_str("newmodality") == Modality.NEWMODALITY
    ), "Failed to match 'newmodality' to dynamically added Modality.NEWMODALITY"
    assert (
        Modality.NEWMODALITY in Modality
    ), "'newmodality' not found in Modality enum after adding"


# Example usage
if __name__ == "__main__":
    add_modality("VIDEO", "video")
    print(Modality.from_str("video"))  # Outputs: Modality.VIDEO
    print(Modality.from_str("image"))  # Outputs: Modality.IMAGE
    print(Modality.from_str("unknown"))  # Outputs: Modality.INVALID

    # Check the new modality is a part of Modality enum
    print(Modality.VIDEO)  # Outputs: Modality.VIDEO
    print(Modality.VIDEO in Modality)  # Outputs: True

    pytest.main()
