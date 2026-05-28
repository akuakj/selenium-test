from setuptools import setup, find_packages

setup(
    name='selenium-test',
    version='1.0.0',
    packages=find_packages(),
)

# cd /mnt/d/projects/selenium-test
# docker run --rm --network host -e USE_SELENOID=true -e SELENOID_URL=http://localhost:4444/wd/hub zagss-tests
# $env:USE_SELENOID="true"; $env:SELENOID_URL="http://localhost:4444/wd/hub"; pytest tests/tests_ui/ -n 3 -v