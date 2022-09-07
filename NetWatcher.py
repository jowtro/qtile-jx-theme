import os
from datetime import timedelta

# from threading import Thread
from libqtile import bar
from libqtile.log_utils import logger
from libqtile.widget import base
from libqtile.images import Img


class NetWatcher(base.InLoopPollText, base._Widget, base.MarginMixin):
    """A simple but flexible host monitor widget"""

    orientations = base.ORIENTATION_BOTH
    defaults = [
        ("update_interval", 10.0, "Update interval em secconds for the clock"),
        ("scale", True, "Enable/Disable image scaling"),
        ("rotate", 0.0, "rotate the image in degrees counter-clockwise"),
        ("image_on", None, "image_on file path"),
        ("image_off", None, "image_off file path"),
        ("host_monitor", None, "Url or server to Monitor"),
    ]
    DELTA = timedelta(seconds=0.5)

    def __init__(self, length=bar.CALCULATED, **config):
        logger.info("INIT NetWatcher")
        self.img = None
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(NetWatcher.defaults)

        base._Widget.__init__(self, length, **config)
        self.add_defaults(NetWatcher.defaults)
        self.add_defaults(base.MarginMixin.defaults)

        # make the default 0 instead
        self._variable_defaults["margin"] = 0

    def _configure(self, qtile, _bar):
        base._Widget._configure(self, qtile, _bar)
        self._update_image(self.image_on)

    def _update_image(self, filename):
        self.img = None

        if not filename:
            logger.warning("Image filename not set!")
            return

        filename = os.path.expanduser(filename)
        if not os.path.exists(filename):
            logger.warning("Image does not exist: %s", filename)
            return

        self.img = Img.from_path(filename)
        self.img.theta = self.rotate
        if not self.scale:
            return
        if self.bar.horizontal:
            new_height = self.bar.height - (self.margin_y * 2)
            self.img.resize(height=new_height)
        else:
            new_width = self.bar.width - (self.margin_x * 2)
            self.img.resize(width=new_width)

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
        self._update_image(filename)

        if self.calculate_length() == old_length:
            self.draw()
        else:
            self.bar.draw()

    def tick(self):
        home = os.getenv("HOME")
        with open(f"{home}/.config/qtile/test.txt", "r", encoding="UTF8") as file:
            txt = file.readline()
            if txt == "0":
                logger.info("NET DOWN")
                self.cmd_update(self.image_off)
            else:
                logger.info("NET UP")
                self.cmd_update(self.image_on)
