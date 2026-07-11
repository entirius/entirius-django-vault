# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = getattr(settings, "API_BASE_URL", "api").strip("/")
