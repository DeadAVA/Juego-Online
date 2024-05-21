import socket
import tkinter as tk
import threading

def send_message():
    message = entry.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Tú: " + message + "\n")
    chat_log.config(state=tk.DISABLED)
    entry.delete(0, tk.END)
    client_socket.send(message.encode())

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, "Cliente: " + message + "\n")
            chat_log.config(state=tk.DISABLED)
        except:
            print("Error al recibir mensaje")
            break

def chat2():
    global client_socket, chat_log, entry
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    root = tk.Tk()
    root.title("Chat2")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chat_log = tk.Text(frame, height=20, width=50)
    chat_log.config(state=tk.DISABLED)
    chat_log.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(frame, command=chat_log.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_log.config(yscrollcommand=scrollbar.set)

    entry = tk.Entry(root, width=50)
    entry.pack()

    send_button = tk.Button(root, text="Enviar", command=send_message)
    send_button.pack()

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    chat2()
