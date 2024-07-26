# Main execution shell script for: PYRAMID-prepare-data
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

RUNNING_PLATFORM="${PREPARE_DATA_ENV:-shell}"

echo "Running in $RUNNING_PLATFORM"

DEBUG=
DEBUG=echo

if ${DEBUG};
then
  echo "Running in debug mode";
else
  echo "Running in normal mode";
fi

if [ "${RUNNING_PLATFORM}" == "docker" ];
then
    DATA_ROOT="/";
else
    DATA_ROOT="./";
fi

export DATA_PATH=${DATA_PATH:=${DATA_ROOT}data}
INPUTS=${DATA_PATH}/inputs
OUTPUTS=${DATA_PATH}/outputs

$DEBUG rm -r ${OUTPUTS}

python -u prepare-data.py
python -u write_output_metadata.py
