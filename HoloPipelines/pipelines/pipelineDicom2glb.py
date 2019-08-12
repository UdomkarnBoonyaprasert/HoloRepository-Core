from components import compCommonPath
from components import compDicom2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
import pathlib
import sys
import logging


def main(dicomFolderPath, outputGlbPath, threshold):
    generatedNumpyList = compDicom2numpy.main(str(pathlib.Path(dicomFolderPath)))
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        threshold,
        str(
            compCommonPath.obj.joinpath(
                str(pathlib.PurePath(dicomFolderPath).parts[-1])
            )
        )
        + ".obj",
    )
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath, outputGlbPath, deleteOriginalObj=True, compressGlb=False
    )
    logging.info("dicom2glb: done, glb saved to {}".format(generatedGlbPath))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
