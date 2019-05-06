from power_read.scope import Scope


class App:
    def __init__(self, scope: Scope):
        self.scope = scope
        # arduino.init()

    def run(self, traces):
        self.scope.get_traces(traces)
        self.scope.close()


if __name__ == '__main__':
    app = App(Scope())
    app.run(100)
