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
            .def("setAcquiringFlag", &Detector::setAcquiringFlag)

            .def("setAllTrimbits", &Detector::setAllTrimbits)
            .def("getAllTrimbits", &Detector::getAllTrimbits)
            .def("setCounterBit", &Detector::setCounterBit)
            .def("getCounterBit", &Detector::getCounterBit)

            .def("getAdc", &Detector::getAdc)
            .def("getDac", &Detector::getDac)
            .def("setDac", &Detector::setDac)

            .def("setThresholdEnergy", &Detector::setThresholdEnergy)
            .def("getThresholdEnergy", &Detector::getThresholdEnergy)

            .def("getSettings", &Detector::getSettings)
            .def("setSettings", &Detector::setSettings)
            .def("getSettingsDir", &Detector::getSettingsDir)
            .def("setSettingsDir", &Detector::setSettingsDir)

            .def("loadTrimbitFile", &Detector::loadTrimbitFile)
            .def("setTrimEnergies", &Detector::setTrimEnergies)
            .def("getTrimEnergies", &Detector::getTrimEnergies)

            .def("pulseChip", &Detector::pulseChip)
            .def("pulseAllPixels", &Detector::pulseAllPixels)
            .def("pulseDiagonal", &Detector::pulseDiagonal)
            .def("getRunStatus", &Detector::getRunStatus)
            .def("readConfigurationFile", &Detector::readConfigurationFile)
            .def("readParametersFile", &Detector::readParametersFile)
            .def("checkOnline", &Detector::checkOnline)
            .def("setReadoutClockSpeed", &Detector::setReadoutClockSpeed)
            .def("getReadoutClockSpeed", &Detector::getReadoutClockSpeed)
            .def("getHostname", &Detector::getHostname)
            .def("setHostname", &Detector::setHostname)

            .def("getOnline", &Detector::getOnline)
            .def("setOnline", &Detector::setOnline)
            .def("getReceiverOnline", &Detector::getReceiverOnline)
            .def("setReceiverOnline", &Detector::setReceiverOnline)

            .def("getRxTcpport", &Detector::getRxTcpport)
            .def("setRxTcpport", &Detector::setRxTcpport)

            .def("isChipPowered", &Detector::isChipPowered)
            .def("powerChip", &Detector::powerChip)

            .def("readRegister", &Detector::readRegister)
            .def("writeRegister", &Detector::writeRegister)
            .def("writeAdcRegister", &Detector::writeAdcRegister)


            .def("setDynamicRange", &Detector::setDynamicRange)
            .def("getDynamicRange", &Detector::getDynamicRange)
            .def("getFirmwareVersion", &Detector::getFirmwareVersion)
            .def("getSoftwareVersion", &Detector::getSoftwareVersion)
            .def("getRateCorrection", &Detector::getRateCorrection)
            .def("setRateCorrection", &Detector::setRateCorrection)

            .def("startAcquisition", &Detector::startAcquisition)
            .def("stopAcquisition", &Detector::stopAcquisition)
            .def("startReceiver", &Detector::startReceiver)
            .def("stopReceiver", &Detector::stopReceiver)
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

            .def("getCycles", &Detector::getCycles)
            .def("setCycles", &Detector::setCycles)

            .def("getTimingMode", &Detector::getTimingMode)
            .def("setTimingMode", &Detector::setTimingMode)

            .def("getDetectorType", &Detector::getDetectorType)


            .def("getRxDataStreamStatus", &Detector::getRxDataStreamStatus)
            .def("setRxDataStreamStatus", &Detector::setRxDataStreamStatus)
            
            .def("getNetworkParameter", &Detector::getNetworkParameter)
            .def("setNetworkParameter", &Detector::setNetworkParameter)
            .def("getDelayFrame", &Detector::getDelayFrame)
            .def("setDelayFrame", &Detector::setDelayFrame)
            .def("getDelayLeft", &Detector::getDelayLeft)
            .def("setDelayLeft", &Detector::setDelayLeft)
            .def("getDelayRight", &Detector::getDelayRight)
            .def("setDelayRight", &Detector::setDelayRight)
            .def("getLastClientIP", &Detector::getLastClientIP)


            .def("setFileWrite", &Detector::setFileWrite)
            .def("getFileWrite", &Detector::getFileWrite)
            .def("getDacVthreshold", &Detector::getDacVthreshold)
            .def("setDacVthreshold", &Detector::setDacVthreshold)
            .def("setNumberOfFrames", &Detector::setNumberOfFrames)
            .def("getNumberOfFrames", &Detector::getNumberOfFrames)
            .def("getFramesCaughtByReceiver", &Detector::getFramesCaughtByReceiver)
            .def("resetFramesCaught", &Detector::resetFramesCaught)
            .def("getReceiverCurrentFrameIndex", &Detector::getReceiverCurrentFrameIndex)
            .def("getGapPixels", &Detector::getGapPixels)
            .def("setGapPixels", &Detector::setGapPixels)

            .def("clearErrorMask", &Detector::clearErrorMask)
            .def("getErrorMask", &Detector::getErrorMask)
            .def("getErrorMessage", &Detector::getErrorMessage)


            .def("getFlippedDataX", &Detector::getFlippedDataX)
            .def("getFlippedDataY", &Detector::getFlippedDataY)
            .def("setFlippedDataX", &Detector::setFlippedDataX)
            .def("setFlippedDataY", &Detector::setFlippedDataY)

            .def("getServerLock", &Detector::getServerLock)
            .def("setServerLock", &Detector::setServerLock)
            .def("getReceiverLock", &Detector::getReceiverLock)
            .def("setReceiverLock", &Detector::setReceiverLock)

            .def("getFileFormat", &Detector::getFileFormat)

            .def("getActive", &Detector::getActive)
            .def("setActive", &Detector::setActive)
            .def("getThreadedProcessing", &Detector::getThreadedProcessing)
            .def("setThreadedProcessing", &Detector::setThreadedProcessing)

            .def("getTenGigabitEthernet", &Detector::getTenGigabitEthernet)
            .def("setTenGigabitEthernet", &Detector::setTenGigabitEthernet)

            .def("getImageSize", &Detector::getImageSize)
            .def("setImageSize", &Detector::setImageSize)
            .def("getNumberOfDetectors", &Detector::getNumberOfDetectors)
            .def("getDetectorGeometry", &Detector::getDetectorGeometry);



#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
