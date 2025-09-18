# -*- coding: utf-8 -*-
from Acquisition import aq_base, aq_inner, aq_parent
from collective.task.setuphandlers import PARENTS_FIELDS_CONFIG
from imio.migrator.migrator import Migrator
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.annotation.interfaces import IAnnotations
from BTrees.OOBTree import OOBTree

import logging
import transaction

logger = logging.getLogger("collective.task")

SAVEPOINT_INTERVAL = 2000
COMMIT_INTERVAL = 20000
OBJ_ALREADY_COMMIT_ANNOTATION = "collective.task.update_commit_obj"
TASK_ALREADY_COMMIT_ANNOTATION = "collective.task.update_commit_task"


class Migrate_To_100(Migrator):
    id_to_annotation = []
    count = 0

    def __init__(self, context):
        Migrator.__init__(self, context)
        self.catalog = api.portal.get_tool("portal_catalog")
        self.portal = api.portal.get()
        self.annotations = IAnnotations(self.portal)

    def init_annotation(self):
        # self.clear_annotations()
        if not OBJ_ALREADY_COMMIT_ANNOTATION in self.annotations:
            self.annotations[OBJ_ALREADY_COMMIT_ANNOTATION] = OOBTree()
        if not TASK_ALREADY_COMMIT_ANNOTATION in self.annotations:
            self.annotations[TASK_ALREADY_COMMIT_ANNOTATION] = OOBTree()

    def get_annotation(self, annotation_name):
        return self.annotations[annotation_name]

    def clear_annotation(self, annotation_name):
        if annotation_name in self.annotations:
            del self.annotations[annotation_name]

    def add_data_in_annotation(self, annotation_name):
        annotation = self.annotations[annotation_name]
        for obj_id in self.id_to_annotation:
            annotation[obj_id] = True
        self.id_to_annotation = []

    def commit(self, annotation_name):
        transaction.commit()
        self.add_data_in_annotation(annotation_name)
        self.id_to_annotation = []

    def _recursiveUpdateRoleMappings(self, ob, wfs):
        """Update roles-permission mappings recursively, and
        reindex special index.
        """
        # Returns a count of updated objects.
        count = 0
        self.id_to_annotation.append(path)
            transaction.savepoint(optimistic=True)

        if self.count > 0 and self.count % COMMIT_INTERVAL == 0:
            logger.info(
                "Start commit objects %s to %s",
                self.count - COMMIT_INTERVAL,
                self.count,
            )
            self.commit(OBJ_ALREADY_COMMIT_REGISTRY)

        if hasattr(aq_base(ob), "objectItems"):
            obs = ob.objectItems()
            if obs:
                for k, v in obs:
                    changed = getattr(v, "_p_changed", 0)
                    count = count + self._recursiveUpdateRoleMappings(v, wfs)
                    if changed is None:
                        # Re-ghostify.
                        v._p_deactivate()
        return count

    def updateRoleMappings(self, REQUEST=None):
        """Allow workflows to update the role-permission mappings."""
        portal_workflow = self.portal.portal_workflow
        wfs = {}
        for id in portal_workflow.objectIds():
            wf = portal_workflow.getWorkflowById(id)
            if hasattr(aq_base(wf), "updateRoleMappingsFor"):
                wfs[id] = wf
        portal = aq_parent(aq_inner(portal_workflow))
        count = self._recursiveUpdateRoleMappings(portal, wfs)
        if REQUEST is not None:
            return portal_workflow.manage_selectWorkflows(
                REQUEST, manage_tabs_message="%d object(s) updated." % count
            )
        else:
            return count

    def clear_annotations(self):
        for name in [TASK_ALREADY_COMMIT_ANNOTATION, OBJ_ALREADY_COMMIT_ANNOTATION]:
            self.clear_annotation(name)


    def run(self):
        logger.info("Migrating to collective.task 100")
        self.cleanRegistries()
        self.init_annotation()
        self.already_update_task = set(
            self.get_annotation(TASK_ALREADY_COMMIT_ANNOTATION).keys()
        )  # cached in memory
        self.already_update_obj = set(
            self.get_annotation(OBJ_ALREADY_COMMIT_ANNOTATION).keys()
        )  # cached in memory
        logger.info("Import profiles")
        self.runProfileSteps(
            "collective.task", steps=["typeinfo", "plone.app.registry", "workflow"]
        )
        logger.info("Update Role Mappings")
        self.updateRoleMappings()
        self.id_to_annotation = []

        # Update existing objects
        logger.info("Reindex tasks")
        tasks = self.catalog(portal_type="task")
        for count, brain in enumerate(tasks):
            logger.info("%s/%s", count, len(tasks) + 1)
            if brain.UID.decode("utf-8") in self.already_update_task:
                logger.info("Task already updated")
                continue
        self.id_to_annotation = []
        # settings config
        registry = getUtility(IRegistry)
        # if not registry.get('collective.task.parents_fields'):
        if True:
            registry["collective.task.parents_fields"] = PARENTS_FIELDS_CONFIG

        self.clear_annotations()

        self.finish()


def migrate(context):
    """ """
    Migrate_To_100(context).run()
