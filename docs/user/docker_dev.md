# Build garage Docker image from source

Garage source comes with a Makefile that contains recipes for building and
running different Docker configurations for garage

Garage uses multi-stage Docker builds with the Docker BuildKit backend. The
BuildKit backend is opt-in and needs to be enabled by setting environment
variable `DOCKER_BUILDKIT=1` in your shell. The Makefile takes care of that
for you.

The important Docker related `make` targets are:

- `run-dev`: builds and runs the Docker image with your copy of garage source
 installed. This builds the `garage-dev` target in Dockerfile and the
 resulting image is tagged as `rlworkgroup/garage-dev`
- `run-dev-nvidia`: same as `run-dev` with CUDA 11.0 and cuDNN 8.0 for taking
 advantage of NVIDIA GPUs and also supports environment visualization. The
 build target is `garage-dev-nvidia` and the resulting image is tagged as
 `rlworkgroup/garage-dev-nvidia`
- `run-dev-nvidia-headless`: same as `run-dev-nvidia` but without support for
 environment visualization. Suitable for running in headless mode for
 machines without a display.


### Prerequisites

Be aware of the following prerequisites to build the image.

- Install [Docker CE](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)
  version 19.03 or higher. Tested on version 19.03.

Tested on Ubuntu 16.04, 18.04 and 20.04.

### Build and run the `garage-dev` image

To build and run the headless image, first clone the garage repository,
move to the root folder of your local repository and then execute;

```bash
make run-dev RUN_CMD="python examples/tf/trpo_cartpole.py"
```

Where `RUN_CMD` specifies the executable to run in the container.

The previous command adds a volume from the `data` folder inside your cloned
garage repository to the `data` folder in the garage container, so any
experiment results ran in the container will be saved in the `data` folder
inside your cloned repository. The Makefile uses the same username and uid as
your current local account to create the default user in the Docker images.
This keeps things simple by allowing the Docker user to write to the data
directory without giving explicit permission.


By default, Docker generates random names for containers. If you want to specify
a name for the container, you can do so with the variable `CONTAINER_NAME`. As a
side effect, this will output the results in `data/$CONTAINER_NAME` directory
instead of the `data` directory.

```bash
make run-dev RUN_CMD="..." CONTAINER_NAME="my_container_123"
```

This will output results in `data/my_container_123` directory.

If you need to use MuJoCo, you need to place your key at `~/.mujoco/mjkey.txt`
or specify the corresponding path through the MJKEY_PATH variable:

```bash
make run-dev RUN_CMD="..." MJKEY_PATH="/home/user/mjkey.txt"
```

If you require to pass additional arguments to docker build and run commands,
you can use the variables BUILD_ARGS and RUN_ARGS, for example:

```bash
make run-dev BUILD_ARGS="--build-arg MY_VAR=123" RUN_ARGS="-e MY_VAR=123"
```

### Prerequisites for NVIDIA image

Additional to the prerequisites for the `garage` image, make sure to have:

- [Install the latest NVIDIA driver](https://tecadmin.net/install-latest-nvidia-drivers-ubuntu/),
  tested on nvidia driver version 455.45.01. CUDA 11.0 requires a minimum of
  version 450.36.06. If you need a different CUDA version, see
  [Using a different CUDA version](#using-a-different-cuda-version)
- [Install nvidia-container-runtime](https://github.com/NVIDIA/nvidia-container-runtime#installation)

Tested on Ubuntu 18.04 & 20.04.

### Build and run the NVIDIA image

The same rules for the headless image apply here, except that the target name
is:

```bash
make run-dev-nvidia ...
```

This make command builds the NVIDIA image and runs it in a non-headless mode.
It will not work on headless machines. You can run the NVIDIA in a headless
state using the following target:

```bash
make run-dev-nvidia-headless ...
```

### Expose GPUs for use

By default, `garage-nvidia` uses all of your gpus. If you want to customize
which GPUs are used and/or want to set the GPU capabilities exposed, as
described in official Docker documentation
[here](https://docs.docker.com/config/containers/resource_constraints/#gpu),
you can pass the desired values to `--gpus` option using the variable GPUS. For
example:

```bash
make run-dev-nvidia GPUS="device=0,2" ...
```

### Using a different CUDA version

The `garage-nvidia` Docker image uses `nvidia/cuda:11.0-cudnn8-runtime-ubuntu18.04`
as the parent image which requires NVIDIA driver version 450.36.06+. If you need
to use garage with a different CUDA version, you might be able to build the
`garage-nvidia` image from scratch using a different parent image using the
variable `PARENT_IMAGE`.

```bash
make run-dev-nvidia PARENT_IMAGE="nvidia/cuda:11.0-cudnn8-runtime-ubuntu18.04" ...
```

You can find the required parent images at [NVIDIA CUDA's DockerHub](https://hub.docker.com/r/nvidia/cuda/tags)

---

**This page was authored by Gitanshu Sardana
([@gitanshu](https://github.com/gitanshu>)),
with contributions from Angel Ivan Gonzalez
([@gonzaiva](https://github.com/gonzaiva))**
