%author: tiagoprn
%title: Docker fundamentals
%date: 2019-09-17 22:07:19

-> DOCKER FUNDAMENTALS  <-

---

-> # WHAT WILL WE COVER <-

- What is it?
- Features
- How does it work
- What it is useful for
- Docker compared to virtual machines
- Requirements to run
- Basics concepts
- How to "dockerize" an application
- Let's practice!
- Kubernetes

---

-> # WHAT IS DOCKER? <-

- Tool to *package* and *run* an *application* and all of its *dependencies* from
  one or more containers.

---

-> # FEATURES <-

- *Universal* way to *distribute* your apps
  (and avoid package dependencies hell)

- Containers are a *universal packaging format* and a *runtime contract*
  (resources like memory, cpus, etc)

---

-> # FEATURES <-

- Even if you don't directly customize a container's use of the
  host resources, docker makes sure *all containers are treated equally*
  and share the same resources.

- You can make a container *run in privileged mode* (with full access
  to the host networking, filesystem, sockets and etc...).
  USE WITH EXTREME CAUTION!

---

-> # FEATURES <-

- Containers can be *tagged with versions*. This allow easy *rollbacks*,
  or to split traffic of 2 different versions between 2 user groups
  in QA or production AKA *blue-green deployments*.
  And both with *no downtime*. :)

---

-> # FEATURES <-

- They are *stateless*...

- ...but you can use *volumes* [0] *to persist* data if you need.

- More than one container can *share the same volume*.

[0] Volumes can be locally shared folders between your host
    and a container, or remote storage like GlusterFS or S3

---

-> # HOW DOES IT WORK? <-

- A container is just *another process running* on your machine,
  but *an isolated one*. Each container has a "private view"
  of the operating system.

- Container *images are stored on your machine* when you do
  a `docker pull` from a registry. An image is analogous to
  a *tar archive* (which you can verify if you
  use the command `docker export`).

---

-> # HOW DOES IT WORK? <-

- Docker uses *linux kernel features* that exist for some time
  even pre-Docker era:

    - *Control Groups*: How many *resources* each process
                        will use (memory, cpu, network, etc)

    - *Namespaces*: A way to *isolate* a process from another
                    on the same machine.

---

-> # WHAT IS IT USEFUL FOR? <-

- Easy way to *distribute* ready-to-use production *application* stacks

- Make a better development environment:
  *"Code once, deploy on containers anywhere"*

- *Automated repeatable deploys*: Use a CI Server to automatically start
  docker containers with your app's code, run tests on it
  and automatically deploy new containers with the updated app
  if the tests pass.

---

-> # DOCKER COMPARED TO VIRTUAL MACHINES <-

- *Built-in batteries*: A Linux distribution with a Docker binary
                        is all you need.
                        No more installing of virtualbox, vmware,
                        compiling kernel modules...

- *Speed*: You don't need to wait for a full OS to boot:
           a running container is up quite as fast as a
           daemon / application on the machine.

- *Less Resources*: since you will not have the overhead of
                    a virtualization "hypervisor", you can have
                    much more containers than VMs on a single
                    physical host. That means more from your money.
                    In production, solutions like Kubernetes
                    choose which host is the best one to host your app.

---

-> # DOCKER COMPARED TO VIRTUAL MACHINES <-

- *Portability*: Dockerfiles ("recipes" to build containers)
                 are text files that will weight some KBs
                 at large. You can also use a public or
                 private "registry" to push and pull images
                 built with those recipes - and even those
                 ideally will weight at most a little hundreds of MB.

- *Resource allocation*: as in a Virtual Machine, you can control
                         how much cpu, memory and disk a container
                         will be able to use.

---

-> # DOCKER COMPARED TO VIRTUAL MACHINES <-

- If for some reason you need a virtual machine...
    you can choose one and run a linux distribution
    with Docker installed on it and have the best of both worls.

- One example of a hybrid scenario would be to use 3 *VMs*
  on a single machine *to simulate a Kubernetes cluster*
  with a master and worker nodes, which would be cheaper
  than buying 3 physical machines. :)

---

-> # REQUIREMENTS TO RUN DOCKER <-


- *Linux* (native),
  *Windows* or *MacOS* (which use virtualization under the hoods)

- *Docker package* installed (packaged by the distribution
                              or third-party)

-> ## ON YOUR DEVELOPMENT ENVIRONMENT <-

- *docker-compose package* installed (makes it easy
  to run entire app stacks with a configuration file)

-> ## IN PRODUCTION <-

- *kubernetes distribution* (AWS, GCP, Azure...
  or bare metal if you are brave enough).

---

-> # BASIC CONCEPTS <-

- *Docker image*: A "packaged app". The "template" to run
                  your containers from. It is `BUILT`
                  through a `Dockerfile`, where each instruction
                  generates a `layer` in the image.

- *Container*: This is what you `RUN` from an image.
               They are ephemeral.

---

-> # BASIC CONCEPTS <-

- *Dockerfile*: a "recipe' used to `build` a container.
                Generates an `image`.

- *Registry*: a central repository where you upload
              your docker images to be used by who
              needs them. The "official" one
              is called "Dockerhub". You can also
              host your own on your private network.

---

-> # HOW TO "DOCKERIZE" AN APPLICATION <-

- Choose a *base image* (language images, OS images)

- Install the *NECESSARY packages*

- Add your *custom files*

- Define the *exposed ports*

- Define the *entrypoint* (so a container can be started
                           from the image doing
                           something useful)

- Use *configuration files* and/or *environment variables*.

---

-> # HOW TO "DOCKERIZE" AN APPLICATION <-

- Define a *user on your host to run your containers*
  (by default this user is `docker`). DO NOT RUN THEM
  AS root TO AVOID COMPROMISING YOUR DOCKER HOST.
  [Here is an article](https://medium.com/@mccode/understanding-how-uid-and-gid-work-in-docker-containers-c37a01d01cf)
  explaining how this works.

- DO NOT SAVE ANY PERSISTENT DATA INSIDE THE CONTAINER
  (use mounted volumes or bind mounts -
  folder on the host linked inside the container)

- DO NOT USE LOG FILES. Log into `stdout` or `stderr`.
  This way you can inspect your streamed logs with `docker logs`.

---

-> # HOW TO "DOCKERIZE" AN APPLICATION <-

- When writing the Dockerfile, *first write the commands*
  that are *less likely to change*.
  E.g. install your pip requirements first, since they
       change less then your app code. That way
       docker can make a more efficient use
       of the image layers, and therefore optimize
       the space used to store an image.

---

-> # HOW TO "DOCKERIZE" AN APPLICATION <-

- Each app/service/repository must be *one separate container.*

- You can also dockerize your app dependencies, separately.
  E.g., a database or queue. Locally you can orchestrate/link them
        through docker-compose, and in production through
        Kubernetes (K8s).

---

-> # HOW TO "DOCKERIZE" AN APPLICATION <-

- Adhere to the [12-factor apps rules ](https://12factor.net/)
- More details [here](https://hackernoon.com/how-to-dockerize-any-application-b60ad00e76da)

---

-> # ENOUGH TALKING, HOW ABOUT SOME PRACTICE NOW? <-

Exercise 1) Let's Dockerize a *simple python flask api*

Run cookiecutter to create a flask app:
    $ cookiecutter gh:tiagoprn/minimal_flask_app_cookiecutter

[Here is the dockerfile that will be used](https://github.com/tiagoprn/devops/tree/master/dockerfiles/python_webapp_example).

---

-> # ENOUGH TALKING, HOW ABOUT SOME PRACTICE NOW? <-

Exercise 2) Let's Dockerize a more complicated *django api that makes use of a database.*

- The application has 2 containers, one for the app
and another for the database.
- I could setup a docker-compose for both containers,
but to enforce the idea that no container should have more
than one app and each container must be its' own separate entity,
each one have their own docker-compose orchestration file.

- Clone the repository at https://github.com/tiagoprn/catalog-sample-django-drf-app.git

- Read its instructions at the [README.md file](https://github.com/tiagoprn/catalog-sample-django-drf-app/blob/master/README.md#running-the-app).

---

-> # ENOUGH TALKING, HOW ABOUT SOME PRACTICE NOW? <-

Exercise 3) Let's use a *privileged container* (portainer) that can be used
   to manage containers through a Web UI.

- Clone the repository at https://github.com/tiagoprn/devops.git

- Read the instructions at the [README.md file](https://github.com/tiagoprn/devops/tree/master/docker_composes/portainer)

---

-> # KUBERNETES <-

- Coming soon, this does not end here. ;)

---

-> # THANK YOU, AND LET'S DOCKERIZE ALL THE THINGS! <-

PS: Check this [mind-blowing use of docker containers](https://iximiuz.com/en/posts/from-docker-container-to-bootable-linux-disk-image/).
