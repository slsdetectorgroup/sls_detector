#ifndef DETECTOR_H
#define DETECTOR_H
#include <iostream>
#include <cstdint>
#include <string>
#include <vector>

#include <stdexcept>

#include "sls_receiver_defs.h"
#include "sls_detector_defs.h"
#include "slsDetectorUtils.h"
#include "multiSlsDetector.h"
#include "slsDetector.h"
#include "error_defs.h"

class Detector{
public:
    Detector(int i):det(i){

        //id of the multi detector instance
        multi_detector_id = i;

        //Disable any output from std::cout
        std::cout.setstate(std::ios_base::failbit);

    }

    int getMultiDetectorId(){ return multi_detector_id; }

    //get image size as [nrow, ncols] return as a pair of ints
    std::pair<int, int> getImageSize(){
        std::pair<int, int> image_size{0,0};
        image_size.first = det.getMaxNumberOfChannelsPerDetector(slsDetectorDefs::dimension::Y);
        image_size.second = det.getMaxNumberOfChannelsPerDetector(slsDetectorDefs::dimension::X);
        return image_size;
    }

    void setImageSize(const int rows, const int cols){
        det.setMaxNumberOfChannelsPerDetector(slsDetectorDefs::dimension::Y, rows);
        det.setMaxNumberOfChannelsPerDetector(slsDetectorDefs::dimension::X, cols);
    }

    //blocking command, acquire set number of frames
    void acquire(){ det.acquire(); }


    //for Eiger check status of  the module
    //true active false deactivated
    bool getActive(const int i){
        return getSlsDetector(i)->activate();
    }
    //activate or deactivate a module
    void setActive(const int i, const bool value){
        getSlsDetector(i)->activate(value);
    }

    int getFramesCaughtByReceiver(){
        return det.getFramesCaughtByReceiver();
    }
    int getFramesCaughtByReceiverSingleDetector(const int i){
        return getSlsDetector(i)->getFramesCaughtByReceiver();

    }

    void resetFramesCaught(){
        det.resetFramesCaught();
    }

    int getReceiverCurrentFrameIndex(){
        return det.getReceiverCurrentFrameIndex();
    }

    bool getThreadedProcessing(){
        return det.setThreadedProcessing();
    }
    void setThreadedProcessing(const bool value){
        det.setThreadedProcessing(value);
    }

    void startReceiver(){ det.startReceiver(); }
    void stopReceiver(){ det.stopReceiver(); }

    bool getTenGigabitEthernet(){
        return det.enableTenGigabitEthernet();
    }
    void setTenGigabitEthernet(const bool value){
        det.enableTenGigabitEthernet(value);
    }

    int getFileFormat(){
        return det.getFileFormat();
    }

    std::string checkOnline(){
       return det.checkOnline();
    }

    void clearErrorMask(){
        det.clearAllErrorMask();
    }

    int64_t getErrorMask(){
        return det.getErrorMask();
    }
    void setErrorMask(const int64_t i){
        det.setErrorMask(i);
    }

    std::string getErrorMessage(){
        //tmp would hold the number of critical errors, is and should this be used?
        int tmp=0;
        return det.getErrorMessage(tmp);
    }

    bool getReceiverOnline(){
        return det.setReceiverOnline();
    }
    void setReceiverOnline(const bool status){
        det.setReceiverOnline(status);
    }

    bool getOnline(){
        return det.setOnline();
    }
    void setOnline(const bool status){
        det.setOnline(status);
    }


    bool isChipPowered(){
        return det.powerChip();
    }
    void powerChip(const bool value){
        det.powerChip(value);
    }


    //read register from readout system, used for low level control
    int readRegister(const int addr){
        return det.readRegister(addr);
    }

    //directly write to register in readout system
    void writeRegister(const int addr, const int value){
        det.writeRegister(addr, value);
    }

    //directly write to the ADC register
    void writeAdcRegister(const int addr, const int value){
        det.writeAdcRegister(addr, value);
    }

    bool getAcquiringFlag(){
        return det.getAcquiringFlag();
    }

    void setAcquiringFlag(const bool flag){
        det.setAcquiringFlag(flag);
    }

    bool getCounterBit(){
        return det.setCounterBit();
    }
    void setCounterBit(bool b){
        det.setCounterBit(b);
    }

    slsDetectorDefs::dacIndex dacNameToEnum(std::string dac_name);

    std::pair<int, int> getDetectorGeometry(){
        std::pair<int, int> g;
        det.getNumberOfDetectors(g.first, g.second);
        return g;
    }

    int getNumberOfDetectors(){
        return det.getNumberOfDetectors();
    }

    std::string getRunStatus(){
        auto s = det.getRunStatus();
        return det.runStatusType(s);
    }


    void startAcquisition(){ det.startAcquisition(); }
    void stopAcquisition(){ det.stopAcquisition(); }

    std::string getHostname(){
        return det.getHostname();
    }

    void setHostname(std::string hostname){
        det.setHostname(hostname.c_str());
    }
    
    int getDynamicRange(){
        return det.setDynamicRange(-1);
    }
    void setDynamicRange(const int dr){
        det.setDynamicRange(dr);
    }

    void pulseChip(const int n){ det.pulseChip(n); }
    void pulseAllPixels(const int n);
    void pulseDiagonal(const int n);

    void readConfigurationFile(std::string fname){ det.readConfigurationFile(fname);}
    void readParametersFile(std::string fname){ det.retrieveDetectorSetup(fname); }
    int getReadoutClockSpeed(){ return det.setSpeed(slsDetectorDefs::CLOCK_DIVIDER, -1); }

    int getFirmwareVersion(){ return det.getId(slsDetectorDefs::DETECTOR_FIRMWARE_VERSION); }
    int getSoftwareVersion(){ return det.getId(slsDetectorDefs::DETECTOR_SOFTWARE_VERSION); }

    int getDetectorNumber(const int i){
        return getSlsDetector(i)->getId(slsDetectorDefs::DETECTOR_SERIAL_NUMBER);
    }

    void setReadoutClockSpeed(const int speed){
        det.setSpeed(slsDetectorDefs::CLOCK_DIVIDER, speed);
    }

    int getRxTcpport(const int i){
        return getSlsDetector(i)->setPort(slsDetectorDefs::portType::DATA_PORT);
    }

    void setRxTcpport(const int i, const int value){
         getSlsDetector(i)->setPort(slsDetectorDefs::portType::DATA_PORT, value);
    }

    void setRateCorrection(std::vector<double> tau){
        for (int i=0; i<det.getNumberOfDetectors(); ++i)
            getSlsDetector(i)->setRateCorrection(tau[i]);
    }

    std::vector<double>getRateCorrection();

    bool getFlippedDataX(const int i){
        return getSlsDetector(i)->getFlippedData(slsDetectorDefs::dimension::X);
    }

    bool getFlippedDataY(const int i){
        return getSlsDetector(i)->getFlippedData(slsDetectorDefs::dimension::Y);
    }

    void setFlippedDataX(const int i, const bool value){
        getSlsDetector(i)->setFlippedData(slsDetectorDefs::dimension::X, value);
    }
    void setFlippedDataY(const int i, const bool value){
        getSlsDetector(i)->setFlippedData(slsDetectorDefs::dimension::Y, value);
    }

    //----------------------------------------------------File
    void setFileName(std::string fname){ det.setFileName(fname); }
   
    std::string getFileName(){
        return det.getFileName();
    }

    void setFilePath(std::string path){ det.setFilePath(path); }
    
    std::string getFilePath(){
        return det.getFilePath();
    }


    void loadTrimbitFile(std::string fname, const int idet){
        det.loadSettingsFile(fname, idet);
    }

    //Eiger: set the energies where the detector is trimmed
    void setTrimEnergies(std::vector<int> energy){
        det.setTrimEn(energy.size(), energy.data());
    }

    std::vector<int> getTrimEnergies(){
        //initial call to get legth, energies defaults to NULL
        auto n_trimen = det.getTrimEn();
        std::vector<int> trim_energies(n_trimen);

        //second call to get the energies
        det.getTrimEn(trim_energies.data());
        return trim_energies;
    }



    /*** Temperature control functions for Jungfrau ***/
    void setThresholdTemperature(float t){
        det.setThresholdTemperature(static_cast<int>(t*1000), -1);
    }

    float getThresholdTemperature(){
        return static_cast<float>(det.setThresholdTemperature(-1,-1))/1000.0;
    }

    void setTemperatureControl(bool v){
        det.setTemperatureControl(v);
    }
    bool getTemperatureControl(){
        return det.setTemperatureControl();
    }

    bool getTemperatureEvent(){
        return det.setTemperatureEvent();
    }
    void resetTemperatureEvent(){
        det.setTemperatureEvent(0);
    }
    /*** END Temperature control functions for Jungfrau ***/



    void setThresholdEnergy(const int eV){
        det.setThresholdEnergy(eV);
    }

    std::string getSettingsDir(){ return det.getSettingsDir(); }
    void setSettingsDir(std::string dir){ det.setSettingsDir(dir); }

    int getThresholdEnergy(){
        return det.getThresholdEnergy();
    }

    std::string getSettings(){
        return det.getDetectorSettings(det.getSettings());
    }

    void setSettings(std::string s){
        det.setSettings(det.getDetectorSettings(s));
    }

    //name to enum translation on the c++ side
    //should we instead expose the enum to Python?
    dacs_t getDac(std::string dac_name, const int mod_id){
        dacs_t val = -1;
        auto dac = dacNameToEnum(dac_name);
        return det.setDAC(val, dac, 0, mod_id);
    }

    void setDac(std::string dac_name, const int mod_id, dacs_t val){
        auto dac = dacNameToEnum(dac_name);
        det.setDAC(val, dac, 0, mod_id);
    }

    //Calling multi do we have a need to lock/unlock a single det?
    bool getServerLock(){ return det.lockServer(-1); }
    void setServerLock(const bool value){ det.lockServer(value); }
    bool getReceiverLock(){ return det.lockReceiver(-1); }
    void setReceiverLock(const bool value){ det.lockReceiver(value); }

    dacs_t getAdc(std::string adc_name, int mod_id){
        auto adc = dacNameToEnum(adc_name);
        return det.getADC(adc, mod_id);

    }

    std::vector<std::string> getReadoutFlags();

    //note singular
    void setReadoutFlag(const string flag_name);

    //name to enum transltion of dac
    dacs_t getDacVthreshold(){
        dacs_t val = -1;
        auto dac = slsDetectorDefs::dacIndex::THRESHOLD;
        return det.setDAC(val, dac, 0, -1);
    }
    
    void setDacVthreshold(const dacs_t val){
        auto dac = slsDetectorDefs::dacIndex::THRESHOLD;
        det.setDAC(val, dac, 0, -1);
    }


    void setFileIndex(const int i){ det.setFileIndex(i); }
    int getFileIndex(){
        return det.setFileIndex(-1);
    }

    //time in ns
    void setExposureTime(const int64_t t){
        det.setTimer(slsReceiverDefs::timerIndex::ACQUISITION_TIME, t);
    }

    //time in ns
    int64_t getExposureTime(){
        return det.setTimer(slsReceiverDefs::timerIndex::ACQUISITION_TIME, -1);
    }

    void setSubExposureTime(const int64_t t){
        det.setTimer(slsReceiverDefs::timerIndex::SUBFRAME_ACQUISITION_TIME, t);
    }

    int64_t getSubExposureTime(){
        //time in ns
        return det.setTimer(slsReceiverDefs::timerIndex::SUBFRAME_ACQUISITION_TIME, -1);
    }

    int64_t getCycles(){
        return det.setTimer(slsReceiverDefs::timerIndex::CYCLES_NUMBER, -1);
    }

    void setCycles(const int64_t n_cycles){
        det.setTimer(slsReceiverDefs::timerIndex::CYCLES_NUMBER, n_cycles);
    }

    void setNumberOfMeasurements(const int n_measurements){
        det.setTimer(slsReceiverDefs::timerIndex::MEASUREMENTS_NUMBER, n_measurements);
    }
    int getNumberOfMeasurements(){
        return det.setTimer(slsReceiverDefs::timerIndex::MEASUREMENTS_NUMBER, -1);
    }


    int getNumberOfGates(){
        return det.setTimer(slsReceiverDefs::timerIndex::GATES_NUMBER, -1);
    }
    void setNumberOfGates(const int t){
        det.setTimer(slsReceiverDefs::timerIndex::GATES_NUMBER, t);
    }
    int getNumberOfProbes(){
        return det.setTimer(slsReceiverDefs::timerIndex::PROBES_NUMBER, -1);
    }
    void setNumberOfProbes(const int t){
        det.setTimer(slsReceiverDefs::timerIndex::PROBES_NUMBER, t);
    }
    //time in ns
    int64_t getDelay(){
        return det.setTimer(slsReceiverDefs::timerIndex::DELAY_AFTER_TRIGGER, -1);
    }
    //time in ns
    void setDelay(const int64_t t){
        det.setTimer(slsReceiverDefs::timerIndex::DELAY_AFTER_TRIGGER, t);
    }
    //time in ns
    int64_t getPeriod(){
        return det.setTimer(slsReceiverDefs::timerIndex::FRAME_PERIOD, -1);
    }
    //time in ns
    void setPeriod(const int64_t t){
        det.setTimer(slsReceiverDefs::timerIndex::FRAME_PERIOD, t);
    }

    int64_t getNumberOfFrames(){
        return det.setTimer(slsReceiverDefs::timerIndex::FRAME_NUMBER, -1);
    }

    void setNumberOfFrames(const int64_t nframes){
        det.setTimer(slsReceiverDefs::timerIndex::FRAME_NUMBER, nframes);
    }

    std::string getTimingMode(){
        return det.externalCommunicationType(det.setExternalCommunicationMode());
    }
    void setTimingMode(const std::string mode){
        det.setExternalCommunicationMode(det.externalCommunicationType(mode));
    }

    void freeSharedMemory(){
        det.freeSharedMemory();
    }

    std::vector<std::string> getDetectorType(){
        std::vector<std::string> detector_type;
        for (int i=0; i<det.getNumberOfDetectors(); ++i){
            detector_type.push_back(det.sgetDetectorsType(i));
        }
        return detector_type;
    }



    void setFileWrite(const bool value){
        det.enableWriteToFile(value);
    }
    bool getFileWrite(){
        return det.enableWriteToFile(-1);
    }
    void setAllTrimbits(int tb){
        det.setAllTrimbits(tb);
    }
    int getAllTrimbits(){
        return det.setAllTrimbits(-1);
    }
    bool getRxDataStreamStatus(){
        return det.enableDataStreamingFromReceiver();
    }
    
    void setRxDataStreamStatus(bool state){
        det.enableDataStreamingFromReceiver(state);
    }
    
    //Get a network parameter for all detectors, looping over individual detectors
    //return a vector of strings
    std::vector<std::string> getNetworkParameter(std::string par_name){
        auto p = networkNameToEnum(par_name);
        std::vector<std::string> par;
        for (int i=0; i<det.getNumberOfDetectors(); ++i){
            par.push_back(getSlsDetector(i)->getNetworkParameter(p));
        }
        return par;
    }

    //Set network parameter for all modules if det_id == -1 otherwise the module
    //specified with det_id.
    void setNetworkParameter(std::string par_name, std::string par, const int det_id){
        auto p = networkNameToEnum(par_name);
        if (det_id == -1){
            det.setNetworkParameter(p, par);
        }else{
            getSlsDetector(det_id)->setNetworkParameter(p, par);
        }
    }

    void configureNetworkParameters(){ det.configureMAC(); }

    std::string getLastClientIP(){
        return det.getLastClientIP();
    }


    //get frame delay of module (det_id) in ns
    int getDelayFrame(const int det_id){
        auto r = getSlsDetector(det_id)->getNetworkParameter(slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_FRAME);
        return std::stoi(r);
    }
    //set frame delay of module (det_id) in ns
    void setDelayFrame(const int det_id, const int delay){
        auto delay_str = std::to_string(delay);
        getSlsDetector(det_id)->setNetworkParameter(slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_FRAME, delay_str);
    }

    //get delay left of module (det_id) in ns
    int getDelayLeft(const int det_id){
        auto r = getSlsDetector(det_id)->getNetworkParameter(slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_LEFT);
        return std::stoi(r);
    }
    //set delay left of module (det_id) in ns
    void setDelayLeft(const int det_id, const int delay){
        auto delay_str = std::to_string(delay);
        getSlsDetector(det_id)->setNetworkParameter(slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_LEFT, delay_str);
    }

    //get delay right of module (det_id) in ns
    int getDelayRight(const int det_id){
        auto r = getSlsDetector(det_id)->getNetworkParameter(slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_RIGHT);
        return std::stoi(r);
    }

    //set delay right of module (det_id) in ns
    void setDelayRight(const int det_id, const int delay){
        auto delay_str = std::to_string(delay);
        getSlsDetector(det_id)->setNetworkParameter(slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_RIGHT, delay_str);
    }


    //Check if detector if filling in gap pixels in module
    //return true if so, currently only in developer
    bool getGapPixels(){
        throw std::runtime_error("gap pixels only in develop");
//        return det.enableGapPixels(-1);
    }


    //Set to true to have the detector filling in gap pixels
    //false to disable, currently only in developer
    void setGapPixels(bool val){
        throw std::runtime_error("gap pixels only in develop");
//        det.enableGapPixels(val);
    }

    slsDetectorDefs::networkParameter networkNameToEnum(std::string par_name);

private:
    multiSlsDetector det;
    slsDetector* getSlsDetector(int i);
    int multi_detector_id = 0;
};


slsDetector* Detector::getSlsDetector(int i){
    //Get a pointer to an slsDetector
    //throw an exception to avoid accessing
    //a null pointer
    const auto d =  det(i);
    if(d)
        return d;
    else
        throw std::runtime_error("Could not get detector: " + std::to_string(i));
}

slsDetectorDefs::networkParameter Detector::networkNameToEnum(std::string par_name){

    if(par_name == "detectormac"){
        return slsDetectorDefs::networkParameter::DETECTOR_MAC;
    }
    else if(par_name == "detectorip"){
        return slsDetectorDefs::networkParameter::DETECTOR_IP;
    }
    else if(par_name == "rx_hostname"){
        return slsDetectorDefs::networkParameter::RECEIVER_HOSTNAME;
    }
    else if(par_name == "rx_udpip"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_IP;
    }
    else if(par_name == "rx_udpport"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_PORT;
    }
    else if(par_name == "rx_udpmac"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_MAC;
    }
    else if(par_name == "rx_udpport2"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_PORT2;
    }
    else if(par_name == "delay_left"){
        return slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_LEFT;
    }
    else if(par_name == "delay_right"){
        return slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_RIGHT;
    }
    else if(par_name == "delay_frame"){
        return slsDetectorDefs::networkParameter::DETECTOR_TXN_DELAY_FRAME;
    }
    else if(par_name == "flow_control_10g"){
        return slsDetectorDefs::networkParameter::FLOW_CONTROL_10G;
    }
    else if(par_name == "client_zmqport"){
        return slsDetectorDefs::networkParameter::CLIENT_STREAMING_PORT;
    }
    else if(par_name == "rx_zmqport"){
        return slsDetectorDefs::networkParameter::RECEIVER_STREAMING_PORT;
    }
    else if(par_name == "rx_zmqip"){
        throw std::runtime_error("rx_zmqip only in developer");
//        return slsDetectorDefs::networkParameter::RECEIVER_STREAMING_SRC_IP;
    }
    
    return slsDetectorDefs::networkParameter::RECEIVER_STREAMING_PORT;
};

slsDetectorDefs::dacIndex Detector::dacNameToEnum(std::string dac_name){
    //to avoid unitialised
    slsDetectorDefs::dacIndex dac = slsDetectorDefs::dacIndex::E_SvP;
    if(dac_name == std::string("vsvp")){
        dac = slsDetectorDefs::dacIndex::E_SvP;
    }
    else if(dac_name == "vtr"){
        dac = slsDetectorDefs::dacIndex::E_Vtr;
    }
    else if(dac_name == "vthreshold"){
        dac = slsDetectorDefs::dacIndex::THRESHOLD;
    }
    else if(dac_name == "vrf"){
        dac = slsDetectorDefs::dacIndex::E_Vrf;
    }
    else if(dac_name == "vrs"){
        dac = slsDetectorDefs::dacIndex::E_Vrs;
    }
    else if(dac_name == "vsvn"){
        dac = slsDetectorDefs::dacIndex::E_SvN;
    }
    else if(dac_name == "vtgstv"){
        dac = slsDetectorDefs::dacIndex::E_Vtgstv;
    }
    else if(dac_name == "vcmp_ll"){
        dac = slsDetectorDefs::dacIndex::E_Vcmp_ll;
    }
    else if(dac_name == "vcmp_lr"){
        dac = slsDetectorDefs::dacIndex::E_Vcmp_lr;
    }
    else if(dac_name == "vcall"){
        dac = slsDetectorDefs::dacIndex::E_cal;
    }
    else if(dac_name == "vcmp_rl"){
        dac = slsDetectorDefs::dacIndex::E_Vcmp_rl;
    }
    else if(dac_name == "rxb_rb"){
        dac = slsDetectorDefs::dacIndex::E_rxb_rb;
    }
    else if(dac_name == "rxb_lb"){
        dac = slsDetectorDefs::dacIndex::E_rxb_lb;
    }
    else if(dac_name == "vcmp_rr"){
        dac = slsDetectorDefs::dacIndex::E_Vcmp_rr;
    }
    else if(dac_name == "vcp"){
        dac = slsDetectorDefs::dacIndex::E_Vcp;
    }
    else if(dac_name == "vcn"){
        dac = slsDetectorDefs::dacIndex::E_Vcn;
    }
    else if(dac_name == "vis"){
        dac = slsDetectorDefs::dacIndex::E_Vis;
    }
    else if(dac_name == "iodelay"){
        dac = slsDetectorDefs::dacIndex::IO_DELAY;
    }
    else if(dac_name == "temp_fpga"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_FPGA;
    }
    else if(dac_name == "temp_fpgaext"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_FPGAEXT;
    }
    else if(dac_name == "temp_10ge"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_10GE;
    }
    else if(dac_name == "temp_dcdc"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_DCDC;
    }
    else if(dac_name == "temp_sodl"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_SODL;
    }
    else if(dac_name == "temp_sodr"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_SODR;
    }
    else if(dac_name == "temp_fpgafl"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_FPGA2;
    }
    else if(dac_name == "temp_fpgafr"){
        dac = slsDetectorDefs::dacIndex::TEMPERATURE_FPGA3;
    }
    else if(dac_name == "vhighvoltage"){
        dac = slsDetectorDefs::dacIndex::HV_NEW;
    }
    else if(dac_name == "vb_comp"){
        dac = static_cast<slsDetectorDefs::dacIndex>(0);
    }
    else if(dac_name == "vdd_prot"){
        dac = static_cast<slsDetectorDefs::dacIndex>(1);
    }
    else if(dac_name == "vin_com"){
        dac = static_cast<slsDetectorDefs::dacIndex>(2);
    }
    else if(dac_name == "vref_prech"){
        dac = static_cast<slsDetectorDefs::dacIndex>(3);
    }
    else if(dac_name == "vb_pixbuff"){
        dac = static_cast<slsDetectorDefs::dacIndex>(4);
    }
    else if(dac_name == "vb_ds"){
        dac = static_cast<slsDetectorDefs::dacIndex>(5);
    }
    else if(dac_name == "vref_ds"){
        dac = static_cast<slsDetectorDefs::dacIndex>(6);
    }
    else if(dac_name == "vref_comp"){
        dac = static_cast<slsDetectorDefs::dacIndex>(7);
    }


    return dac;

}


std::vector<std::string> Detector::getReadoutFlags(){
    std::vector<std::string> flags;
    auto r = det.setReadOutFlags();
    if(r & slsDetectorDefs::readOutFlags::STORE_IN_RAM)
        flags.push_back("storeinram");
    if(r & slsDetectorDefs::readOutFlags::TOT_MODE)
        flags.push_back("tot");
    if(r & slsDetectorDefs::readOutFlags::CONTINOUS_RO)
        flags.push_back("continous");
    if(r & slsDetectorDefs::readOutFlags::PARALLEL)
        flags.push_back("parallel");
    if(r & slsDetectorDefs::readOutFlags::NONPARALLEL)
        flags.push_back("nonparallel");
    if(r & slsDetectorDefs::readOutFlags::SAFE)
        flags.push_back("safe");
    if(r & slsDetectorDefs::readOutFlags::DIGITAL_ONLY)
        flags.push_back("digital");
    if(r & slsDetectorDefs::readOutFlags::ANALOG_AND_DIGITAL)
        flags.push_back("analog_digital");

    return flags;
}

//note singular
void Detector::setReadoutFlag(const string flag_name){
    if(flag_name == "none")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::NORMAL_READOUT);
    else if(flag_name == "storeinram")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::STORE_IN_RAM);
    else if(flag_name == "tot")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::TOT_MODE);
    else if(flag_name == "continous")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::CONTINOUS_RO);
    else if(flag_name == "parallel")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::PARALLEL);
    else if(flag_name == "nonparallel")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::NONPARALLEL);
    else if(flag_name == "safe")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::SAFE);
    else if(flag_name == "digital")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::DIGITAL_ONLY);
    else if(flag_name == "analog_digital")
        det.setReadOutFlags(slsDetectorDefs::readOutFlags::ANALOG_AND_DIGITAL);
    else
        throw std::runtime_error("Flag name not recognized");

}

std::vector<double> Detector::getRateCorrection(){
    std::vector<double> rate_corr;
    double tmp = 0;
    for (int i=0; i<det.getNumberOfDetectors(); ++i){
        getSlsDetector(i)->getRateCorrection(tmp);
        rate_corr.push_back(tmp);
    }
    return rate_corr;
}

void Detector::pulseAllPixels(int n){
//  int pulsePixelNMove(int n=0,int x=0,int y=0);
//  int pulsePixel(int n=0,int x=0,int y=0);

    for (int j=0; j<8; ++j){
        det.pulsePixel(0, -255+j, 0);
        for (int i=0; i<256; ++i){
            det.pulsePixelNMove(n, 0, 1);
        }
    }
    return;
}
void Detector::pulseDiagonal(int n){
//  int pulsePixelNMove(int n=0,int x=0,int y=0);
//  int pulsePixel(int n=0,int x=0,int y=0);

    for (int j=20; j<232; j+=16){
        det.pulsePixel(0, -255, j);
        for (int i=0; i<8; ++i){
            det.pulsePixelNMove(n, 1, 1);
        }
    }
    return;
}


#endif // DETECTOR_H
