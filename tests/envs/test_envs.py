import unittest

import gym
from nose2 import tools
import numpy as np

from garage.envs import DelayedActionEnv
from garage.envs import GridWorldEnv
from garage.envs import IdentificationEnv
from garage.envs import NoisyObservationEnv
from garage.envs import NormalizedEnv
from garage.envs.box2d import CarParkingEnv
from garage.envs.box2d import CartpoleEnv
from garage.envs.box2d import CartpoleSwingupEnv
from garage.envs.box2d import DoublePendulumEnv
from garage.envs.box2d import MountainCarEnv

MUJOCO_ENABLED = True
try:
    from garage.envs.mujoco import HalfCheetahEnv
    from garage.envs.mujoco import HopperEnv
    from garage.envs.mujoco import InvertedDoublePendulumEnv
    from garage.envs.mujoco import PointEnv
    from garage.envs.mujoco import SimpleHumanoidEnv
    from garage.envs.mujoco import SwimmerEnv
    from garage.envs.mujoco import Walker2DEnv
    from garage.envs.mujoco.gather import AntGatherEnv
    from garage.envs.mujoco.gather import PointGatherEnv
    from garage.envs.mujoco.gather import SwimmerGatherEnv
    from garage.envs.mujoco.maze import AntMazeEnv
    from garage.envs.mujoco.maze import PointMazeEnv
    from garage.envs.mujoco.maze import SwimmerMazeEnv
except OSError:
    print("Warning: MuJoCo not installed. Skipping MuJoCo-related tests")
    MUJOCO_ENABLED = False

simple_env_classes = [
    GridWorldEnv,
    CartpoleEnv,
    CarParkingEnv,
    CartpoleSwingupEnv,
    DoublePendulumEnv,
    MountainCarEnv,
]

if MUJOCO_ENABLED:
    simple_env_classes.extend([
        PointEnv,
        Walker2DEnv,
        SwimmerEnv,
        SimpleHumanoidEnv,
        InvertedDoublePendulumEnv,
        HopperEnv,
        HalfCheetahEnv,
        PointGatherEnv,
        SwimmerGatherEnv,
        AntGatherEnv,
        PointMazeEnv,
        SwimmerMazeEnv,
        AntMazeEnv,
    ])
envs = [cls() for cls in simple_env_classes]
envs.append(IdentificationEnv(CartpoleEnv, {}))
envs.append(NoisyObservationEnv(CartpoleEnv()))
envs.append(DelayedActionEnv(CartpoleEnv()))
envs.append(NormalizedEnv(CartpoleEnv()))
envs.append(gym.make("CartPole-v1"))


class TestEnvs(unittest.TestCase):
    @tools.params(*envs)
    def test_env(self, env):
        print("Testing", env.__class__)
        ob_space = env.observation_space
        act_space = env.action_space
        ob = env.reset()
        assert ob_space.contains(ob)
        a = act_space.sample()
        assert act_space.contains(a)
        res = env.step(a)
        assert ob_space.contains(res[0])  # res[0] --> observation
        assert np.isscalar(res[1])  # res[1] --> reward
        env.render()
        env.close()
