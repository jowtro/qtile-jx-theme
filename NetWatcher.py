import os
from datetime import timedelta
from libqtile import bar
from libqtile.log_utils import logger
from libqtile.widget import base
from libqtile.images import Img


class NetWatcher(base.InLoopPollText, base._Widget, base.MarginMixin):
    """A simple but flexible text-based clock"""

    orientations = base.ORIENTATION_BOTH
    defaults = [
        ("format", "%H:%M", "A Python datetime format string"),
        ("update_interval", 10.0, "Update interval for the clock"),
        (
            "timezone",
            None,
            "The timezone to use for this clock, either as"
            ' string if pytz or dateutil is installed (e.g. "US/Central" or'
            " anything in /usr/share/zoneinfo), or as tzinfo (e.g."
            " datetime.timezone.utc). None means the system local timezone and is"
            " the default.",
        ),
        ("scale", True, "Enable/Disable image scaling"),
        ("rotate", 0.0, "rotate the image in degrees counter-clockwise"),
        ("image_on", None, "image_on"),
        ("image_off", None, "image_off"),
        ("url_monitor", None, "Image filename. Can contain '~'"),
    ]
    DELTA = timedelta(seconds=0.5)

    def __init__(self, length=bar.CALCULATED, **config):
        logger.info("INIT")
        self.img = None
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(NetWatcher.defaults)

        base._Widget.__init__(self, length, **config)
        self.add_defaults(NetWatcher.defaults)
        self.add_defaults(base.MarginMixin.defaults)
        self.filename = self.image_off

        # make the default 0 instead
        self._variable_defaults["margin"] = 0

    def _configure(self, qtile, _bar):
        base._Widget._configure(self, qtile, _bar)
        logger.info("configure")
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
        logger.info(self.filename)
        self._update_image()

        if self.calculate_length() == old_length:
            self.draw()
        else:
            self.bar.draw()

    def tick(self):
        self.cmd_update(self.poll())

    # adding .5 to get a proper seconds value because glib could
    # theoreticaly call our method too early and we could get something
    # like (x-1).999 instead of x.000
    def poll(self):
        resp = os.system(f"ping -c 1 {self.url_monitor}")
        if resp == 0:
            return self.image_on
        else:
            return self.image_off
