# -*- coding: utf-8 -*-

# This file is part of 'dob'.
#
# 'dob' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'dob' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'dob'.  If not, see <http://www.gnu.org/licenses/>.
"""Facts Carousel Header (Fact meta and diff)"""

from __future__ import absolute_import, unicode_literals

from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import Label

__all__ = (
    'ZoneStreamer',
)


class ZoneStreamer(object):
    """"""
    def __init__(self, carousel):
        self.carousel = carousel

    def standup(self):
        self.streamer_style = self.carousel.classes_style['streamer']

    # ***

    def rebuild_viewable(self):
        """"""
        def _rebuild_viewable():
            self.zone_manager = self.carousel.zone_manager
            assemble_children()
            self.streamer_container = build_container()
            self.refresh_all_children()
            return self.streamer_container

        def assemble_children():
            self.children = []
            add_fact_banner()

        def add_fact_banner():
            add_interval_banner()

        # ***

        def add_interval_banner():
            self.interval_banner = Label(text='')
            self.children.append(self.interval_banner)

        # ***

        def build_container():
            streamer_container = HSplit(children=self.children)
            return streamer_container

        # ***

        return _rebuild_viewable()

    # ***

    def refresh_all_children(self):
        self.refresh_interval()

    # ***

    def selectively_refresh(self):
        self.refresh_interval()

    # ***

    def refresh_interval(self):
        tod_humanize = self.zone_manager.facts_diff.edit_fact.time_of_day_humanize
        interval_text = tod_humanize(show_now=True)
        self.interval_banner.text = self.bannerize(interval_text)
        # (lb): Not sure why, but unlike add_stylable_classes, which sets
        # widget.formatted_text_control.style, here we set widget.window's
        # style instead.
        self.interval_banner.window.style += ' class:streamer-line'
        self.add_stylable_classes()

    def add_stylable_classes(self):
        # Register class:streamer[-line] styles.
        friendly_name = 'streamer'
        for suffix in ('', '-line'):
            # The label itself, 'streamer', includes the '╭─...' border,
            # so 3 rows of output are styled. If you specify the whole container,
            # 'streamer-line', the style will include the blank lines, one
            # each, above and below those 3 rows.
            self.carousel.add_stylable_classes(
                self.interval_banner,
                friendly_name + suffix,
            )

    # ***

    # Interval as currently formatted has max 53 chars, e.g.,
    MAX_INTERVAL_WIDTH = len('Fri 13 Jul 2018 ◐ 11:40 PM — 12:29 AM Sat 14 Jul 2018')

    def bannerize(self, text):
        def _bannerize():
            # There are a few ways to style the banner, including the ANSI border,
            # and optionally including the before and after newlines. By default,
            # the 'streamer' class from the current style is used to style the
            # banner and ANSI border; and the 'streamer-line' class is used to
            # style the same, and also the blank lines before and after. You can
            # also stylize the banner conditionally using the same two options,
            # 'streamer' and 'streamer-line', from a stylit.conf rule set.
            bannerful = colorful_banner_town(text)
            parts = []
            # Inline style only applies to parts with text, so
            # using 'blank-line' style here would be fruitless.
            parts += [('', '\n')]
            parts += [(self.streamer_style, bannerful)]
            parts += [('', '\n')]
            return parts

        def colorful_banner_town(text):
            # MAYBE: (lb): We could go to the trouble of styling the ANSI border
            # separately than the text... but that seems a wee bit tedious to code.
            reps = self.carousel.avail_width - 1
            padded_text = '{0:<{1}}'.format(text, ZoneStreamer.MAX_INTERVAL_WIDTH)
            centered_text = '{0:^{1}}'.format(padded_text, reps)
            padded_hrule_top = '╭' + '─' * reps + '╮'
            padded_hrule_bot = '╰' + '─' * reps + '╯'
            banner = '{0}\n│{1}│\n{2}'.format(
                padded_hrule_top, centered_text, padded_hrule_bot,
            )
            return banner

        return _bannerize()

