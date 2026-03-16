import customtkinter as ctk
import grpc
import calculator_pb2
import calculator_pb2_grpc

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

channel = grpc.insecure_channel("localhost:50051")
stub = calculator_pb2_grpc.CalculatorStub(channel)

app = ctk.CTk()
app.title("Scientific Calculator")
app.geometry("320x450")

expression = ""

display = ctk.CTkEntry(app, width=280, height=50, font=("Arial",20))
display.pack(pady=10)

def press(num):
    global expression
    expression += str(num)
    display.delete(0,"end")
    display.insert(0,expression)

def clear():
    global expression
    expression=""
    display.delete(0,"end")

def calculate(op):
    global expression
    try:
        if op in ["sin","cos","tan","sqrt","square"]:
            a=float(expression)

            if op=="sin":
                r=stub.Sin(calculator_pb2.OneNumberRequest(a=a))
            elif op=="cos":
                r=stub.Cos(calculator_pb2.OneNumberRequest(a=a))
            elif op=="tan":
                r=stub.Tan(calculator_pb2.OneNumberRequest(a=a))
            elif op=="sqrt":
                r=stub.Sqrt(calculator_pb2.OneNumberRequest(a=a))
            elif op=="square":
                r=stub.Square(calculator_pb2.OneNumberRequest(a=a))

        else:
            a,b=map(float,expression.split(op))

            if op=="+":
                r=stub.Add(calculator_pb2.TwoNumberRequest(a=a,b=b))
            elif op=="-":
                r=stub.Subtract(calculator_pb2.TwoNumberRequest(a=a,b=b))
            elif op=="*":
                r=stub.Multiply(calculator_pb2.TwoNumberRequest(a=a,b=b))
            elif op=="/":
                r=stub.Divide(calculator_pb2.TwoNumberRequest(a=a,b=b))

        display.delete(0,"end")
        display.insert(0,str(r.result))
        expression=str(r.result)

    except:
        display.delete(0,"end")
        display.insert(0,"Error")

frame = ctk.CTkFrame(app)
frame.pack()

buttons=[
("sin","sin"),("cos","cos"),("tan","tan"),("√","sqrt"),
("x²","square"),("C","clear"),

("7","7"),("8","8"),("9","9"),("/","/"),
("4","4"),("5","5"),("6","6"),("*","*"),
("1","1"),("2","2"),("3","3"),("-","-"),
("0","0"),(".","."),("=","="),("+","+")
]

row=0
col=0

for (text,val) in buttons:

    if val=="clear":
        cmd=clear
    elif val=="=":
        cmd=lambda:calculate("+") 
    elif val in ["+","-","*","/"]:
        cmd=lambda v=val: press(v)
    elif val in ["sin","cos","tan","sqrt","square"]:
        cmd=lambda v=val: calculate(v)
    else:
        cmd=lambda v=val: press(v)

    b=ctk.CTkButton(frame,text=text,width=60,height=40,command=cmd)
    b.grid(row=row,column=col,padx=5,pady=5)

    col+=1
    if col>3:
        col=0
        row+=1

app.mainloop()