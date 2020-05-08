"""Simulation"""

import numpy as np
from farms_bullet.model.model import (
    SimulationModels,
    GroundModel,
    DescriptionFormatModel,
)
from farms_bullet.simulation.options import SimulationOptions
from salamandra_simulation.simulation import simulation_setup
from salamandra_simulation.options import SalamandraOptions
from network import SalamandraNetwork
import farms_pylog as pylog


def simulation(
        sim_parameters,
        arena='water',
        **kwargs
):
    """Main"""
    # Simulation options
    pylog.info('Creating simulation')
    n_iterations = int(sim_parameters.duration/sim_parameters.timestep)
    simulation_options = SimulationOptions.with_clargs(
        timestep=sim_parameters.timestep,
        n_iterations=n_iterations,
        **kwargs,
    )

    # Arena
    if arena == 'water':
        water_surface = 0
        arena = SimulationModels([
            DescriptionFormatModel(
                path='arena_water.sdf',
                spawn_options={
                    'posObj': [0, 0, water_surface],
                    'ornObj': [0, 0, 0, 1],
                }
            ),
            GroundModel(position=[0, 0, -1]),
        ])
    elif arena == 'amphibious':
        water_surface = -0.1
        arena = SimulationModels([
            DescriptionFormatModel(
                path='arena_amphibious.sdf',
                visual_options={
                    'path': 'BIOROB2_blue.png',
                    'rgbaColor': [1, 1, 1, 1],
                    'specularColor': [1, 1, 1],
                }
            ),
            DescriptionFormatModel(
                path='arena_water.sdf',
                spawn_options={
                    'posObj': [0, 0, water_surface],
                    'ornObj': [0, 0, 0, 1],
                }
            ),
        ])
    else:
        water_surface = -np.inf
        arena = SimulationModels([GroundModel(position=[0, 0, 0])])

    # Robot
    network = SalamandraNetwork(
        sim_parameters=sim_parameters,
        n_iterations=n_iterations
    )
    sim, data = simulation_setup(
        animat_sdf='salamandra_robotica.sdf',
        arena=arena,
        animat_options=SalamandraOptions.from_options(dict(
            water_surface=water_surface,
            spawn_position=sim_parameters.spawn_position,
            spawn_orientation=sim_parameters.spawn_orientation,
        )),
        simulation_options=simulation_options,
        network=network,
    )

    # Run simulation
    pylog.info('Running simulation')
    # sim.run(show_progress=show_progress)
    # contacts = data.sensors.contacts
    # gps = data.sensors.gps
    for iteration in sim.iterator(show_progress=True):
        # pylog.info(np.asarray(
        #     contacts.reaction(
        #         iteration=iteration,  # Current iteration
        #         sensor_i=0,  # 0...3, one for each leg
        #     )
        # ))
        # Position of head: gps.urdf_position(iteration=iteration, link_i=0)
        # You can make changes to sim_parameters and then update with:
        # network.robot_parameters.update(sim_parameters)
        assert iteration >= 0

    # Terminate simulation
    pylog.info('Terminating simulation')
    sim.end()
    return sim, data

