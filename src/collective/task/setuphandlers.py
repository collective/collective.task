# -*- coding: utf-8 -*-


def isNotCurrentProfile(context):
    return context.readDataFile('collectivetask_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
