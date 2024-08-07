# Dockerfile for constructing the DAFNI model container: PYRAMID-prepare-data
# Copyright (C) 2023  Robin Wardle & Newcastle University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

###############################################################################
# Base image
###############################################################################
FROM ubuntu:20.04

###############################################################################
# Installation variables
###############################################################################
ARG APP_HOME=/src

###############################################################################
# Anaconda set up
# See: https://pythonspeed.com/articles/activate-conda-dockerfile/
###############################################################################

# Relevant environment variables. conda needs to be added to the PATH
# environment variable so subsequent conda commands work
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# Update apt
RUN apt update --fix-missing
RUN apt install wget -y
RUN apt upgrade -y

# Get and install Anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh -O ~/anaconda.sh
RUN /bin/bash ~/anaconda.sh -b -p /opt/conda
RUN ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
RUN conda update -y -n base -c defaults conda

# Use conda and strict channel priority (setup ~/.condarc for this)
# This is needed for wradlib to install properly
RUN echo -e \
"channel_priority: strict\n\
channels:\n\
  - conda-forge\n\
  - defaults" > ~/.condarc

# Create conda environment and set the shell to make sure all
# commands are run within it
WORKDIR $APP_HOME
COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "prepare-data", "--no-capture-output", "/bin/bash", "-c"]

COPY prepare-data.ipynb ./
COPY write_output_metadata.py ./
COPY run.sh ./

# Produce the Python file from the Notebook. We could run this directly using
# the --execute flag in run.sh
RUN jupyter nbconvert --to python prepare-data.ipynb

#RUN python -m pip install --upgrade pip
#RUN python -m pip install -r requirements.txt

# Entry point
ENV PREPARE_DATA_ENV=docker
WORKDIR $APP_HOME
CMD ["conda", "run", "-n", "prepare-data", "--no-capture-output", "/bin/bash", "run.sh"]
