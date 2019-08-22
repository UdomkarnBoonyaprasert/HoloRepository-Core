import logging

import nibabel
import numpy as np
import scipy.ndimage


def extract_np_array_from_nifti_image(image_data: nibabel.nifti1.Nifti1Image):
    """
    Returns the numpy array representation of the dataobj inside a NIfTI image
    :param image_data: NIfTI image
    :return: numpy array representing the image data
    """
    return np.array(image_data.dataobj)


def extract_np_array_from_nifti_image_and_normalise(
    image_data: nibabel.nifti1.Nifti1Image
):
    """
    After loading a NIfTI file, this function resamples it according to the file headers
    in order to compensate different slice thickness.
    :param image_data: input image data
    :return: numpy array representing normalised NIfTI
    """
    image_data_as_np_array = extract_np_array_from_nifti_image(image_data)

    original_shape = image_data_as_np_array.shape[:3]

    # getting slice thickness (z) in relative to x and y from the header data
    spacing = map(
        float,
        (
            [list(image_data.header.get_zooms())[2]]
            + [
                list(image_data.header.get_zooms())[0],
                list(image_data.header.get_zooms())[1],
            ]
        ),
    )
    spacing = np.array(list(spacing))

    # calculate resize factor
    new_spacing = [1, 1, 1]
    resize_factor = spacing / new_spacing
    new_real_shape = original_shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image_data_as_np_array.shape[:3]

    image_data_as_np_array = scipy.ndimage.interpolation.zoom(
        image_data_as_np_array, real_resize_factor
    )

    logging.info("Shape before resampling\t" + repr(original_shape))
    logging.info("Shape after resampling\t" + repr(image_data_as_np_array.shape[:3]))

    return image_data_as_np_array


def read_nifti_image(input_path: str):
    """
    Reads NIfTI image from disk.
    :param input_path: Path to the NIfTI image
    :return: NIfTI image represented as nibabel.nifti1.Nifti1Image
    """
    # Note: Workaround according to https://github.com/nipy/nibabel/issues/626
    nibabel.Nifti1Header.quaternion_threshold = -1e-06
    return nibabel.load(input_path)


def read_nifti_as_np_array_and_normalise(input_path: str):
    nifti_image: nibabel.nifti1.Nifti1Image = read_nifti_image(input_path)
    normalised_nifti_image_as_np_array: np.ndarray = extract_np_array_from_nifti_image_and_normalise(
        nifti_image
    )
    return normalised_nifti_image_as_np_array


def write_nifti_image(nifti_image: nibabel.nifti1.Nifti1Image, output_file_path: str):
    nibabel.save(nifti_image, output_file_path)


def convert_dicom_np_ndarray_to_nifti_image(dicom_image: np.ndarray):
    return nibabel.Nifti1Image(dicom_image, affine=np.eye(4))
