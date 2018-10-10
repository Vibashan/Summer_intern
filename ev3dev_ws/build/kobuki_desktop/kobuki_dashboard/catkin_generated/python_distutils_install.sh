#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/nikes/tum_simulator_ws/src/kobuki_desktop/kobuki_dashboard"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/nikes/tum_simulator_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/nikes/tum_simulator_ws/install/lib/python2.7/dist-packages:/home/nikes/tum_simulator_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/nikes/tum_simulator_ws/build" \
    "/usr/bin/python" \
    "/home/nikes/tum_simulator_ws/src/kobuki_desktop/kobuki_dashboard/setup.py" \
    build --build-base "/home/nikes/tum_simulator_ws/build/kobuki_desktop/kobuki_dashboard" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/nikes/tum_simulator_ws/install" --install-scripts="/home/nikes/tum_simulator_ws/install/bin"
