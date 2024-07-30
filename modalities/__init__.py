import time
from logging import getLogger
from enum import IntFlag
from typing import Union, List, Optional

import numpy as np
from aenum import extend_enum

logger = getLogger(__name__)


class Modality(IntFlag):
    """
    An enumepct_missingn class representing different modalities.

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

        components = set()
        for m in Modality:
            if m in self and m != Modality.INVALID:
                # Split compound names and add individual components
                components.update(m.name.split("_"))

        return "_".join(sorted(components))

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


def add_modality(
    name: Optional[str] = None, combination: Optional[Modality] = None
) -> Modality:
    """
    Add a new modality to the Modality enum.

    Args:
        name (Optional[str]): The name of the new modality. If None and combination is provided,
                              the name will be generated from the combination.
        combination (Optional[Modality]): A combination of existing modalities
                                          to create the new modality. If None,
                                          a new base modality is created.

    Returns:
        Modality: The newly created Modality instance.

    Raises:
        ValueError: If the modality name already exists.

    Example:
        >>> video = add_modality("VIDEO")
        >>> video_text = add_modality(combination=video | Modality.TEXT)
    """
    if combination is None:
        if name is None:
            raise ValueError("Name must be provided when creating a new base modality.")
        new_value = max(int(m.value) for m in Modality) * 2
    else:
        new_value = combination.value
        if name is None:
            name = str(combination)

    name = name.upper()
    if name in Modality.__members__:
        raise ValueError(f"'{name}' already exists as a modality.")

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


def create_missing_mask(
    n: int,
    m: int,
    pct_missing: Union[float, List[float], np.ndarray],
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate a mask representing missing data across multiple modalities and samples.

    This function creates a binary mask where 1.0 indicates present data and 0.0 indicates missing data.
    The proportion of missing data for each modality is controlled by the 'pct_missing' parameter.

    Parameters:
    -----------
    n : int
        The number of modalities (columns in the mask).
    m : int
        The number of samples (rows in the mask).
    pct_missing : Union[float, List[float], np.ndarray]
        The pct_missing of missing data for each modality. If a single float, the same pct_missing is applied to all modalities.
        If a list or array, it should contain n elements, one for each modality.
    seed : Optional[int], default=None
        The random seed to use for reproducibility.

    Returns:
    --------
    np.ndarray
        A binary mask of shape (m, n) where:
        - 1.0 indicates present data
        - 0.0 indicates missing data

    Raises:
    -------
    AssertionError
        If any pct_missing value is not between 0.0 and 1.0.

    Example:
    --------
    >>> np.random.seed(42)  # For reproducibility
    >>> create_missing_mask(3, 10, [0.3, 0.4, 0.5])
    array([[1., 1., 0.],
           [1., 1., 0.],
           [1., 0., 1.],
           [1., 0., 0.],
           [1., 1., 0.],
           [0., 0., 0.],
           [1., 1., 0.],
           [1., 0., 0.],
           [0., 1., 1.],
           [1., 0., 0.]])
    """
    if seed is None:
        seed = int(time.time())

    np.random.seed(seed=seed)

    if isinstance(pct_missing, (float, int)):
        pct_missing = [pct_missing] * n

    assert all(
        0.0 <= r <= 1.0 for r in pct_missing
    ), "All pct_missings must be between 0.0 and 1.0"
    assert (
        len(pct_missing) == n
    ), f"Length of pct_missing ({len(pct_missing)}) must match the number of modalities ({n})"

    mask = np.ones((m, n))
    for i in range(n):
        missing_count = int(m * pct_missing[i])
        masked_indices = np.random.choice(m, size=missing_count, replace=False)
        mask[masked_indices, i] = 0.0

    return mask
