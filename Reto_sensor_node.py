import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import serial

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')

        # Publisher (enviamos temperatura como float)
        self.publisher_ = self.create_publisher(Float32, 'sensor_data', 10)

        # Configurar puerto serial (Arduino)
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            self.get_logger().info("Puerto serial conectado")
        except:
            self.get_logger().error("No se pudo abrir /dev/ttyACM0")
            self.ser = None

        # Timer (resolución)
        self.timer = self.create_timer(5.0, self.publish_data)

    def publish_data(self):
        if self.ser is not None:
            try:
                # Vaciar buffer y tomar el último dato
                self.ser.reset_input_buffer()
                line = self.ser.readline().decode('utf-8').strip()

                if line != "":
                    adc = int(line)

                    # Mapear ADC (0–1023) → Temperatura (10–40 °C)
                    temp = 10 + (adc / 1023.0) * 30

                    # Publicar temperatura
                    msg = Float32()
                    msg.data = temp
                    self.publisher_.publish(msg)

                    self.get_logger().info(f'ADC: {adc} → Temp: {temp:.2f} °C')

            except Exception as e:
                self.get_logger().error(f"Error leyendo serial: {e}")
        else:
            self.get_logger().warn("Sin conexión al Arduino")

def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

