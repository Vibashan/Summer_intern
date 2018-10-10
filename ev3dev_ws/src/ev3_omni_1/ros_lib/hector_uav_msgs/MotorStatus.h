#ifndef _ROS_hector_uav_msgs_MotorStatus_h
#define _ROS_hector_uav_msgs_MotorStatus_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace hector_uav_msgs
{

  class MotorStatus : public ros::Msg
  {
    public:
      typedef std_msgs::Header _header_type;
      _header_type header;
      typedef bool _on_type;
      _on_type on;
      typedef bool _running_type;
      _running_type running;
      uint32_t voltage_length;
      typedef float _voltage_type;
      _voltage_type st_voltage;
      _voltage_type * voltage;
      uint32_t frequency_length;
      typedef float _frequency_type;
      _frequency_type st_frequency;
      _frequency_type * frequency;
      uint32_t current_length;
      typedef float _current_type;
      _current_type st_current;
      _current_type * current;

    MotorStatus():
      header(),
      on(0),
      running(0),
      voltage_length(0), voltage(NULL),
      frequency_length(0), frequency(NULL),
      current_length(0), current(NULL)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        bool real;
        uint8_t base;
      } u_on;
      u_on.real = this->on;
      *(outbuffer + offset + 0) = (u_on.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->on);
      union {
        bool real;
        uint8_t base;
      } u_running;
      u_running.real = this->running;
      *(outbuffer + offset + 0) = (u_running.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->running);
      *(outbuffer + offset + 0) = (this->voltage_length >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->voltage_length >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->voltage_length >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->voltage_length >> (8 * 3)) & 0xFF;
      offset += sizeof(this->voltage_length);
      for( uint32_t i = 0; i < voltage_length; i++){
      union {
        float real;
        uint32_t base;
      } u_voltagei;
      u_voltagei.real = this->voltage[i];
      *(outbuffer + offset + 0) = (u_voltagei.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_voltagei.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_voltagei.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_voltagei.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->voltage[i]);
      }
      *(outbuffer + offset + 0) = (this->frequency_length >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->frequency_length >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->frequency_length >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->frequency_length >> (8 * 3)) & 0xFF;
      offset += sizeof(this->frequency_length);
      for( uint32_t i = 0; i < frequency_length; i++){
      union {
        float real;
        uint32_t base;
      } u_frequencyi;
      u_frequencyi.real = this->frequency[i];
      *(outbuffer + offset + 0) = (u_frequencyi.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_frequencyi.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_frequencyi.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_frequencyi.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->frequency[i]);
      }
      *(outbuffer + offset + 0) = (this->current_length >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->current_length >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->current_length >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->current_length >> (8 * 3)) & 0xFF;
      offset += sizeof(this->current_length);
      for( uint32_t i = 0; i < current_length; i++){
      union {
        float real;
        uint32_t base;
      } u_currenti;
      u_currenti.real = this->current[i];
      *(outbuffer + offset + 0) = (u_currenti.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_currenti.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_currenti.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_currenti.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->current[i]);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        bool real;
        uint8_t base;
      } u_on;
      u_on.base = 0;
      u_on.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->on = u_on.real;
      offset += sizeof(this->on);
      union {
        bool real;
        uint8_t base;
      } u_running;
      u_running.base = 0;
      u_running.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->running = u_running.real;
      offset += sizeof(this->running);
      uint32_t voltage_lengthT = ((uint32_t) (*(inbuffer + offset))); 
      voltage_lengthT |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1); 
      voltage_lengthT |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2); 
      voltage_lengthT |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3); 
      offset += sizeof(this->voltage_length);
      if(voltage_lengthT > voltage_length)
        this->voltage = (float*)realloc(this->voltage, voltage_lengthT * sizeof(float));
      voltage_length = voltage_lengthT;
      for( uint32_t i = 0; i < voltage_length; i++){
      union {
        float real;
        uint32_t base;
      } u_st_voltage;
      u_st_voltage.base = 0;
      u_st_voltage.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_st_voltage.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_st_voltage.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_st_voltage.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->st_voltage = u_st_voltage.real;
      offset += sizeof(this->st_voltage);
        memcpy( &(this->voltage[i]), &(this->st_voltage), sizeof(float));
      }
      uint32_t frequency_lengthT = ((uint32_t) (*(inbuffer + offset))); 
      frequency_lengthT |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1); 
      frequency_lengthT |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2); 
      frequency_lengthT |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3); 
      offset += sizeof(this->frequency_length);
      if(frequency_lengthT > frequency_length)
        this->frequency = (float*)realloc(this->frequency, frequency_lengthT * sizeof(float));
      frequency_length = frequency_lengthT;
      for( uint32_t i = 0; i < frequency_length; i++){
      union {
        float real;
        uint32_t base;
      } u_st_frequency;
      u_st_frequency.base = 0;
      u_st_frequency.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_st_frequency.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_st_frequency.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_st_frequency.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->st_frequency = u_st_frequency.real;
      offset += sizeof(this->st_frequency);
        memcpy( &(this->frequency[i]), &(this->st_frequency), sizeof(float));
      }
      uint32_t current_lengthT = ((uint32_t) (*(inbuffer + offset))); 
      current_lengthT |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1); 
      current_lengthT |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2); 
      current_lengthT |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3); 
      offset += sizeof(this->current_length);
      if(current_lengthT > current_length)
        this->current = (float*)realloc(this->current, current_lengthT * sizeof(float));
      current_length = current_lengthT;
      for( uint32_t i = 0; i < current_length; i++){
      union {
        float real;
        uint32_t base;
      } u_st_current;
      u_st_current.base = 0;
      u_st_current.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_st_current.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_st_current.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_st_current.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->st_current = u_st_current.real;
      offset += sizeof(this->st_current);
        memcpy( &(this->current[i]), &(this->st_current), sizeof(float));
      }
     return offset;
    }

    const char * getType(){ return "hector_uav_msgs/MotorStatus"; };
    const char * getMD5(){ return "d771017cd812838d32da48fbe32b0928"; };

  };

}
#endif