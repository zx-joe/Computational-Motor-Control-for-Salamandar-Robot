""" Lab 6 System Animation"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from muscle_system import MuscleSystem


class SystemAnimation(object):
    """ SystemAnimation

    """

    def __init__(
            self,
            res_sys,
            pendulum_sys,
            muscle_sys,
            neural_sys=None,
            fps=50
    ):
        super(SystemAnimation, self).__init__()

        self.pendulum_sys = pendulum_sys
        self.muscle_sys = muscle_sys
        self.neural_sys = neural_sys
        self.time = res_sys[:, 0]
        self.state = res_sys[:, 1:]

        # Define positions for neurons
        self.neurons_pos = np.asarray([[-.5, .5],
                                       [.5, .5],
                                       [-0.25, 0.25],
                                       [0.25, 0.25]])
        self.fps = fps
        self.fig, self.ax = plt.subplots(num="Simulation")

        self.anims = self.animation_objects()
        t_max = self.time[-1]
        dt = 1 / float(fps)

        self.anim_link = animation.FuncAnimation(
            self.fig, self._animate, np.arange(0, t_max, dt),
            interval=1e3 / float(fps), blit=True
        )
        plt.title("LAB 6 : Neuromuscular simulation")
        plt.axis('scaled')
        # plt.axis('off')
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.set_frame_on('True')
        limit = 1.25 * self.pendulum_sys.parameters.L
        if limit < 0.5:
            limit = .5
        plt.axis([-limit, limit,
                  -1.5*limit, limit])
        plt.grid(False)
        return

    def animation_objects(self):
        """ Create and return animation objects """

        blue = (0.0, 0.3, 1.0, 1.0)

        # Origin
        self.ax.plot(
            [0, ], [-1, ], color='k', marker='o', markersize=12.5,
            zorder=4
        )

        # Pendulum
        pendulum = self.pendulum_sys.pose()
        self.line, = self.ax.plot(
            pendulum[:, 0],
            pendulum[:, 1] - 1.0,
            color=blue,
            linewidth=5,
            animated=True,
            zorder=1
        )
        # Mass
        self.m, = self.ax.plot(
            self.pendulum_sys.origin[0], self.pendulum_sys.parameters.L-1,
            color=blue, marker='o', markersize=12.5, animated=True
        )
        # Base
        self.ax.plot(
            [0.0, 0.0], [-1, 0], c='g', linewidth=7.5
        )

        # Muscles
        self.muscle_sys.update_attachment_position(self.state[0, 0])

        muscles = [
            self.ax.plot(
                m[:, 0], m[:, 1], color='r', linewidth=3.5, animated=True
            )[0]
            for m in [
                self.muscle_sys.muscle_1_pos_curr,
                self.muscle_sys.muscle_2_pos_curr,
            ]
        ]

        # Time
        time = self.ax.text(
            -0.2, 1.05, "Time: 0.0", fontsize=14, animated=True
        )

        # Neurons
        if self.neural_sys is not None:
            neurons = [self.ax.scatter(
                self.neurons_pos[:, 0], self.neurons_pos[:, 1],
                s=np.ones(4) * 350, c='r', animated=True, alpha=0.5)]
            for n in range(4):
                self.ax.text(
                    self.neurons_pos[n, 0], self.neurons_pos[n, 1],
                    "N{}".format(n+1), fontsize=11, animated=False,
                    zorder=10, horizontalalignment='center',
                    verticalalignment='center'
                )

            #: connections
            weights = (np.asarray(self.neural_sys.w)).T
            connections = np.nonzero(weights)
            for i, j in zip(connections[0], connections[1]):
                weight = weights[i, j]
                color = "red" if weight < 0.0 else "green"
                start = [self.neurons_pos[j, 0], self.neurons_pos[j, 1]]
                end = [self.neurons_pos[i, 0], self.neurons_pos[i, 1]]
                SystemAnimation.draw_arrow(
                    self.ax, start, end, color=color)
            start = [self.neurons_pos[0, 0], self.neurons_pos[0, 1]]
            end = [self.neurons_pos[0, 0], self.neurons_pos[0, 1]]
            handle1 = SystemAnimation.draw_arrow(
                self.ax, start, end, color="green")
            start = [self.neurons_pos[1, 0], self.neurons_pos[1, 1]]
            end = [self.neurons_pos[1, 0], self.neurons_pos[1, 1]]
            handle2 = SystemAnimation.draw_arrow(
                self.ax, start, end, color="green",
                connectionstyle="arc3,rad=-0.3"
            )
            return (
                [self.line, self.m] + muscles + [time] +
                neurons + [handle1] + [handle2]
            )
        return [self.line, self.m] + muscles + [time]

    @staticmethod
    def draw_arrow(ax, start, end, **kwargs):
        """ Draw arrow. """
        handle = ax.annotate(
            "",
            xy=(start[0], start[1]),
            xycoords='data',
            xytext=(end[0], end[1]),
            textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            color=kwargs.pop("color", "0.5"),
                            shrinkA=5, shrinkB=5,
                            patchA=None, patchB=None,
                            connectionstyle=kwargs.pop(
                                "connectionstyle", "arc3,rad=0.3")
                            ),
        )
        return handle

    @staticmethod
    def animate():
        """Animate System"""
        plt.show()
        return

    def _animate(self, time):
        """ Animation """
        index = np.argmin((self.time - time)**2)
        self.pendulum_sys.theta = self.state[index, 0]
        pendulum = self.pendulum_sys.pose()

        # Pendulum
        self.anims[0].set_xdata(pendulum[:, 0])
        self.anims[0].set_ydata(pendulum[:, 1]-1)

        # Mass
        self.anims[1].set_xdata([pendulum[1, 0]])
        self.anims[1].set_ydata([pendulum[1, 1] - 1])

        # Muscles
        self.muscle_sys.update_attachment_position(self.state[index, 0])
        muscles = [
            self.muscle_sys.muscle_1_pos_curr,
            self.muscle_sys.muscle_2_pos_curr,
        ]
        activations = [self.state[index, 2], self.state[index, 4]]
        for i, musc in enumerate(self.anims[2:4]):
            musc.set_color((activations[i], 0.0, 0.0, 1.0))
            musc.set_xdata(muscles[i][:, 0])
            musc.set_ydata(muscles[i][:, 1] - 1)

        # Text
        self.anims[4].set_text("Time: {:.1f}".format(self.time[index]))

        # Neurons
        if self.neural_sys is not None:
            n_rate = self.neural_sys.n_act(self.state[index, 6:])
            self.anims[5].set_color(
                np.asarray([[0.0, n_rate[0], 0.0, 1.0],
                            [0.0, n_rate[1], 0.0, 1.0],
                            [0.0, n_rate[2], 0.0, 1.0],
                            [0.0, n_rate[3], 0.0, 1.0]]))
            # self.anims[5].set_sizes(np.ones(4) * 250)
            self.anims[5].set_offsets(self.neurons_pos)
            p1 = (
                self.muscle_sys.muscle_1_pos_curr[0, :] +
                self.muscle_sys.muscle_1_pos_curr[1, :]
            )*0.5
            p2 = (
                self.muscle_sys.muscle_2_pos_curr[0, :] +
                self.muscle_sys.muscle_2_pos_curr[1, :]
            )*0.5
            self.anims[6].xy = (p1[0], p1[1]-1)
            self.anims[7].xy = (p2[0], p2[1]-1)
        return self.anims

