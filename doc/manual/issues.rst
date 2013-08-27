Known issues/limitation/things-yet-yo-be-implemented
=====================================================

- Groups cannot have white spaces in its name when they are created

- Layers, groups and styles do not support using namespaces when handled through the REST API
- Creating spatialite stores when the QGIS layer is a spatialite-based one. Maybe even use spatialite as the default format for unsupported formats, instead of converting to shapefiles.


- Refactoring the explorer module. Functionality should be moved to the ExplorerTree class, since now it is a bit messy.

- Improve signaling when a drag&drop operation is not permited

