import rclpy,numpy,psutil
from rclpy.node import Node

from std_msgs.msg import Float32

class RpiMon(Node):
    def __init__(self):
        super().__init__('rpi_mon')
        self.ramPublisher = self.create_publisher(Float32, 'freeram', 1)
        timer_period = 2.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float32()
        msg.data = 100.0-psutil.virtual_memory()[2]
        self.ramPublisher.publish(msg)


def main(args=None):
    print('Hi from rpi_mon.')
    rclpy.init(args=args)

    rpi_mon = RpiMon()

    rclpy.spin(rpi_mon)

    rpi_mon.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
