import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
import random
import math

class MosquitoSwarmNode(Node):
    def __init__(self):
        super().__init__('mosquito_swarm_node')
        self.publisher = self.create_publisher(MarkerArray, '/mosquito_swarm_markers', 10)
        self.timer = self.create_timer(0.1, self.update_swarm)
        
        self.num_drones = 60
        self.target = [3.5, 3.5, 0.5]
        self.reset_swarm()

    def reset_swarm(self):
        # 原点付近へドローン群をリセット
        self.drones = [[random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(0.5, 1.2)] for _ in range(self.num_drones)]
        self.time_count = 0.0

    def update_swarm(self):
        self.time_count += 0.1

        # 【自動ループ機能】14秒経過したら自動的に原点へリセットして再スタート！
        if self.time_count > 14.0:
            self.reset_swarm()

        marker_array = MarkerArray()

        # ターゲット（赤色シリンダー）
        target_marker = Marker()
        target_marker.header.frame_id = "map"
        target_marker.header.stamp = self.get_clock().now().to_msg()
        target_marker.ns = "target"
        target_marker.id = 999
        target_marker.type = Marker.CYLINDER
        target_marker.action = Marker.ADD
        target_marker.pose.position.x = self.target[0]
        target_marker.pose.position.y = self.target[1]
        target_marker.pose.position.z = self.target[2]
        target_marker.scale.x = 0.8
        target_marker.scale.y = 0.8
        target_marker.scale.z = 1.0
        target_marker.color = ColorRGBA(r=1.0, g=0.2, b=0.2, a=0.8)
        marker_array.markers.append(target_marker)

        # ドローン群の移動
        for i in range(self.num_drones):
            pos = self.drones[i]
            dist_to_target = math.sqrt((pos[0]-self.target[0])**2 + (pos[1]-self.target[1])**2)

            if self.time_count < 4.0 or dist_to_target > 2.2:
                # 風による受動漂流
                pos[0] += 0.04 + random.uniform(-0.02, 0.02)
                pos[1] += 0.03 + random.uniform(-0.02, 0.02)
                pos[2] += random.uniform(-0.01, 0.01)
            else:
                # AI検知・アクティブ集積
                dx = self.target[0] - pos[0]
                dy = self.target[1] - pos[1]
                pos[0] += dx * 0.08 + random.uniform(-0.015, 0.015)
                pos[1] += dy * 0.08 + random.uniform(-0.015, 0.015)

            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = "mosquitoes"
            m.id = i
            m.type = Marker.SPHERE
            m.action = Marker.ADD
            m.pose.position.x = pos[0]
            m.pose.position.y = pos[1]
            m.pose.position.z = pos[2]
            m.scale.x = 0.15
            m.scale.y = 0.15
            m.scale.z = 0.15

            if dist_to_target <= 2.2 and self.time_count >= 4.0:
                m.color = ColorRGBA(r=1.0, g=0.8, b=0.0, a=0.9) # 黄色
            else:
                m.color = ColorRGBA(r=0.2, g=0.7, b=1.0, a=0.7) # 水色

            marker_array.markers.append(m)

        self.publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = MosquitoSwarmNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
