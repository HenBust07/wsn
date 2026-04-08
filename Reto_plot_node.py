import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class PlotNode(Node):
    def __init__(self):
        super().__init__('plot_node')

        self.subscription = self.create_subscription(
            Float32,
            'sensor_data',
            self.listener_callback,
            10
        )

        # Parámetros
        self.max_points = 100          # tamaño total del buffer
        self.visible_points = 50      # mitad del eje X (lo visible)

        self.data = []

    def listener_callback(self, msg):
        valor = msg.data

        # Añadir dato
        self.data.append(valor)

        #  Eliminar los más antiguos si se llena
        if len(self.data) > self.max_points:
            self.data.pop(0)

        self.get_logger().info(f'Temp: {valor:.2f}')

        # Actualizar gráfica cada muestra
        if len(self.data) % 1 == 0:
            self.plot()

    def plot(self):
        plt.figure()

        #  Solo mostrar los últimos "visible_points"
        data_visible = self.data[-self.visible_points:]

        plt.plot(data_visible)

        plt.title("Temperatura en tiempo real")
        plt.xlabel("Muestras recientes")
        plt.ylabel("°C")

        #  Limitar eje Y
        plt.ylim(0, 60)

        #  Limitar eje X (siempre mismo rango visual)
        plt.xlim(0, self.visible_points)

        plt.grid()

        plt.savefig('/data/plot.png')
        plt.close()

        self.get_logger().info("Gráfica actualizada")


def main(args=None):
    rclpy.init(args=args)
    node = PlotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


