import sympy


# command syntax = .integrate expression
def integral(command=""):
    try:
        # tidy command
        expression = command[10:]

        # set symbols to use in expression
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        z = sympy.Symbol('z')
        t = sympy.Symbol('t')

        # integration
        output = sympy.integrate(expression, x)
        return output

    except sympy.SympifyError as err:
        print(err)
        return err


# command syntax = .derive expression
def derivative(command=""):
    try:
        # tidy command
        expression = command[7:]

        # set symbols to use in expression
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        z = sympy.Symbol('z')
        t = sympy.Symbol('t')

        # integration
        output = sympy.diff(expression, x)
        return output

    except sympy.SympifyError as err:
        print(err)
        return err
