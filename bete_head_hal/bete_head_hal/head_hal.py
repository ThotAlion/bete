import rclpy,numpy,time
import pypot.robot
from rclpy.node import Node

from sensor_msgs.msg import JointState

class HeadHal(Node):
    def __init__(self):
        super().__init__('head_hal')
        self.jointPublisher = self.create_publisher(JointState, 'joint_states', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.robot = pypot.robot.from_json('/home/ubuntu/bete_ws/src/bete_head_hal/head.json')

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = super().get_clock().now().to_msg()
        msg.name = ['pan','tilt']
        msg.position = [self.robot.pan.present_position*numpy.pi/180.0,self.robot.tilt.present_position*numpy.pi/180.0]
        msg.velocity = [self.robot.pan.present_speed,self.robot.tilt.present_speed]
        msg.effort = [self.robot.pan.present_current,self.robot.tilt.present_current]

        self.jointPublisher.publish(msg)

    def stop(self):
        self.robot.compliant = True
        self.robot.close()

def main(args=None):
    print('Hi from bete_head_hal.')
    rclpy.init(args=args)

    head_hal = HeadHal()

    rclpy.spin(head_hal)

    head_hal.stop()
    head_hal.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
