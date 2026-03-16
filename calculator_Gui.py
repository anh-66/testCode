import customtkinter as ctk
import grpc
import calculator_pb2
import calculator_pb2_grpc

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# gRPC connection
channel = grpc.insecure_channel("localhost:50051")
stub = calculator_pb2_grpc.CalculatorStub(channel)

app = ctk.CTk()
app.title("Scientific Calculator")
app.geometry("320x450")

expression = ""

display = ctk.CTkEntry(app, width=280, height=50, font=("Arial", 20))
display.pack(pady=10)


# ---------------- FUNCTIONS ----------------

def update_display():
    display.delete(0, "end")
    display.insert(0, expression)


def press(value):
    global expression
    expression += str(value)
    update_display()


def clear():
    global expression
    expression = ""
    update_display()


def calculate():
    global expression
    try:

        # unary operations
        unary_ops = {
            "sin": stub.Sin,
            "cos": stub.Cos,
            "tan": stub.Tan,
            "sqrt": stub.Sqrt,
            "square": stub.Square
        }

        for op in unary_ops:
            if expression.startswith(op):
                num = float(expression.replace(op, ""))
                r = unary_ops[op](calculator_pb2.OneNumberRequest(a=num))
                expression = str(r.result)
                update_display()
                return

        # binary operations
        binary_ops = {
            "+": stub.Add,
            "-": stub.Subtract,
            "*": stub.Multiply,
            "/": stub.Divide
        }

        for op in binary_ops:
            if op in expression:
                a, b = map(float, expression.split(op))
                r = binary_ops[op](calculator_pb2.TwoNumberRequest(a=a, b=b))
                expression = str(r.result)
                update_display()
                return

    except Exception as e:
        display.delete(0, "end")
        display.insert(0, "Error")
        print("Error:", e)


# ---------------- BUTTON UI ----------------

frame = ctk.CTkFrame(app)
frame.pack()

buttons = [
    ("sin", "sin"), ("cos", "cos"), ("tan", "tan"), ("√", "sqrt"),
    ("x²", "square"), ("C", "clear"),

    ("7", "7"), ("8", "8"), ("9", "9"), ("/", "/"),
    ("4", "4"), ("5", "5"), ("6", "6"), ("*", "*"),
    ("1", "1"), ("2", "2"), ("3", "3"), ("-", "-"),
    ("0", "0"), (".", "."), ("=", "="), ("+", "+")
]

row = 0
col = 0

for text, val in buttons:

    if val == "clear":
        cmd = clear
    elif val == "=":
        cmd = calculate
    elif val in ["+","-","*","/"]:
        cmd = lambda v=val: press(v)
    elif val in ["sin","cos","tan","sqrt","square"]:
        cmd = lambda v=val: press(v)
    else:
        cmd = lambda v=val: press(v)

    b = ctk.CTkButton(frame, text=text, width=60, height=40, command=cmd)
    b.grid(row=row, column=col, padx=5, pady=5)

    col += 1
    if col > 3:
        col = 0
        row += 1

app.mainloop()