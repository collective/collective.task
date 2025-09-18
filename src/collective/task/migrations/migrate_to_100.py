# -*- coding: utf-8 -*-
from Acquisition import aq_base, aq_inner, aq_parent
from BTrees.OOBTree import OOBTree
from collective.task.setuphandlers import PARENTS_FIELDS_CONFIG
from imio.migrator.migrator import Migrator
from plone import api
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

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
        """Update roles-permission mappings recursively, and reindex special index."""
        count = 0

        if not self._should_skip(ob):
            # logger.info("Upgrade : {}".format(ob.absolute_url_path()))
            updated = self._update_workflow_mappings(ob, wfs)
            if updated:
                count += 1
                self._maybe_reindex(ob)

            self._track_object(ob)
            self._maybe_savepoint(self.count, OBJ_ALREADY_COMMIT_ANNOTATION)
            self._maybe_commit(self.count, OBJ_ALREADY_COMMIT_ANNOTATION)
        # else:
        #     logger.info("already updated")

        count += self._process_children(ob, wfs)
        return count

    def _should_skip(self, ob):
        """Check if object should be skipped based on already updated list."""
        path = ob.absolute_url_path().decode("utf-8")
        return path in self.already_update_obj

    def _update_workflow_mappings(self, ob, wfs):
        """Update workflow role mappings for an object. Return True if changed."""
        changed = False
        wf_ids = self.portal.portal_workflow.getChainFor(ob)
        for wf_id in wf_ids or []:
            wf = wfs.get(wf_id)
            if wf is not None and wf.updateRoleMappingsFor(ob):
                changed = True
        return changed

    def _maybe_reindex(self, ob):
        """Reindex object if possible."""
        if hasattr(aq_base(ob), "reindexObject"):
            try:
                ob.reindexObject(idxs=["allowedRolesAndUsers"])
            except TypeError:
                # Ignore portal_catalog itself
                pass

    def _track_object(self, ob):
        """Add object to annotation and update counters."""
        path = ob.absolute_url_path().decode("utf-8")
        self.id_to_annotation.append(path)
        self.count += 1

    def _maybe_savepoint(self, count, name, logger_msg=None):
        """Savepoint every SAVEPOINT_INTERVAL objects."""
        if count > 0 and count % SAVEPOINT_INTERVAL == 0:
            if logger_msg is None:
                logger_msg = "Start save point objects {} to {} ({})".format(
                    count - SAVEPOINT_INTERVAL, count, name
                )
            logger.info(logger_msg)
            transaction.savepoint(optimistic=True)
            logger.info("End save point")

    def _maybe_commit(self, count, annontation, logger_msg=None, force_commit=False):
        """Commit every COMMIT_INTERVAL objects."""
        if len(self.id_to_annotation) <= 0:
            return
        if force_commit or (count > 0 and count % COMMIT_INTERVAL == 0):
            if logger_msg is None:
                logger_msg = "Start commit objects {} to {} ({})".format(
                    count - COMMIT_INTERVAL, count, annontation
                )
            logger.info(logger_msg)
            self.commit(annontation)
            logger.info("End commit")

    def _process_children(self, ob, wfs):
        """Recursively update children if object has them."""
        total = 0
        if hasattr(aq_base(ob), "objectItems"):
            for _, child in ob.objectItems() or []:
                changed = getattr(child, "_p_changed", 0)
                total += self._recursiveUpdateRoleMappings(child, wfs)
                if changed is None:
                    child._p_deactivate()  # Re-ghostify
        return total

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

    def reindex_task(self, brain, count, total):
        obj = brain.getObject()
        obj.__ac_local_roles_block__ = True
        obj.parents_assigned_groups = None
        obj.parents_enquirers = None
        obj.reindexObjectSecurity()
        self.id_to_annotation.append(obj.UID().decode("utf-8"))

        self._maybe_savepoint(count, TASK_ALREADY_COMMIT_ANNOTATION)
        self._maybe_commit(count, TASK_ALREADY_COMMIT_ANNOTATION)

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
        self._maybe_commit(self.count, OBJ_ALREADY_COMMIT_ANNOTATION, force_commit=True)
        self.id_to_annotation = []

        # Update existing objects
        tasks = self.catalog(portal_type="task")
        logger.info("Reindex {} tasks".format(len(tasks)))
        for count, brain in enumerate(tasks):
            if brain.UID.decode("utf-8") in self.already_update_task:
                continue
            self.reindex_task(brain, count, len(tasks))
        self._maybe_commit(count, TASK_ALREADY_COMMIT_ANNOTATION, force_commit=True)

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
