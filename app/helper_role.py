from flask import current_app
from flask_login import current_user
from flask_principal import identity_loaded, identity_changed, ActionNeed, RoleNeed, Permission, Identity, AnonymousIdentity
from enum import Enum

# Custom roles and actions

class Role(str, Enum):
    admin = "admin"
    moderator = "moderator"
    wanner = "wanner"

class Action(str, Enum):
    edit = "create, update and delete"
    view = "list and read"
    moderate = "moderar"
    admin = "admin"

# Role Needs

__admin_role_need = RoleNeed(Role.admin)
__moderator_role_need = RoleNeed(Role.moderator)
__wanner_role_need = RoleNeed(Role.wanner)

# Action Needs

__admin_action_need = ActionNeed(Action.admin)
__edit_action_need = ActionNeed(Action.edit)
__view_action_need = ActionNeed(Action.view)
__moderate_action_need = ActionNeed(Action.moderate)

# Role  Permissions

requireAdminRole = Permission(__admin_role_need)
requireModeratorRole = Permission(__moderator_role_need)
requireWannerRole = Permission(__wanner_role_need)

# Action Permissions
requireAdminPermission = Permission(__admin_role_need)
requireEditPermission = Permission(__edit_action_need)
requireViewPermission = Permission(__view_action_need)
requireModeratePermission = Permission(__moderate_action_need)



@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        if current_user.role == Role.admin:
            identity.provides.add(__admin_role_need)
            # Action needs
            identity.provides.add(__admin_action_need)
            identity.provides.add(__edit_action_need)
            identity.provides.add(__view_action_need)
            identity.provides.add(__moderate_action_need)
        elif current_user.role == Role.moderator:
            # Role needs
            identity.provides.add(__moderator_role_need)
            # Action needs

            identity.provides.add(__view_action_need)
            identity.provides.add(__moderate_action_need)
        elif current_user.role == Role.wanner:
            # Role needs
            identity.provides.add(__wanner_role_need)
            # Action needs
            identity.provides.add(__edit_action_need)
            identity.provides.add(__view_action_need)
        else:
            current_app.logger.debug("Unkown role")

def notify_identity_changed():
    if hasattr(current_user, 'email'):
        identity = Identity(current_user.email)
    else:
        identity = AnonymousIdentity()
    
    identity_changed.send(current_app._get_current_object(), identity = identity)