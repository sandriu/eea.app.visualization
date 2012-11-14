""" Evolve to version 6.2
"""
import logging
from zope.component import queryAdapter
from zope.component.interface import interfaceToName
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationEnabled
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger("eea.app.visualization.upgrades")

def fix_column_labels(context):
    """ Move column label settings from facet annotations directly to daviz JSON
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IVisualizationEnabled)
    brains = ctool(
        object_provides=iface,
        show_inactive=True, Language='all'
    )

    logger.info('Fixing daviz column labels: %s', len(brains))
    for brain in brains:
        doc = brain.getObject()
        mutator = queryAdapter(doc, IVisualizationConfig)
        data = mutator.json
        properties = data.get('properties', {})
        facets = mutator.facets
        logger.info("Fixing column labels for %s", doc.absolute_url())
        for facet in facets:
            name = facet.get('name')
            label = facet.get('label', name)
            config = properties.get(name, {})
            config.setdefault('label', label)
        mutator.json = data
