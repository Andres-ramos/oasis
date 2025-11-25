# Official Python image
FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Create non-root user
RUN addgroup oasis_group 
RUN adduser oasis_user --ingroup oasis_group

# Install server dependencies
# See more here: https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/geolibs/#installing-geospatial-libraries
# Alpine Package  - PyPi Package - Reference
# g++             - fiona        - https://stackoverflow.com/questions/58700451/alpine-error-during-installing-python-shapely
# gdal (x2)       - gdal-config  - https://stackoverflow.com/a/50539325/13290655
# geos (x2)       - shapely      - https://stackoverflow.com/questions/58700451/alpine-error-during-installing-python-shapely
# musl-dev        - psycopg2     - https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-doc
# postgresql-libs - psycopg2     - https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock
# postgresql-dev  - psycopg2     - https://stackoverflow.com/questions/46711990/error-pg-config-executable-not-found-when-installing-psycopg2-on-alpine-in-dock
# proj (x3)       - pyproj       - https://gis.stackexchange.com/questions/383726/unable-to-install-proj-related-python-packages-in-a-linux-alpine-environment
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    binutils \
    g++ \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    proj-bin \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# RUN apt install \
#     binutils \
#     g++ \
#     gdal \
#     gdal-dev \
#     geos \
#     geos-dev \
#     musl-dev \
#     postgresql-dev \
#     postgresql-libs \
#     proj \
#     proj-dev \
#     proj-util

# Install app dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . .

# Switch to non-root user
USER oasis_user
