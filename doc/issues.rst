Known issues/limitation/things-yet-yo-be-implemented
=====================================================

- Groups cannot have white spaces in its name when they are created
- Layers cannot be created from a given resource already uploaded (limitation of the REST API)
- It would be interesting to implement rearranging of catalog elements via drag&drop (i.e., moving a resource from one workspace to another). Internally that might require several operations, so it might be taime-consuming to implement that, since the REST API does not support those operations, and a long workaround is needed.
- Styles are not correectly uploaded if they are complex.
- Layers, groups and styles do not support using namespaces when handled through the REST API
- Creating spatialite stores when the QGIS layer is a spatialite-based one. Maybe even use spatialite as the default format for unsupported formats, instead of converting to shapefiles.

- Refactoring the explorer module. Functionality should be moved to the ExplorerTree class, since now it is a bit messy.

- Improve signaling when a drag&drop operation is not permited

draggin and dropping should use default workspace in some operations, if not dropping on workspace item. This operations are now not enable (i.e dropping a group in the "groups" element of a catalog)
