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
    admin = "admin"

# Needs

__admin_role_need = RoleNeed(Role.admin)
__moderator_role_need = RoleNeed(Role.moderator)
__wanner_role_need = RoleNeed(Role.wanner)

__admin_action_need = ActionNeed(Action.admin)
__moderator_action_need = ActionNeed(Action.edit)
__wanner_action_need = ActionNeed(Action.view)

# Permissions
require_admin_role = Permission(__admin_role_need)
require_moderator_role = Permission(__moderator_role_need)
require_wanner_role = Permission(__wanner_role_need)

require_admin_permission = Permission(__admin_role_need)
require_moderator_permission = Permission(__moderator_action_need)
require_wanner_permission = Permission(__wanner_action_need)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        if current_user.role == Role.admin:
            identity.provides.add(__admin_role_need)
            # Action needs
            identity.provides.add(__admin_action_need)
            identity.provides.add(__moderator_action_need)
            identity.provides.add(__wanner_action_need)
        elif current_user.role == Role.moderator:
            # Role needs
            identity.provides.add(__moderator_role_need)
            # Action needs
            identity.provides.add(__moderator_action_need)
            identity.provides.add(__wanner_action_need)
        elif current_user.role == Role.viewer:
            # Role needs
            identity.provides.add(__wanner_role_need)
            # Action needs
            identity.provides.add(__wanner_action_need)
        else:
            current_app.logger.debug("Unkown role")

def notify_identity_changed():
    if hasattr(current_user, 'email'):
        identity = Identity(current_user.email)
    else:
        identity = AnonymousIdentity()
    
    identity_changed.send(current_app._get_current_object(), identity = identity)