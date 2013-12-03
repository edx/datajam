# Django settings for insight server project.

#### edinsights-specific settings

from insightserver.common import *

INSTALLED_ANALYTICS_MODULES = [
    'modules.dump_to_db',
    'modules.instructor_dash',
    'modules.problem_answers',
]

print INSTALLED_ANALYTICS_MODULES
