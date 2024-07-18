import numpy as np
import math

from numba import njit, prange


@njit
def vec_haversine(
    lat1: np.ndarray, lon1: np.ndarray, lat2: np.ndarray, lon2: np.ndarray
) -> np.ndarray:
    """
    Vectorized haversine distance calculation
    :param lat1: Array of initial latitudes in degrees
    :param lon1: Array of initial longitudes in degrees
    :param lat2: Array of destination latitudes in degrees
    :param lon2: Array of destination longitudes in degrees
    :return: Array of distances in meters
    """
    earth_radius = 6378137.0

    rad_lat1 = np.radians(lat1)
    rad_lon1 = np.radians(lon1)
    rad_lat2 = np.radians(lat2)
    rad_lon2 = np.radians(lon2)

    d_lon = rad_lon2 - rad_lon1
    d_lat = rad_lat2 - rad_lat1

    a = np.sin(d_lat / 2.0) ** 2 + np.multiply(
        np.multiply(np.cos(rad_lat1), np.cos(rad_lat2)), np.sin(d_lon / 2.0) ** 2
    )

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    meters = earth_radius * c
    return meters


@njit
def num_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Haversine distance calculation
    :param lat1: Initial latitude in degrees
    :param lon1: Initial longitude in degrees
    :param lat2: Destination latitude in degrees
    :param lon2: Destination longitude in degrees
    :return: Distances in meters
    """
    earth_radius = 6378137.0

    rad_lat1 = math.radians(lat1)
    rad_lon1 = math.radians(lon1)
    rad_lat2 = math.radians(lat2)
    rad_lon2 = math.radians(lon2)

    d_lon = rad_lon2 - rad_lon1
    d_lat = rad_lat2 - rad_lat1

    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(d_lon / 2.0) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    meters = c * earth_radius
    return meters


@njit()
def outer_haversine(lat1: np.ndarray,
                    lon1: np.ndarray,
                    lat2: np.ndarray,
                    lon2: np.ndarray) -> np.ndarray:
    matrix = np.zeros((lat1.shape[0], lat2.shape[0]))
    for i in prange(lat1.shape[0]):
        matrix[i, :] = vec_haversine(lat2, lon2, lat1[i], lon1[i])
    return matrix
