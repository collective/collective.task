# -*- coding: utf-8 -*-
from Acquisition import aq_base, aq_inner, aq_parent
from collective.task.setuphandlers import PARENTS_FIELDS_CONFIG
from imio.migrator.migrator import Migrator
from plone import api
from plone.registry import Record, field
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging
import transaction

logger = logging.getLogger("collective.task")

SAVEPOINT_INTERVAL = 2000
COMMIT_INTERVAL = 20000
OBJ_ALREADY_COMMIT_REGISTRY = "collective.task.update_commit_obj"
TASK_ALREADY_COMMIT_REGISTRY = "collective.task.update_commit_task"


class Migrate_To_100(Migrator):
    id_to_registry = []
    count = 0

    def __init__(self, context):
        Migrator.__init__(self, context)
        self.catalog = api.portal.get_tool("portal_catalog")

    @property
    def get_already_update_task(self):
        return api.portal.get_registry_record(TASK_ALREADY_COMMIT_REGISTRY, default=[])

    @property
    def get_already_update_obj(self):
        return api.portal.get_registry_record(OBJ_ALREADY_COMMIT_REGISTRY, default=[])

    def create_registry(self, registry_name):
        registry = getUtility(IRegistry)
        if registry_name in registry:
            return

        registry.records[registry_name] = Record(
            field.List(
                title=u"Id already commit", value_type=field.TextLine(), default=[]
            )
        )

    def add_record_in_registry(self, registry_name):
        registry = getUtility(IRegistry)
        values = registry[registry_name]
        values += self.id_to_registry
        registry[registry_name] = values

    def commit(self, registry_name):
        transaction.commit()
        logger.info("Transaction commit ...")
        self.create_registry(registry_name)
        self.add_record_in_registry(registry_name)
        logger.info("Id updated put in registry")
        self.id_to_registry = []

    def _recursiveUpdateRoleMappings(self, ob, wfs):
        """Update roles-permission mappings recursively, and
        reindex special index.
        """
        # Returns a count of updated objects.
        count = 0
        if ob.absolute_url_path().decode("utf-8") not in self.already_update_obj:
            logger.info("Upgrade : {}".format(ob.absolute_url_path()))
            wf_ids = self.portal.portal_workflow.getChainFor(ob)
            if wf_ids:
                changed = 0
                for wf_id in wf_ids:
                    wf = wfs.get(wf_id, None)
                    if wf is not None:
                        did = wf.updateRoleMappingsFor(ob)
                        if did:
                            changed = 1
                if changed:
                    count = count + 1
                    if hasattr(aq_base(ob), "reindexObject"):
                        # Reindex security-related indexes
                        try:
                            ob.reindexObject(idxs=["allowedRolesAndUsers"])
                        except TypeError:
                            # Catch attempts to reindex portal_catalog.
                            pass
            self.id_to_registry.append(ob.absolute_url_path().decode("utf-8"))
            self.count += 1
        else:
            logger.info("Object already updated : %s", ob.absolute_url_path())

        if self.count > 0 and self.count % SAVEPOINT_INTERVAL == 0:
            logger.info(
                "Start save point objects %s to %s",
                self.count - SAVEPOINT_INTERVAL,
                self.count,
            )
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

    def clean_registry(self):
        registry = getUtility(IRegistry)
        for name in [TASK_ALREADY_COMMIT_REGISTRY, OBJ_ALREADY_COMMIT_REGISTRY]:
            if name in registry.records:
                del registry.records[name]
                logger.info("Deleted registry record: %s", name)

    def run(self):
        logger.info("Migrating to collective.task 100")
        self.cleanRegistries()
        self.already_update_task = set(self.get_already_update_task)  # cached in memory
        self.already_update_obj = set(self.get_already_update_obj)  # cached in memory
        logger.info("Import profiles")
        self.runProfileSteps(
            "collective.task", steps=["typeinfo", "plone.app.registry", "workflow"]
        )
        logger.info("Update Role Mappings")
        self.updateRoleMappings()
        self.id_to_registry = []

        # Update existing objects
        logger.info("Reindex tasks")
        tasks = self.catalog(portal_type="task")
        for count, brain in enumerate(tasks):
            logger.info("%s/%s", count, len(tasks) + 1)
            if brain.UID.decode("utf-8") in self.already_update_task:
                logger.info("Task already updated")
                continue
            obj = brain.getObject()
            obj.__ac_local_roles_block__ = True
            obj.parents_assigned_groups = None
            obj.parents_enquirers = None
            obj.reindexObjectSecurity()
            self.id_to_registry.append(obj.UID().decode("utf-8"))
            if count > 0 and count % SAVEPOINT_INTERVAL == 0:
                logger.info(
                    "Start save point objects %s to %s",
                    count - SAVEPOINT_INTERVAL,
                    count,
                )
            transaction.savepoint(optimistic=True)
            if count > 0 and count % COMMIT_INTERVAL == 0:
                logger.info("Start commit tasks %s/%s", count, len(tasks) + 1)
                self.commit(TASK_ALREADY_COMMIT_REGISTRY)
        self.id_to_registry = []
        # settings config
        registry = getUtility(IRegistry)
        # if not registry.get('collective.task.parents_fields'):
        if True:
            registry["collective.task.parents_fields"] = PARENTS_FIELDS_CONFIG

        self.clean_registry()

        self.finish()


def migrate(context):
    """ """
    Migrate_To_100(context).run()
