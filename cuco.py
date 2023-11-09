import tkinter as tk
import socket

class SocketGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Socket GUI")

        # Buat label dan entri untuk host
        self.host_label = tk.Label(master, text="Host:")
        self.host_label.pack(pady=10)
        self.host_entry = tk.Entry(master)
        self.host_entry.pack()

        # Buat label dan entri untuk port
        self.port_label = tk.Label(master, text="Port:")
        self.port_label.pack(pady=10)
        self.port_entry = tk.Entry(master)
        self.port_entry.pack()

        # Buat tombol untuk menjalankan fungsi test_socket_timeout()
        self.timeout_button = tk.Button(master, text="Test Socket Timeout", command=self.test_socket_timeout)
        self.timeout_button.pack(pady=10)

        # Buat tombol untuk menjalankan fungsi modify_buff_size()
        self.buff_size_button = tk.Button(master, text="Modify Buffer Size", command=self.modify_buff_size)
        self.buff_size_button.pack(pady=10)

        # Buat tombol untuk menjalankan fungsi main()
        self.main_button = tk.Button(master, text="Main", command=self.main)
        self.main_button.pack(pady=10)

        # Buat label untuk menampilkan hasil
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def test_socket_timeout(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Set the socket timeout
        s.settimeout(10)

        try:
            # Receive data from the socket
            data = s.recv(1024)
        except socket.timeout:
            # The socket timed out
            self.result_label.config(text="Socket timed out")
        else:
            # Data was received
            self.result_label.config(text=data.decode())

    def modify_buff_size(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Get the current buffer size
        bufsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

        # Set the new buffer size
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)

        # Get the new buffer size
        new_bufsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

        # Display the results
        self.result_label.config(text=f"Buffer size changed from {bufsize} to {new_bufsize}")

    def main(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Send a request to the server
        s.sendall("GET / HTTP/1.0\r\n\r\n".encode())

        # Receive data from the server
        data = s.recv(1024)

        # Display the results
        self.result_label.config(text=data.decode())

if __name__ == '__main__':
    root = tk.Tk()
    app = SocketGUI(root)
    root.mainloop()
