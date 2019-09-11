
# Bioinformatics Workshop Day 3 - To the Cloud!

_Ian Thomas, Nick May_

![](https://github.com/eresearchrmit/bioinfocloudtutorial/blob/master/meme.jpg "")

##  Introduction

This workshop introduces the NeCTAR research cloud, and how to create a specialised nodes for bioinformatics on the cloud for running common tools including your own Python or R programs. We introduce a well-known platform for building computational workflows of bioinformatics programs, and then show how to package up those tools (including ones you’ve created) into reusable containers.     Finally we address the problem of efficiently using these new cloud resources to speed up the execution of programs.


This workshop is intended as  a brief introduction to multiple topics in cloud computing for research in bioinformatics.   Hence we utilise material from existing tutorials and  there is much more material here than can be reasonably be expected to be explored in an afternoon.  We suggest you dip into the material as needed.  In most cases there are links to follow on material or for all the material in the specific tutorial .  Also, the staff at the Research Technology services are available to help give advice about how to adapt some of these concepts to your specific research problems. Have fun!

The sample data files mentioned in the tutorial can be found [Here](https://github.com/eresearchrmit/bioinfocloudtutorial/tree/master/data)

## 1. The NeCTAR Research Cloud

The NeCTAR research cloud (RC)  (http://nectar.org.au ) is a national facility that provides research compute resources to australian researchers.  The good news is that you have access to it right now, as all Austrialian researchers are allocated a small amount of resources with which to experiment.  RMIT has its own share of these resources that it can provide to RMIT researchers through an allocation scheme.

The primary purpose for the RC is for scaling up research programs to utilise more resources than are available on a typical desktop.  For example the largest NeCTAR instance has 32 CPU cores and 64GB or RAM, and you can also create multiple instances on which to run your programs.

Try it out!  The front page is at  http://nectar.org.au/cloudpage

The basic terminology of the cloud is described here: https://support.ehelp.edu.au/support/solutions/articles/6000055378-welcome

Creating an instance is described here: https://support.ehelp.edu.au/support/solutions/articles/6000055376-launching-virtual-machines

If you’d like to apply for additional resources then instructions are here:
https://support.ehelp.edu.au/support/solutions/articles/6000068044-managing-an-allocation

As well as deploying basic linux instances to use in your work, the NeCTAR RC also provides many predefined applications that you can deploy with only a few steps.
https://support.ehelp.edu.au/support/solutions/articles/6000168298-nectar-applications-overview

We will be using one of these packages:  Bioconda, in the next section.

## 2. Deploy Bioconda on the cloud


Bioconda (https://bioconda.github.io) is a Linux distribution that includes hundreds of applications from the bioinformatics domain.  It can provide an excellent platform for computational biology analyses. It can provide an environment  for running your own programs or tools.
For this cloud deployment, we will use the NeCTAR application environment preconfigured for Bioconda (and docker) Here are the detailed steps to follow to create a bioconda VM on NeCTAR: https://support.ehelp.edu.au/support/solutions/articles/6000174749-nectar-applications-bioconda

Notes:

* for the Instance flavour field, please select `m2.medium` (as we need a larger base directory to store docker images);
* for the instance image use `NeCTAR Ubuntu 18.04 LTS (Bionic) amd64 (with docker)`, as we use that docker functionality later.

Then connect to your instance  (e.g., putty)...

You can download the same test files fot this tutorial using the following commands:

        wget https://github.com/eresearchrmit/bioinfocloudtutorial/tree/master/data/in.fq
        wget https://github.com/eresearchrmit/bioinfocloudtutorial/tree/master/data/alignment.sam

Conda uses the idea of environments to separate installations  for different tasks.  Environments can have different packages and versions of tools.

        conda create -y --name seqtktest
        source activate seqtktest

        conda install -y samtools=1.9
        conda install -y seqtk=1.3

Convert FASTQ to FASTA:

        seqtk seq -a in.fq > out.fa

Reverse complement FASTA/Q:

         seqtk seq -r in.fq > out.fq


(See https://github.com/lh3/seqtk  for more)

        source deactivate

### Use Python


        conda create --name pythonenv python=3 pandas numpy timeit multiprocess
        source activate pythonenv
        python3 program.py
        source deactivate

### Use R

        conda create --name renv r
        source activate renv
        Rscript program.r
        Source deactivate

### Connecting to Cloudstor

The storage on the nectar instance is ephemeral, which means that if you delete the instance then the data is deleted permanently too!.  However,  you can utilise your existing cloudstor for permanent storage by connecting it  to your nectar instance.

* What is Cloudstor?
* Logging in.
   * https://cloudstor.aarnet.edu.au
   * using AAF.
* Creating an App Password.
   * Setting > Security > Create New App Password
   * copy key.
* Mounting your storage to the VM.
   * run command:         `cloudstor-setup`
   * https://support.ehelp.edu.au/support/solutions/articles/6000211327-using-aarnet-cloudstor-on-a-nectar-vm
* Checking synchronization.
   * create a test file:         `vi test.txt`
   * view online.
* Further information:
   * Set-up the Owncloud client on your desktop/laptop.
   * https://cloudstor.aarnet.edu.au/client-download/

## 3. Bioinformatics workflows

There are many choices in this space but here we demonstrate Galaxy (https://galaxyproject.org).  It  allows applications (installed using conda or docker containers) to be chained together into reproducible execution pipelines.

Although it possible install your own copy of galaxy server (we will see this later), for this workshop we will use an existing publically available australian galaxy instance:
https://usegalaxy.org.au

The basic tutorial for galaxy is at  https://galaxyproject.org/tutorials/g101/.  It is not expected that you can finish this tutorial in this session, but dip in and have a look around.

## 4. Containers for bioinformatics

It is important for scientific integrity that experimental results can be reproducible and this has traditionally been difficult programs for results produced by software.  Different runs of a program may require different versions of dependent software and therefore need to maintain potentially many exact environments can make reproducibility difficult.  We have seen how the concept of a conda environment can make this easier by allowing you pin the version of dependent libraries, but there is a   more general solution available that allows you to assemble your program and all its dependencies libraries and files into a single portable package. This technology is called containerisation.
The two major research focussed container technologies are Docker (http://docker.com) and Singularity (https://sylabs.io/docs/)

Here we introduce docker and show how it can be used to quickly run existing packages efficiently and reproducibly. . Your bioconda VM from before should already have docker software installed…

Basic commands:

* `docker build` = create an image from Dockerfile
* `docker pull` = download an existing image
* `docker run` = create and execute a container from the image
* `docker ps` = show the currently running containers
* `docker rm` = delete a container

Examples:

* Samtools (tool for working with SAM and BAM alignment files)

    Create a my_samtools/Dockerfile:

        FROM ubuntu
        RUN apt-get update && apt-get install -y samtools
        ENTRYPOINT [“samtools”]

    Build the image from the Dockerfile

        sudo docker build -t my_samtools my_samtools/

    Then try it out

        sudo docker run -i my_samtools view -S -b - < alignment.sam > alignment.bam

    (This example is from https://www.melbournebioinformatics.org.au/tutorials/tutorials/docker/media/#41 )

* There are many ready-to-use bioinformatics containers at : http://biocontainers.pro . For example,

        sudo docker pull quay.io/biocontainers/samtools:0.1.19--2
        sudo docker run --rm -v $PWD:/data quay.io/biocontainers/samtools:0.1.19--2 samtools view -S -b data/alignment.sam > alignment.bam


    All the tools from biolinux you may installed have their equivalent biocontainer versions.


    _Note you will need to open 8888/8080 ports using a security group for these to work._

* Jupyter notebooks (for python)

        sudo docker run -p 8888:8888 --name jupyter jupyter/scipy-notebook

    Then jupyter notebook will be available from http://instanceid:8888

    where `instanceid` is the public id address for the instance from the NeCTAR dashboard.

    See https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html for more information

* Rstudio (graphical interface)

        sudo docker run -p 8080:8787 -e PASSWORD=mypass bioconductor/release_core2

    Then Rstudio will be available from http://instanceid:8080

    where `instanceid` is the public id address for the instance from the NeCTAR dashboard.

    See https://andrewguy.github.io/RStudio-on-Nectar-with-Docker/  for more information

* Galaxy Workflow engine

    This is your own personal instance of the workflow engine we saw earlier

        sudo docker run -d -p 8080:80 bgruening/galaxy-stable

    Then galaxy will be available from http://instanceid:8080

    where `instanceid` is the public id address for the instance from the NeCTAR dashboard.

    See https://github.com/bgruening/docker-galaxy-stable for more information.

## 5. Cloud-based Scaling

The issue of scaling up a problem to properly utilise cloud resources can be complicated and there are many different approaches that are possible.

Here we concentrate on when to use various approaches and what benefits and in what situations.

 We consider two different approaches to this task:
* **Vertical scaling** (using a single larger VM with multiple cores)
* **Horizontal scaling** (using a large number of smaller VMs running parts of a single problem or  multiple instances of a problem).

### Vertical Scaling

In vertical scaling, we increase the performance of a program by utilizing the multiple computing cores typically present on modern PCs (and cloud nodes).  Although some programs may already be written to utilise all available cores, it is unlikely that python or R programs you will writes will utilise multiple cores without modification.

#### Vertical scaling in Python

        import time
        from timeit import timeit

        def sleeping(arg):
            time.sleep(0.1)
        from multiprocess import Pool
        ncores = 2
        pool = Pool(ncores)
        # sequential run
        %timeit list(map(sleeping, range(24)))
        # parallel run
        %timeit pool.map(sleeping, range(24))
        pool.close()

        2.4 s ± 260 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
        1.2 s ± 278 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)


This example comes from a tutorial at  https://hpc-carpentry.github.io/hpc-python/06-parallel

#### Vertical scaling in R

As with python, there are libraries allowing multi cores to be utilised in R.  There is a parallel
package  that allows a function to be applied in parallel to all elements of a loop utilising the existing cores of the machine:

        library(parallel)
        library(MASS)

        starts <- rep(100, 40)
        fx <- function(nstart) kmeans(Boston, 4, nstart=nstart)
        numCores <- detectCores()
        numCores

        system.time(
        results <- lapply(starts, fx)
        )

        system.time(
        results <- mclapply(starts, fx, mc.cores = numCores)
        )


There is also a parallel version of a for loop where the contents of the loop are applied in parallel:

        library(foreach)
        library(doParallel)

        registerDoParallel(numCores)  # use multicore, set to the number of our cores
        foreach (i=1:3) %dopar% {
        sqrt(i)
        }


These examples come from the tutorial at https://nceas.github.io/oss-lessons/parallel-computing-in-r/parallel-computing-in-r.html

### Horizontal scaling

There are many different ways of distributing a job across a collection of servers (called a cluster). Here we investigate an approach which uses GNU parallel to distribute jobs between Biolinux instances.  Your initial trial allocation of NeCTAR should be enough to create two small-sized instances, so these instructions could be utilised.

Assume two bioconda servers `server-a` and `server-b`. Both have been created on the NeCTAR research cloud share the same private key file called `mykey.pem` and each having a conda python environment `myenv` and an identical program `program.py`:


        import sys
        import time
        time.sleep(3)
        print("hello from run {}".format(sys.argv[1]))

The first step is to temporarily copy your private key file `mykey.pem` onto the `server-a`

        scp ~/.ssh/mykey.pem -i ~/.ssh/mykey.pem ubuntu@server-a:/home/ubuntu/.ssh/mykey.pem

(this instruction will change if you are using putty on windows to connect to your NeCTAR instance)

Connect to `server-a` as described in the first tutorial as usual using ssh or putty with the `mykey.pem` (e.g., `ssh -i ~/.ssh/mykey.pem ubuntu@server-a` for linux)

We now need to setup a new separate set of security keys that will this server to login to the other servers security and start tasks.

        source activate myenv
        cd ~/.ssh
        ssh-keygen -f gnu # press return until finished
        chmod 700 gnu gnu.pub
        cat gnu.pub >> authorized_keys
        (echo 'Host *'; echo 'StrictHostKeyChecking no'; echo 'IdentityFile /home/ubuntu/.ssh/mykey.pem' ) >> config

        ssh-copy-id -f -i gnu ubuntu@serverb # repeat for any other nodes
        ...
        rm -i mykey.pem # important, run this command only on server-a
        cd ..

Now you can run the parallel command from the server-a to schedule execution of other servers in your cluster. The following command runs the python `program.py` ten times with different parameters on the two elements in your cluster:

        seq 10 | parallel --env PATH  -S server-a,server-b ~/.parallel/my_cluster 'python3 program.py ' {}

This should output

        Hello from run 1
        Hello from run 2
        …
        Hello from run 10

But they should be in groups of two tasks in parallel.

## High performance computing systems

High-performance computing (HPC) systems solve a specific class of horizontal scaling where multiple nodes coordinate in order to work on a single problem.  In horizontal scaling we have discussed, the tasks that run on these nodes tend to be either partitions of the space of the problem or may be copies of the same program run with different input parameters.  The key property here is that the tasks are largely independent of each other so little coordination or communication is needed between the nodes.

In HPC a single problem is broken up to run over multiple nodes but typically the individual parts need extensive coordination to solve the overall problem.  This necessitates the need to invest in specialised high-performance networks and relatively powerful nodes.

Such setups are typically very expensive so it is more cost effective to centralise such a facility and share these resources with many users in order to maximise utilisation.  This is a high-performance computing centre:

* Many (potentially thousands) of high-powered computing nodes,
* High performance network interconnects,
* A queueing system to allow multiple users’ access and full utilisation of hardware,
* Suite of pre-optimised domain-specific applications.

The main provider of HPC for RMIT University  is the National Computing Infrastructure (NCI) which is located in Canberra.  This facility provides systems that are preconfigured with many common bioinformatics programs that are optimised to utilise multiple nodes and solve very large problems.  For example, here is the list of available NCI programs: https://opus.nci.org.au/display/Help/Software

When should you use an HPC system?    HPC is best suited to when you need well-known programs that are already installed and already optimised for that HPC use.  You can compile and run your own programs; however, you will see little performance improvement unless the program is written to use these cores and manage its own communication between nodes. The effort required to adapt existing programs can be substantial as you will need to use specific HPC libraries such as MPI : https://nci.org.au/sites/default/files/documents/2019-07/nci_intro_openmp_mpi_06Jan17.pdf

For more information about HPC user at RMIT, please talk to the Research Technology Service team, who can advise you of the best next steps.

Contact  eResearch and Research Technology Services under the form at
https://rmitheda.force.com/Researcherportal/s/research-support

## Notes: