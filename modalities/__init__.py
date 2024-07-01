from logging import getLogger
from enum import IntFlag
from aenum import extend_enum
from typing import Optional


logger = getLogger(__name__)


class Modality(IntFlag):
    """
    An enumeration class representing different modalities.

    This class uses the IntFlag enum to allow for combinations of modalities.
    Predefined modalities include IMAGE, TEXT, AUDIO, and MULTIMODAL.
    Additional modalities can be added using the add_modality function.

    Attributes:
        IMAGE (Modality): Represents image modality.
        TEXT (Modality): Represents text modality.
        AUDIO (Modality): Represents audio modality.
        MULTIMODAL (Modality): Represents a combination of multiple modalities.
        INVALID (Modality): Represents an invalid modality.

    Methods:
        from_str: Create a Modality instance from a string representation.
        __str__: Return a string representation of the Modality.
        __or__: Combine two Modality instances using bitwise OR.
        __add__: Combine two Modality instances (alias for __or__).
    """

    IMAGE = 1
    TEXT = 2
    AUDIO = 4
    MULTIMODAL = 8
    INVALID = 0

    @staticmethod
    def from_str(s: str) -> "Modality":
        """
        Create a Modality instance from a string representation.

        Args:
            s (str): A string representation of the modality or modalities,
                     separated by underscores (e.g., "IMAGE_TEXT").

        Returns:
            Modality: The corresponding Modality instance.

        Example:
            >>> Modality.from_str("IMAGE_TEXT")
            <Modality.IMAGE|TEXT: 3>
        """
        modalities = [m.strip().upper() for m in s.split("_")]
        result = Modality(0)
        for m in modalities:
            try:
                result |= Modality[m]
            except KeyError:
                return Modality.INVALID
        return result if result != Modality.INVALID else Modality.INVALID

    def __str__(self) -> str:
        """
        Return a string representation of the Modality.

        Returns:
            str: A string representation of the Modality.

        Example:
            >>> str(Modality.IMAGE | Modality.TEXT)
            'IMAGE_TEXT'
        """
        if self == Modality.INVALID:
            return "INVALID"
        return "_".join(
            sorted(m.name for m in Modality if m in self and m != Modality.INVALID)
        )

    def __or__(self, other: "Modality") -> "Modality":
        """
        Combine two Modality instances using bitwise OR.

        Args:
            other (Modality): Another Modality instance to combine with.

        Returns:
            Modality: A new Modality instance representing the combination.

        Example:
            >>> Modality.IMAGE | Modality.TEXT
            <Modality.IMAGE|TEXT: 3>
        """
        if isinstance(other, Modality):
            return Modality(self.value | other.value)
        return NotImplemented

    def __add__(self, other: "Modality") -> "Modality":
        """
        Combine two Modality instances (alias for __or__).

        Args:
            other (Modality): Another Modality instance to combine with.

        Returns:
            Modality: A new Modality instance representing the combination.

        Example:
            >>> Modality.IMAGE + Modality.TEXT
            <Modality.IMAGE|TEXT: 3>
        """
        return self.__or__(other)

    def __radd__(self, other: "Modality") -> "Modality":
        """
        Support reversed addition.

        Args:
            other (Modality): Another Modality instance to combine with.

        Returns:
            Modality: A new Modality instance representing the combination.
        """
        return self.__add__(other)


# The add_modality function remains the same


def add_modality(name: str, combination: Optional[Modality] = None) -> Modality:
    """
    Add a new modality to the Modality enum.

    Args:
        name (str): The name of the new modality.
        combination (Optional[Modality]): A combination of existing modalities
                                          to create the new modality. If None,
                                          a new base modality is created.

    Returns:
        Modality: The newly created Modality instance.

    Raises:
        ValueError: If the modality name already exists.

    Example:
        >>> video = add_modality("VIDEO")
        >>> video_text = add_modality("VIDEO_TEXT", video | Modality.TEXT)
    """
    name = name.upper()
    if name in Modality.__members__:
        raise ValueError(f"'{name}' already exists as a modality.")

    if combination is None:
        new_value = max(int(m.value) for m in Modality) * 2
    else:
        new_value = combination.value

    new_member = extend_enum(Modality, name, new_value)
    logger.debug(f"Added new modality: {name}")
    return new_member


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
