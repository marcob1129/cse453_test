#include <rclcpp/rclcpp.hpp>                    
#include <sensor_msgs/msg/nav_sat_fix.hpp>  


class GPSProcessor : public rclcpp::Node
{
public:
    GPSProcessor() : Node("gps_processor")     //gps_processor node
    {
        // subscribes to the /fix topic and calls gpsCallback when a new message is received
        subscription_ = this->create_subscription<sensor_msgs::msg::NavSatFix>("/fix",10,std::bind(&GPSProcessor::gpsCallback,this,std::placeholders::_1));
    }

private:
    // subscription variable
    rclcpp::Subscription<sensor_msgs::msg::NavSatFix>::SharedPtr subscription_;


    //function is called when a new GPS message is received
    void gpsCallback(const sensor_msgs::msg::NavSatFix::SharedPtr msg)
    {
        double lat = msg->latitude;
        double lon = msg->longitude;
        double alt = msg->altitude;

        RCLCPP_INFO(this->get_logger(),
            "GPS: Lat = %f, Lon = %f, Alt = %f",
            lat, lon, alt);

    }
};


int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);                             
    rclcpp::spin(std::make_shared<GPSProcessor>());      
    rclcpp::shutdown();                                   
    return 0;                                             
}