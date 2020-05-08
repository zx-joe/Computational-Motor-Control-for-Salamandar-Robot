import numpy as np
import math
import farms_pylog as pylog
import copy


class MuscleSystem(object):
    """Class comprising of the antagonist muscle pair
    """

    def __init__(self, muscle_1, muscle_2):
        super(MuscleSystem, self).__init__()
        self.muscle_1 = muscle_1
        self.muscle_2 = muscle_2

        (self.muscle_1_length,
         self.muscle_2_length) = self.compute_default_muscle_length()

        #: Net muscle system torque
        self.torque = 0.0

        #: Attachment Point Attributes
        self.a1_m1 = None
        self.a2_m1 = None
        self.a1_m2 = None
        self.a2_m2 = None

        # Muscle 1 acts in negative torque direction
        self.dir1 = -1.0
        # Muscle 2 acts in positive torque direction
        self.dir2 = 1.0

        #: Muscle Position
        self.muscle_1_pos = None
        self.muscle_2_pos = None
        self.muscle_1_pos_curr = None
        self.muscle_2_pos_curr = None

    ########## INITIALIZATION METHODS ##########

    def initialize_muscle_length(self, angle):
        """Initialize the muscle contractile and tendon length.

        Parameters
        ----------
        self: type
            description
        angle: float
            Initial position of the pendulum [rad]

        """

        self.update_attachment_position(angle)
        self.update_attachment_distances()
        self.update_muscle_length()

        l_ce_1 = self.muscle_1.compute_initial_l_ce(
            self.muscle_1_length
        )
        l_ce_2 = self.muscle_2.compute_initial_l_ce(
            self.muscle_2_length
        )
        return np.asarray([l_ce_1, l_ce_2])

    def attach(self, muscle_1_pos, muscle_2_pos):
        """ Muscle attachment points.

        Parameters:
        -----------
            muscle_1_pos : <numpy.array>
                Attachment point of muscle 1.
                [origin,
                 insertion]
            muscle_2_pos : <numpy.array>
                Attachment point of muscle 2.
                [origin,
                 insertion]

        Example:
        --------
        >>> muscle_1_pos = numpy.array([[-5.0, 0.0],
                                       [0.0, 1.0]])
        >>> muscle_2_pos = numpy.array([[5.0, 0.0],
                                       [0.0, 1.0]])
        """
        self.muscle_1_pos = muscle_1_pos
        self.muscle_1_pos_curr = copy.deepcopy(self.muscle_1_pos)
        self.muscle_2_pos = muscle_2_pos
        self.muscle_2_pos_curr = copy.deepcopy(self.muscle_2_pos)

        self.update_attachment_distances()

    ########## COMPUTE METHODS ##########
    @staticmethod
    def compute_distance_between_points(point_a, point_b):
        """ Compute eucledian distance between two points  """
        return np.linalg.norm(
            point_a - point_b
        )

    @staticmethod
    def compute_moment_arm(a1, a2, length, angle):
        """ Compute moment arm. """
        return (a1 * a2 * np.sin(angle) / length)

    @staticmethod
    def compute_muscle_torque(radius_vector, force_vector):
        """ Keyword Arguments:
            angle -- Angle of the Pendulum
        """
        return np.cross(radius_vector, force_vector)

    @staticmethod
    def compute_vector_from_points(point_a, point_b):
        """ Compute vector for given two points. """
        return point_b - point_a

    @staticmethod
    def compute_vector_norm(vector):
        """ Compute the norm of a vector. """
        return np.linalg.norm(vector)

    @staticmethod
    def compute_unit_vector_from_points(point_a, point_b):
        """ Compute unit vector for given two points. """
        vector = MuscleSystem.compute_vector_from_points(
            point_a, point_b
        )
        return vector/MuscleSystem.compute_vector_norm(vector)

    @staticmethod
    def rot_matrix(angle):
        return np.asarray(
            [[np.cos(angle), -np.sin(angle)],
             [np.sin(angle), np.cos(angle)]]
        )

    ########## UPDATE METHODS ##########
    def update(self, angle, l_ce_1, l_ce_2):
        """ Update the muscle system. """
        self.update_attachment_position(angle)
        self.update_attachment_distances()
        self.update_muscle_length()
        self.update_moment_arm(angle)
        self.update_muscle_torque(l_ce_1, l_ce_2)

    def update_attachment_distances(self):
        """ Update the distances between the pendulum joint
            and muscle attachment origin and inertion point.
        """

        # Muscle 1
        self.a1_m1 = MuscleSystem.compute_distance_between_points(
            self.muscle_1_pos[0], np.zeros((2,))
        )
        self.a2_m1 = MuscleSystem.compute_distance_between_points(
            self.muscle_1_pos[1], np.zeros((2,))
        )

        # Muscle 2
        self.a1_m2 = MuscleSystem.compute_distance_between_points(
            self.muscle_2_pos[0], np.zeros((2,))
        )
        self.a2_m2 = MuscleSystem.compute_distance_between_points(
            self.muscle_2_pos[1], np.zeros((2,))
        )

    def update_attachment_position(self, angle):
        """ Compute the muscle position from joint angle.

        Parameters:
        -----------
            angle : <float>
                Pendulum angle

        Returns:
        --------
            muscle_1_pos : <float>
                Updates Attachment points of muscle 1
            muscle_2_pos : <float>
                Updates Attachment points of muscle 2
        """

        # Update muscle attachment points on the pendulum
        rotation = MuscleSystem.rot_matrix(angle)
        self.muscle_1_pos_curr[1, :] = rotation@self.muscle_1_pos[1, :]
        self.muscle_2_pos_curr[1, :] = rotation@self.muscle_2_pos[1, :]

    def update_muscle_length(self):
        """ Compute the muscle length from joint angle.
        """
        self.muscle_1_length = MuscleSystem.compute_distance_between_points(
            self.muscle_1_pos_curr[0, :], self.muscle_1_pos_curr[1, :]
        )
        self.muscle_2_length = MuscleSystem.compute_distance_between_points(
            self.muscle_2_pos_curr[0, :], self.muscle_2_pos_curr[1, :]
        )

    def update_moment_arm(self, angle):
        """ Compute the moment arm of the muscles based on the joint angle.

        moment = a1*a2

        Parameters
        ----------
        angle: float
            Current angle of the pendulum

        """
        # Muscle 1 moment arm
        self.moment1 = MuscleSystem.compute_moment_arm(
            self.a1_m1, self.a2_m1, self.muscle_1_length, angle
        )
        # Muscle 2 moment arm
        self.moment2 = MuscleSystem.compute_moment_arm(
            self.a1_m2, self.a2_m2, self.muscle_2_length, angle
        )

    def update_muscle_torque(self, l_ce_1, l_ce_2):
        """ Keyword Arguments:
            angle -- Angle of the Pendulum
        """

        #: Compute tendon slack length from current state
        l_se_1 = self.muscle_1_length - l_ce_1
        l_se_2 = self.muscle_2_length - l_ce_2

        #: Compute radius and force vectors for muscle 1
        r1 = MuscleSystem.compute_vector_from_points(
            np.zeros((2,)), self.muscle_1_pos_curr[1, :]
        )
        f1 = MuscleSystem.compute_unit_vector_from_points(
            self.muscle_1_pos_curr[1, :], self.muscle_1_pos_curr[0, :]
        )
        f1 = self.muscle_1.compute_tendon_force(l_se_1)*f1
        muscle_1_torque = np.cross(r1, f1)
        #: Compute radius and force vectors for muscle 2
        r2 = MuscleSystem.compute_vector_from_points(
            np.zeros((2,)), self.muscle_2_pos_curr[1, :]
        )
        f2 = MuscleSystem.compute_unit_vector_from_points(
            self.muscle_2_pos_curr[1, :], self.muscle_2_pos_curr[0, :]
        )
        f2 = self.muscle_2.compute_tendon_force(l_se_2)*f2
        #: Update torque
        self.torque = (
            MuscleSystem.compute_muscle_torque(r1, f1) +
            MuscleSystem.compute_muscle_torque(r2, f2)
        )

    def compute_default_muscle_length(self):
        """ Compute the default length of the muscles. """

        m1_l_mtu = self.muscle_1.l_slack + self.muscle_1.l_opt
        m2_l_mtu = self.muscle_2.l_slack + self.muscle_2.l_opt

        return m1_l_mtu, m2_l_mtu

    def derivative(self, state, time, *args):
        """ Muscle system derivatives
        Parameters
        ----------
        self: type
            description
        state: <array>
            States of the two muscles
        time: <float>
            Current integration time
        args: <list>
            Muscle stimulations at current integration time

        Returns
        -------
        derivative: <np.array>
            Derivative at current integration time

        """

        stimulations = args[0]

        # Update and retrieve the derivatives
        return np.concatenate((
            self.muscle_1.dxdt(
                state[: 2], time, stimulations[0], self.muscle_1_length
            ),
            self.muscle_2.dxdt(
                state[2:], time, stimulations[1], self.muscle_2_length
            )))

