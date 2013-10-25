import unittest
from opengeo.plugin import OpenGeoPlugin

class ProcessingPluginTest(unittest.TestCase):
    """Test suite for OpenGeo Explorer plugin."""

    def testCreatePlugin(self):
        """Initialize plugin."""
        self.processingplugin = OpenGeoPlugin(IFACE)
        self.assertIsNotNone(self.processingplugin)
