from PyQt5.QtCore import Qt

from playground.core.modules import PlaygroundModule
from playground.core.widget import CETechWiget


class LevelWidget(CETechWiget, PlaygroundModule):
    Name = "level_editor"

    def __init__(self, module_manager):
        self.project = None

        super(LevelWidget, self).__init__()
        self.init_module(module_manager)

        self.dock = self.modules_manager.new_docked(self, self.Name, "Level editor", Qt.TopDockWidgetArea)

    def open_level(self, level_name):
        if not self.ready:
            return

        self.instance.console_api.lua_execute("Editor:load_level(\"%s\")" % level_name)

    def on_open_asset(self, path, name, ext):
        if ext == "level":
            if not self.instance.ready:
                return True

            self.open_level(name)
            return True

        return False

    def on_open_project(self, project):
        """
        :type project: cetech.project.ProjectManager
        """
        self.project = project

        self.set_instance(
            self.project.run_develop("LevelView", compile_=True, continue_=True, wid=self.wid,
                                     bootscript="playground/leveleditor_boot"))

    def on_close_project(self):
        if self.ready:
            self.instance.console_api.quit()
            self.instance.console_api.disconnect()