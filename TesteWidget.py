import os
import sys
import time
from datetime import datetime, timedelta, timezone
from libqtile import bar
from libqtile.log_utils import logger
from libqtile.widget import base
from libqtile.images import Img


try:
    import pytz
except ImportError:
    pass

try:
    import dateutil.tz
except ImportError:
    pass


class TesteWidget(base.InLoopPollText, base._Widget, base.MarginMixin):
    """A simple but flexible text-based clock"""

    orientations = base.ORIENTATION_BOTH
    defaults = [
        ("format", "%H:%M", "A Python datetime format string"),
        ("update_interval", 1.0, "Update interval for the clock"),
        ("timezone",None,
            "The timezone to use for this clock, either as"
            ' string if pytz or dateutil is installed (e.g. "US/Central" or'
            " anything in /usr/share/zoneinfo), or as tzinfo (e.g."
            " datetime.timezone.utc). None means the system local timezone and is"
            " the default.",
        ),
        ("scale", True, "Enable/Disable image scaling"),
        ("rotate", 0.0, "rotate the image in degrees counter-clockwise"),
        ("filename", None, "Image filename. Can contain '~'"),
    ]
    DELTA = timedelta(seconds=0.5)

    def __init__(self, length=bar.CALCULATED, **config):
        if hasattr(config, "timezone"):
            self.timezone = config["timezone"]
        else:
            self.timezone = None
        self.img = None

        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(TesteWidget.defaults)

        base._Widget.__init__(self, length, **config)
        self.add_defaults(TesteWidget.defaults)
        self.add_defaults(base.MarginMixin.defaults)

        # make the default 0 instead
        self._variable_defaults["margin"] = 0
        if isinstance(self.timezone, str):
            if "pytz" in sys.modules:
                self.timezone = pytz.timezone(self.timezone)
            elif "dateutil" in sys.modules:
                self.timezone = dateutil.tz.gettz(self.timezone)
            else:
                logger.warning(
                    "Clock widget can not infer its timezone from a"
                    " string without pytz or dateutil. Install one"
                    " of these libraries, or give it a"
                    " datetime.tzinfo instance."
                )
        if self.timezone is None:
            logger.debug("Defaulting to the system local timezone.")

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        self._update_image()

    def _update_image(self):
        self.img = None

        if not self.filename:
            logger.warning("Image filename not set!")
            return

        self.filename = os.path.expanduser(self.filename)

        if not os.path.exists(self.filename):
            logger.warning("Image does not exist: %s", self.filename)
            return

        img = Img.from_path(self.filename)
        self.img = img
        img.theta = self.rotate
        if not self.scale:
            return
        if self.bar.horizontal:
            new_height = self.bar.height - (self.margin_y * 2)
            img.resize(height=new_height)
        else:
            new_width = self.bar.width - (self.margin_x * 2)
            img.resize(width=new_width)

    def draw(self):
        if self.img is None:
            return

        self.drawer.clear(self.background or self.bar.background)
        self.drawer.ctx.save()
        self.drawer.ctx.translate(self.margin_x, self.margin_y)
        self.drawer.ctx.set_source(self.img.pattern)
        self.drawer.ctx.paint()
        self.drawer.ctx.restore()

        if self.bar.horizontal:
            self.drawer.draw(
                offsetx=self.offset, offsety=self.offsety, width=self.width
            )
        else:
            self.drawer.draw(
                offsety=self.offset, offsetx=self.offsetx, height=self.width
            )

    def calculate_length(self):
        if self.img is None:
            return 0

        if self.bar.horizontal:
            return self.img.width + (self.margin_x * 2)
        else:
            return self.img.height + (self.margin_y * 2)

    def cmd_update(self, filename):
        old_length = self.calculate_length()
        self.filename = filename
        self._update_image()

        if self.calculate_length() == old_length:
            self.draw()
        else:
            self.bar.draw()

    def tick(self):
        self.update(self.poll())
        return self.update_interval - time.time() % self.update_interval

    # adding .5 to get a proper seconds value because glib could
    # theoreticaly call our method too early and we could get something
    # like (x-1).999 instead of x.000
    def poll(self):
        if self.timezone:
            now = datetime.now(timezone.utc).astimezone(self.timezone)
        else:
            now = datetime.now(timezone.utc).astimezone()
        return (now + self.DELTA).strftime(self.format)
