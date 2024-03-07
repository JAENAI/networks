import socket
import threading
import os


class Client(threading.Thread):
    """
    Client class. It allows to create a client.
    Multiple clients will be created.

    Attributes:
        client_id: The id of the client
        total_clients: The number of clients
        filename: The name of the file to receive
        protocol: Protocol to be used
        window_size: Size of window

    """
    client_socket=""
    client_id=0
    total_clients=0
    filename=""
    buffer_size=0
    window_size=0
    server=""
    number_files=0

    def __init__(self,client_id,total_clients,filename,buffer_size,window_size,number_files):
        self.client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.filename=filename
        self.total_clients=total_clients
        self.client_id=client_id
        self.buffer_size=buffer_size
        self.window_size=window_size
        self.number_files=number_files
    
    def client_connect(self):
        """
        Connection of a client

        """
        msg="HELLO"
        self.client_socket.sendto(msg.encode(),(socket.gethostbyname(socket.gethostname()),8080))
        data,s_addr=self.client_socket.recvfrom(1024)
        self.server=s_addr
        print(f"Server {s_addr} sent {data}")

    def receive_file_go_back_n(self,n):
        """
        Receiving of bytes of data with go-back-n protocol
        """

        new_filename=f"client {str(self.client_id)} file {n} "+self.filename

        with open(new_filename,'wb') as file:
            expected_seqnum=0

            file_size=os.path.getsize(self.filename)
            while expected_seqnum<file_size//(self.buffer_size-7) + 1:
                data,_=self.client_socket.recvfrom(self.buffer_size)
                seqnum=expected_seqnum

                if seqnum==int(data[:7].decode()):
                    file.write(data[7:])
                    expected_seqnum+=1

                    ack_num=str(seqnum).encode()
                    self.client_socket.sendto(ack_num,self.server)
                else:
                    print(f"Out of order packet")

    def start(self):
        """
        Starting of a client thread
        """
        thread=threading.Thread(target=self.client_connect,args=())
        thread.start()
        thread.join()
        for i in range(self.number_files):
            thread_s=threading.Thread(target=self.receive_file_go_back_n,args=(i,))
            thread_s.start()
            thread_s.join()
        
        
    

        