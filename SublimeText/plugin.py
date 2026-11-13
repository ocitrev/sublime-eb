import sublime, sublime_plugin
from os.path import getsize
import re
import uuid
from os.path import basename, splitext
import json

DO_NOT_RUN_HOOK = 'from_new_window_hook'

# turn off rulers for build output
def no_ruler_on_output_panel(win):
    win.create_output_panel('exec').settings().set("rulers", [])

def apply():
    [no_ruler_on_output_panel(w) for w in sublime.windows()]

def plugin_loaded():
    tmp = LoadSaveListener()
    tmp.run(sublime.active_window().active_view())
    apply()

class NewWindowHook(sublime_plugin.WindowCommand):
    def run(self):
        # re-run new_window command with DO_NOT_RUN_HOOK as parameter
        # to avoid running the hook again
        a = self.window.run_command("new_window", DO_NOT_RUN_HOOK)
        # change setting on each window after a new one was created
        apply()

class Listener(sublime_plugin.EventListener):
    def on_window_command(self, window, command_name, args):
        if command_name == "new_window" and args != DO_NOT_RUN_HOOK:
            return ("new_window_hook", None)
        return None

class LoadSaveListener(sublime_plugin.EventListener):
    def on_load_async(self, v):
        self.run(v)

    def on_post_save_async(self, v):
        self.run(v)

    def on_activated_async(self, v):
        self.run(v)

    def run(self, v):
        if (v.file_name()):
            try:
                self.show(v, getsize(v.file_name()))
            except:
                pass

    def show(self, v, size):
        suffix = " B"

        if size > 1000:
            size /= 1024
            suffix = " KB"

        if size > 1000:
            size /= 1024
            suffix = " MB"

        v.set_status("file_size", str(round(size, 2)) + suffix)

class GenerateUuidListenerCommand(sublime_plugin.EventListener):
    """
    Expand 'uuid' and 'uuid4' to a random uuid (uuid4) and
    'uuid1' to a uuid based on host and current time (uuid1).
    Searches for "uuid_uppercase" setting in user preferences, capitalizes
    UUID if true. - author Matt Morrison mattdmo@pigimal.com

    Author: Rob Cowie
    Seealso: https://github.com/SublimeText/GenerateUUID/issues/1

    * modified to remove 0x prefix and keyboard shortcuts
    """
    def on_query_completions(self, view, prefix, locations):

        md = re.match(r'^uuid([14])?(s)?$', prefix)

        if md:

            # default is 4
            type = md.group(1) or '4'

            if type == '1':
                # make a UUID based on the host ID and current time
                val = str(uuid.uuid1())
            elif type == '4':
                # make a random ac908eb3-e2f1-4f54-bce3-37127baa8860
                val = str(uuid.uuid4())
            elif type == '7':
                val = str(uuid.uuid7())

            if md.group(2) == 's':
                val = re.sub('-', '', val)

            settings = sublime.load_settings('Preferences.sublime-settings')
            if settings.get('uuid_uppercase'):
                val = val.upper()

            return [(prefix, prefix, val)]

        else:
            return []


class FormatJson(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view

    def indent(self, s):
        parsed = json.loads(s)
        return json.dumps(parsed, indent='\t', ensure_ascii=False)

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        language = splitext(basename(syntax))[0].lower() if syntax is not None else "plain text"
        return language

    def is_enabled(self):
        if self.view is None:
            return False

        return self.get_language() in ['json', 'plain text']

    def indent_region(self, edit, region):
        s = self.view.substr(region).strip()
        s = self.indent(s)
        if s:
            self.view.replace(edit, region, s)

    def run(self, edit):
        view = self.view
        regions = view.sel()

        if len(regions) > 1 or not regions[0].empty():
            for region in regions:
                if not region.empty():
                    self.indent_region(edit, region)
        else:
            self.indent_region(edit, sublime.Region(0, view.size()))


# import ctypes
# from ctypes import wintypes

# GetModuleHandle = ctypes.WinDLL('kernel32',use_last_error=True).GetModuleHandleW
# GetModuleHandle.argtypes = [wintypes.LPCVOID]
# GetModuleHandle.restype = wintypes.HANDLE
# p = ctypes.cast(GetModuleHandle(0) + 0x3D9000, ctypes.POINTER(ctypes.c_uint)).contents
# print(p)



import sublime
import sublime_plugin

class VsStyleColumnSelectCommand(sublime_plugin.TextCommand):
    debug = False

    def run(self, edit, forward=True):
        view = self.view
        selections_before = list(view.sel())

        if len(selections_before) == 0:
            return

        # Trouver la sÃ©lection avec la plus grande taille (la plus complÃ¨te)
        # ou utiliser la premiÃ¨re si forward=True, la derniÃ¨re si forward=False
        if forward:
            reference_region = selections_before[0]
        else:
            reference_region = selections_before[-1]

        anchor_col = view.rowcol(reference_region.begin())[1]
        target_size = reference_region.size()

        if self.debug:
            print(f"Before: {len(selections_before)} selection(s), forward={forward}")
            print(f"Anchor: col={anchor_col}, size={target_size}")

        # Laisser column_select faire son travail
        view.run_command("column_select", {"by": "lines", "forward": forward})

        selections_after = list(view.sel())

        # Corriger toutes les sÃ©lections
        view.sel().clear()
        for region in selections_after:
            row = view.rowcol(region.begin())[0]

            line_start_pt = view.text_point(row, 0)
            line_region = view.line(line_start_pt)
            line_length = line_region.end() - line_region.begin()

            col_start = min(anchor_col, line_length)
            col_end = min(anchor_col + target_size, line_length)

            pt_start = line_start_pt + col_start
            pt_end = line_start_pt + col_end

            view.sel().add(sublime.Region(pt_start, pt_end))

        if self.debug:
            print(f"After: {len(view.sel())} selection(s) at col={anchor_col}")
            print("---")

