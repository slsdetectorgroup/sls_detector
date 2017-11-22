#ifndef DETECTOR_H
#define DETECTOR_H
#include <iostream>
#include <cstdint>
#include <string>
#include <vector>

#include "sls_receiver_defs.h"
#include "sls_detector_defs.h"
#include "slsDetectorUtils.h"
#include "multiSlsDetector.h"
#include "slsDetector.h"

class Detector{
public:
    Detector():det(){
        det.setOnline(slsDetectorDefs::ONLINE_FLAG);
        det.setReceiverOnline(slsDetectorDefs::ONLINE_FLAG);

        //Disable any output from std::cout
        std::cout.setstate(std::ios_base::failbit);

    }

    std::pair<int, int> getImageSize(){
        //image size in [rows, cols]
        std::pair<int, int> image_size{0,0};
        image_size.first = det.getMaxNumberOfChannelsPerDetector(slsDetectorDefs::dimension::Y);
        image_size.second = det.getMaxNumberOfChannelsPerDetector(slsDetectorDefs::dimension::X);
        return image_size;
    }

    void acquire(){ det.acquire(); }

    std::string checkOnline(){
       std::string r = det.checkOnline();
       return r;
    }

    bool getAcquiringFlag(){
        return det.getAcquiringFlag();
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
    
    int getDynamicRange(){
        return det.setDynamicRange(-1);
    }
    void setDynamicRange(int dr){
        det.setDynamicRange(dr);
    }

    void pulseChip(int n){ det.pulseChip(n); }

    void readConfigurationFile(std::string fname){ det.readConfigurationFile(fname);}
    void readParametersFile(std::string fname){ det.retrieveDetectorSetup(fname); }
    int getReadoutClockSpeed(){ return det.setSpeed(slsDetectorDefs::CLOCK_DIVIDER, -1); }

    int getFirmwareVersion(){ return det.getId(slsDetectorDefs::DETECTOR_FIRMWARE_VERSION); }
    int getSoftwareVersion(){  return det.getId(slsDetectorDefs::DETECTOR_SOFTWARE_VERSION); }

    void setReadoutClockSpeed(int speed){
        det.setSpeed(slsDetectorDefs::CLOCK_DIVIDER, speed);
    }

    void setRateCorrection(std::vector<double> tau){
        slsDetector* _d;
        for (int i=0; i<det.getNumberOfDetectors(); ++i){
            _d = det.getSlsDetector(i);
            _d->setRateCorrection(tau[i]);
        }

    }

    std::vector<double>getRateCorrection(){
        std::vector<double> rate_corr;
        slsDetector* _d;
        for (int i=0; i<det.getNumberOfDetectors(); ++i){
            _d = det.getSlsDetector(i);
            std::pair<int, double> r = {0,0};
            r.first = _d->getRateCorrection(r.second);
            rate_corr.push_back(r.second);
        }
        return rate_corr;
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


    //name to enum translation on the c++ side
    //should we instead expose the enum to Python?
    dacs_t getDac(std::string dac_name, int mod_id){
        dacs_t val = -1;
        auto dac = dacNameToEnum(dac_name);
        return det.setDAC(val, dac, 0, mod_id);
    }

    void setDac(std::string dac_name, int mod_id, dacs_t val){
        auto dac = dacNameToEnum(dac_name);
        det.setDAC(val, dac, 0, mod_id);
    }




    dacs_t getAdc(std::string adc_name, int mod_id){
        auto adc = dacNameToEnum(adc_name);
        return det.getADC(adc, mod_id);

    }

    //name to enum transltion of dac
    dacs_t getDacVthreshold(){
        dacs_t val = -1;
        auto dac = slsDetectorDefs::dacIndex::THRESHOLD;
        return det.setDAC(val, dac, 0, -1);
    }
    
    void setDacVthreshold(dacs_t val){
        auto dac = slsDetectorDefs::dacIndex::THRESHOLD;
        det.setDAC(val, dac, 0, -1);
    }

    //dacs_t multiSlsDetector::setDAC(dacs_t val, dacIndex idac, int mV, int imod)

    void setFileIndex(int i){ det.setFileIndex(i); }
    int getFileIndex(){
        return det.setFileIndex(-1);
    }


    void setExposureTime(int64_t t){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::ACQUISITION_TIME;
        det.setTimer(timer, t);
    }
    int64_t getExposureTime(){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::ACQUISITION_TIME;
        return det.setTimer(timer, -1);
    }

    void setSubExposureTime(int64_t t){
        auto timer = slsReceiverDefs::timerIndex::SUBFRAME_ACQUISITION_TIME;
        det.setTimer(timer, t);
    }
    int64_t getSubExposureTime(){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::SUBFRAME_ACQUISITION_TIME;
        return det.setTimer(timer, -1);
    }

    std::string getTimingMode(){
        return det.externalCommunicationType(det.setExternalCommunicationMode());
    }
    void setTimingMode(std::string mode){
        det.setExternalCommunicationMode(det.externalCommunicationType(mode));
    }

    void freeSharedMemory(){ det.freeSharedMemory(); }

    std::string getDetectorType(){
        return det.ssetDetectorsType();
    }

    int64_t getPeriod(){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::FRAME_PERIOD;
        return det.setTimer(timer, -1);
    }
    void setPeriod(int64_t t){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::FRAME_PERIOD;
        det.setTimer(timer, t);
    }
    int64_t getNumberOfFrames(){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::FRAME_NUMBER;
        return det.setTimer(timer, -1);
    }
    void setNumberOfFrames(int64_t nframes){
        //time in ns
        auto timer = slsReceiverDefs::timerIndex::FRAME_NUMBER;
        det.setTimer(timer, nframes);
    }

    void setFileWrite(bool value){
        if (value == true)
            det.enableWriteToFile(1);
        else
            det.enableWriteToFile(0);
    }

    bool getFileWrite(){
        auto r = det.enableWriteToFile(-1);
        if (r==1)
            return true;
        else
            return false;
    }


    void setAllTrimbits(int tb){
        det.setAllTrimbits(tb);
    }

    int getAllTrimbits(){
        return det.setAllTrimbits(-1);
    }
    
    bool getRxDataStreamStatus(){
        auto i = det.enableDataStreamingFromReceiver();
        if(i==0)
            return false;
        else
            return true;
    }
    
    void setRxDataStreamStatus(bool state){
        det.enableDataStreamingFromReceiver(state);
    }
    
    std::string getNetworkParameter(std::string par_name){
        auto p = networkNameToEnum(par_name);
        return det.getNetworkParameter(p);  
    }

    slsDetectorDefs::networkParameter networkNameToEnum(std::string par_name);
private:
    multiSlsDetector det;
};


//enum networkParameter {
//  DETECTOR_MAC, 	    	/**< detector MAC */
//  DETECTOR_IP,	 	    	/**< detector IP */
//  RECEIVER_HOSTNAME,  		/**< receiver IP/hostname */
//  RECEIVER_UDP_IP,			/**< receiever UDP IP */
//  RECEIVER_UDP_PORT,		/**< receiever UDP Port */
//  RECEIVER_UDP_MAC,			/**< receiever UDP MAC */
//  RECEIVER_UDP_PORT2,		/**< receiever UDP Port of second half module for eiger */
//  DETECTOR_TXN_DELAY_LEFT, 	/**< transmission delay on the (left) port for next frame */
//  DETECTOR_TXN_DELAY_RIGHT,	/**< transmission delay on the right port for next frame  */
//  DETECTOR_TXN_DELAY_FRAME, /**< transmission delay of a whole frame for all the ports */
//  FLOW_CONTROL_10G,			/**< flow control for 10GbE */
//  FLOW_CONTROL_WR_PTR,		/**< memory write pointer for flow control */
//  FLOW_CONTROL_RD_PTR,		/**< memory read pointer for flow control */
//  RECEIVER_STREAMING_PORT,	/**< receiever streaming TCP(ZMQ) port */
//  CLIENT_STREAMING_PORT,	/**< client streaming TCP(ZMQ) port */
//  RECEIVER_STREAMING_SRC_IP,/**< receiever streaming TCP(ZMQ) ip */
//  CLIENT_STREAMING_SRC_IP	/**< client streaming TCP(ZMQ) ip */
//};

slsDetectorDefs::networkParameter Detector::networkNameToEnum(std::string par_name){

    if(par_name == "detector_mac"){
        return slsDetectorDefs::networkParameter::DETECTOR_MAC;
    }
    else if(par_name == "detector_ip"){
        return slsDetectorDefs::networkParameter::DETECTOR_IP;
    }
    else if(par_name == "rx_hostname"){
        return slsDetectorDefs::networkParameter::RECEIVER_HOSTNAME;
    }
    else if(par_name == "rx_udpip"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_IP;
    }
    else if(par_name == "rx_updport"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_PORT;
    }
    else if(par_name == "rx_udpmac"){
        return slsDetectorDefs::networkParameter::RECEIVER_UDP_MAC;
    }
    else if(par_name == "rx_updport2"){
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
        return slsDetectorDefs::networkParameter::RECEIVER_STREAMING_SRC_IP;
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
    else if(dac_name == "temp_10gr"){
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
    return dac;

}






#endif // DETECTOR_H
