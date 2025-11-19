from sqladmin import ModelView
from app.user.models import User

class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.is_active,
        User.is_superuser,
        User.created_at,
        User.changed_at,
    ]
    column_searchable_list = [User.username, User.email]
    column_details_exclude_list = [User.hashed_password]
    form_excluded_columns = [User.hashed_password, User.created_at, User.changed_at]

def register_user_views(admin):
    admin.add_view(UserAdmin)