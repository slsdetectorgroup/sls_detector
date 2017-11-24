#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Detector.h"


namespace py = pybind11;

PYBIND11_MODULE(_sls_detector, m) {
    m.doc() = R"pbdoc(
        C/C++ API
        -----------------------
        .. warning ::

            This is the compiled c extension. You probably want to look at the
            interface provided by sls instead.

    )pbdoc";

    py::class_<Detector> DetectorApi(m, "DetectorApi");
    DetectorApi
            .def(py::init<>())
            .def("freeSharedMemory", &Detector::freeSharedMemory)
            .def("acq", &Detector::acquire, "Acqire")
            .def("getAcquiringFlag", &Detector::getAcquiringFlag)
            .def("setAllTrimbits", &Detector::setAllTrimbits)
            .def("getAllTrimbits", &Detector::getAllTrimbits)
            .def("setCounterBit", &Detector::setCounterBit)
            .def("getCounterBit", &Detector::getCounterBit)

            .def("getAdc", &Detector::getAdc)
            .def("getDac", &Detector::getDac)
            .def("setDac", &Detector::setDac)
            

            .def("pulseChip", &Detector::pulseChip)
            .def("pulseAllPixels", &Detector::pulseAllPixels)
            .def("getRunStatus", &Detector::getRunStatus)
            .def("readConfigurationFile", &Detector::readConfigurationFile)
            .def("readParametersFile", &Detector::readParametersFile)
            .def("checkOnline", &Detector::checkOnline)
            .def("setReadoutClockSpeed", &Detector::setReadoutClockSpeed)
            .def("getReadoutClockSpeed", &Detector::getReadoutClockSpeed)
            .def("getHostname", &Detector::getHostname)
            .def("setDynamicRange", &Detector::setDynamicRange)
            .def("getDynamicRange", &Detector::getDynamicRange)
            .def("getFirmwareVersion", &Detector::getFirmwareVersion)
            .def("getSoftwareVersion", &Detector::getSoftwareVersion)
            .def("getRateCorrection", &Detector::getRateCorrection)
            .def("setRateCorrection", &Detector::setRateCorrection)
            .def("startAcquisition", &Detector::startAcquisition)
            .def("stopAcquisition", &Detector::stopAcquisition)
            .def("getFilePath", &Detector::getFilePath)
            .def("setFilePath", &Detector::setFilePath)
            .def("setFileName", &Detector::setFileName)
            .def("getFileName", &Detector::getFileName)
            .def("setFileIndex", &Detector::setFileIndex)
            .def("getFileIndex", &Detector::getFileIndex)

            .def("setExposureTime", &Detector::setExposureTime)
            .def("getExposureTime", &Detector::getExposureTime)
            .def("setSubExposureTime", &Detector::setSubExposureTime)
            .def("getSubExposureTime", &Detector::getSubExposureTime)
            .def("setPeriod", &Detector::setPeriod)
            .def("getPeriod", &Detector::getPeriod)

            .def("getTimingMode", &Detector::getTimingMode)
            .def("setTimingMode", &Detector::setTimingMode)

            .def("getDetectorType", &Detector::getDetectorType)


            .def("getRxDataStreamStatus", &Detector::getRxDataStreamStatus)
            .def("setRxDataStreamStatus", &Detector::setRxDataStreamStatus)
            
            .def("getNetworkParameter", &Detector::getNetworkParameter)


            .def("setFileWrite", &Detector::setFileWrite)
            .def("getFileWrite", &Detector::getFileWrite)
            .def("getDacVthreshold", &Detector::getDacVthreshold)
            .def("setDacVthreshold", &Detector::setDacVthreshold)
            .def("setNumberOfFrames", &Detector::setNumberOfFrames)
            .def("getNumberOfFrames", &Detector::getNumberOfFrames)
            .def("getImageSize", &Detector::getImageSize)
            .def("getNumberOfDetectors", &Detector::getNumberOfDetectors)
            .def("getDetectorGeometry", &Detector::getDetectorGeometry);



#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
