import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class MoveTurtle(Node):
    def __init__(self):
        super().__init__('move_turtle')

        # Publisher per moure la tortuga
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # Subscriber per llegir la posició
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.listener_callback,
            10
        )

        self.stopped = False  # Flag per controlar si ja s'ha aturat

    def listener_callback(self, msg):
        twist = Twist()

        # Si la tortuga supera x o y > 7 → s’atura
        if msg.x > 7.0 or msg.y > 7.0:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            if not self.stopped:
                self.get_logger().info('Turtle stopped!')
                self.stopped = True
        else:
            twist.linear.x = 1.0   # velocitat lineal segura
            twist.angular.z = 1.0  # velocitat angular segura
            self.stopped = False

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()