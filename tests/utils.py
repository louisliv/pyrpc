from pyrpc.decorators import safe_method

def fixture():
    fixture = {}

    @safe_method
    def plain_method():
        pass

    class PlainClass():
        @safe_method
        def class_plain_method(self):
            pass

    fixture['test_class'] = PlainClass
    fixture['test_method'] = plain_method

    return fixture