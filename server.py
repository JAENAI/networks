import socket
import threading
import random
import time

class Server(threading.Thread):
    """
    Server class. It allows to create a server.
    Only one server will be created.

    Attributes:
        total_clients: Number of clients to expect
        filename: Path of file to send
        probability: Probability of a udp send failing
        protocol: Protocol to use
        window_size: Size of the window
    """
    number_conn=0
    server_socket=""
    filename=""
    probability=0 
    timeout=0
    buffer_size=0
    window_size=0
    number_files=0
    clients=[]
    times=[]

    def __init__(self,total_clients,filename,probability,timeout,buffer_size,window_size,number_files):
        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.filename=filename
        self.probability=probability
        self.timeout=timeout
        self.buffer_size=buffer_size
        self.total_clients=total_clients
        self.window_size=window_size
        self.number_files=number_files

    def new_connection(self,data,addr,lock):
        """
        Allows connection of each individual client to server.
        Then sends a welcome message.

        Args:
            data: Data sent by client to connect
            addr: Address of the client
            lock: Lock for sharing resources
        """
        lock.acquire()
        self.number_conn+=1
        print(f"Client {addr} sent {data}")
        msg="WELCOME Client "+ str(self.number_conn)
        self.server_socket.sendto(msg.encode(),addr)
        self.clients.append(addr)
        print(f"Number of connections : {self.number_conn}")
        lock.release()

    def udp_send_with_probability(self,data,addr):
        """
        Sends data with a simulation of errors depending on a given probability.

        Args:
            data: Data to be sent
            addr: Address of the receiver
        """
        if random.random()>self.probability:
            try:
                self.server_socket.sendto(data,addr)
            except socket.error as e:
                print(f"Error: {e}")
        else:
            print(f"Simulated error")

    def send_file_go_back_n(self,addr):
        """
        Send file to a client using go-back-n protocol.

        Args:
            addr: Address to send to.

        """
        
        #Opening file and storing content as data
        with open(self.filename,'rb') as file:
            data=file.read()
        
        #Splitting data into packets of size 1024
            size=self.buffer_size-7
            packets = [data[i:i+size] for i in range (0,len(data),size)]

        #Start go-back-n protocol

            base=0
            nextseqnum=0

            start=time.perf_counter()
            while base<len(packets):
                while nextseqnum < base + self.window_size and nextseqnum < len(packets):
                    packet=f"{nextseqnum:07d}".encode()+packets[nextseqnum]
                    self.udp_send_with_probability(packet,addr)
                    nextseqnum+=1

                try:
                    self.server_socket.settimeout(self.timeout)
                    ack,_= self.server_socket.recvfrom(self.buffer_size)
                    ack_num=int(ack.decode())
                    base=max(base,ack_num+1)
                except socket.timeout:
                    print(f"Timeout: Resend window ({base} to {nextseqnum-1})")
                    nextseqnum=base
            print(f"File downloaded by {addr}")
            stop=time.perf_counter()
            taken=stop-start
            self.times.append(taken)

    


    def start(self):
        """
        Starting of the server thread
        """
        self.server_socket.bind((socket.gethostbyname(socket.gethostname()),8080))
        lock=threading.Lock()
        try:
            while self.number_conn<self.total_clients:
                data,addr=self.server_socket.recvfrom(1024)
                thread = threading.Thread(target=self.new_connection, args=(data,addr,lock))
                thread.start()
                thread.join()

            for client in self.clients:
                for i in range(self.number_files):
                    thread_s=threading.Thread(target=self.send_file_go_back_n,args=(client,))
                    thread_s.start()
                    thread_s.join()

        except Exception as e:
            print(f"Error in server: {e}")

        finally:
            self.server_socket.close()
        print(f"Times taken : {self.times}")
