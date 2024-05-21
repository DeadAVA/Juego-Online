import socket
import threading
import tkinter as tk

def handle_client(client_socket, chat_log):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print("Cliente dice:", message)
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, "Cliente: " + message + "\n")
            chat_log.config(state=tk.DISABLED)
        except:
            print("Cliente desconectado")
            break

def send_message():
    message = message_entry.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Servidor: " + message + "\n")
    chat_log.config(state=tk.DISABLED)
    message_entry.delete(0, tk.END)
    client_socket.send(message.encode())

def chat1():
    global client_socket, chat_log, message_entry
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)

    print("Esperando conexión...")

    client_socket, client_address = server.accept()
    print("Conexión establecida con", client_address)

    root = tk.Tk()
    root.title("Chat1 - Servidor")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chat_log = tk.Text(frame, height=20, width=50)
    chat_log.config(state=tk.DISABLED)
    chat_log.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(frame, command=chat_log.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_log.config(yscrollcommand=scrollbar.set)

    message_entry = tk.Entry(root, width=50)
    message_entry.pack()

    send_button = tk.Button(root, text="Enviar", command=send_message)
    send_button.pack()

    receive_thread = threading.Thread(target=handle_client, args=(client_socket, chat_log))
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    chat1()
