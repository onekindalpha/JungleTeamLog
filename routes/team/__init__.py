from .create import create_bp
from .users import users_bp
from .view import view_bp
from .scrums import scrums_bp
from .coretime import coretime_bf
from .wil import wil_bf
from .curriculum import curriculum_bp
from .goals import goals_bp

team_blueprints = [create_bp, users_bp, view_bp, 
                   scrums_bp, coretime_bf, wil_bf,
                   curriculum_bp, goals_bp]