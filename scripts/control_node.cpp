#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class ControlNode : public rclcpp::Node {
public:
    ControlNode() : Node("control_node") {
        sub_ = this->create_subscription<std_msgs::msg::String>(
            "vision_data", 10, std::bind(&ControlNode::callback, this, std::placeholders::_1));
            
        RCLCPP_INFO(this->get_logger(), "C++ Control Node Started");
    }
private:
    void callback(const std_msgs::msg::String::SharedPtr msg) const {
        if (msg->data == "[]") {
            RCLCPP_INFO(this->get_logger(), ">>> [C++] CLEAR: Path is empty.");
        } else {
            RCLCPP_WARN(this->get_logger(), ">>> [C++] DETECTED: Stop! Data: %s", msg->data.c_str());
        }
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ControlNode>());
    rclcpp::shutdown();
    return 0;
}